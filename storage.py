"""Persistence for guests and wishlist sign-ups.

Uses a Google Sheet when Streamlit secrets contain `gcp_service_account` and
`sheet.spreadsheet`; otherwise falls back to a local JSON file (for local dev).
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

TZ = ZoneInfo("Europe/Zurich")
GUESTS_SHEET = "Gaeste"
GUESTS_HEADER = ["Name", "Titel", "Zeit", "Aufgabe"]
WISHES_SHEET = "Wunschliste"
WISHES_HEADER = ["Wunsch-ID", "Wunsch", "Name", "Zeit"]


def _now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M")


def _has_sheet_secrets() -> bool:
    try:
        return "gcp_service_account" in st.secrets and "sheet" in st.secrets
    except Exception:  # no secrets.toml at all
        return False


# ---------------------------------------------------------------- Google Sheets
@st.cache_resource(show_spinner=False)
def _spreadsheet():
    import gspread

    client = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    ref = st.secrets["sheet"]["spreadsheet"]
    return client.open_by_url(ref) if ref.startswith("http") else client.open_by_key(ref)


@st.cache_resource(show_spinner=False)
def _worksheet(title: str, header: tuple):
    import gspread

    book = _spreadsheet()
    try:
        ws = book.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = book.add_worksheet(title=title, rows=200, cols=len(header))
    if ws.row_values(1) != list(header):
        if ws.col_count < len(header):
            ws.add_cols(len(header) - ws.col_count)
        ws.update([list(header)], "A1")
    return ws


@st.cache_data(ttl=20, show_spinner=False)
def _cached_rows(title: str, header: tuple) -> list:
    return _worksheet(title, header).get_all_values()


class SheetsBackend:
    def _guests_ws(self):
        return _worksheet(GUESTS_SHEET, tuple(GUESTS_HEADER))

    def _wishes_ws(self):
        return _worksheet(WISHES_SHEET, tuple(WISHES_HEADER))

    @staticmethod
    def _parse_guests(rows: list) -> dict:
        return {r[0]: (r[1] if len(r) > 1 else "") for r in rows[1:] if r and r[0]}

    @staticmethod
    def _parse_signups(rows: list) -> dict:
        result: dict[str, list[str]] = {}
        for r in rows[1:]:
            if len(r) >= 3 and r[0] and r[2]:
                result.setdefault(r[0], []).append(r[2])
        return result

    def guests(self) -> dict:
        return self._parse_guests(_cached_rows(GUESTS_SHEET, tuple(GUESTS_HEADER)))

    def add_guest(self, name: str, title: str, task: str = "") -> None:
        ws = self._guests_ws()
        if name not in self._parse_guests(ws.get_all_values()):
            ws.append_row([name, title, _now(), task], value_input_option="RAW")
            _cached_rows.clear()

    def signups(self) -> dict:
        return self._parse_signups(_cached_rows(WISHES_SHEET, tuple(WISHES_HEADER)))

    def add_signup(self, item_id: str, item_title: str, name: str) -> None:
        ws = self._wishes_ws()
        if name not in self._parse_signups(ws.get_all_values()).get(item_id, []):
            ws.append_row([item_id, item_title, name, _now()], value_input_option="RAW")
        _cached_rows.clear()

    def remove_signup(self, item_id: str, name: str) -> None:
        ws = self._wishes_ws()
        rows = ws.get_all_values()
        # delete bottom-up so row indices stay valid
        for idx in range(len(rows), 1, -1):
            r = rows[idx - 1]
            if len(r) >= 3 and r[0] == item_id and r[2] == name:
                ws.delete_rows(idx)
        _cached_rows.clear()


# ---------------------------------------------------------------- local JSON
class LocalBackend:
    path = Path(__file__).parent / "data" / "registry.json"
    _lock = threading.Lock()

    def _load(self) -> dict:
        if not self.path.exists():
            return {"guests": {}, "wishlist": {}}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        data.setdefault("guests", {})
        data.setdefault("wishlist", {})
        return data

    def _update(self, fn) -> None:
        with self._lock:
            data = self._load()
            fn(data)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.path)

    def guests(self) -> dict:
        return self._load()["guests"]

    def add_guest(self, name: str, title: str, task: str = "") -> None:
        self._update(lambda d: d["guests"].setdefault(name, title))

    def signups(self) -> dict:
        return self._load()["wishlist"]

    def add_signup(self, item_id: str, item_title: str, name: str) -> None:
        def apply(d):
            names = d["wishlist"].setdefault(item_id, [])
            if name not in names:
                names.append(name)

        self._update(apply)

    def remove_signup(self, item_id: str, name: str) -> None:
        def apply(d):
            names = d["wishlist"].get(item_id, [])
            if name in names:
                names.remove(name)

        self._update(apply)


def backend():
    return SheetsBackend() if _has_sheet_secrets() else LocalBackend()


def using_sheets() -> bool:
    return _has_sheet_secrets()
