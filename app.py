"""Invitatio — Gregorius XXIII. A Roman birthday invitation in Streamlit."""

import json
import threading
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_FILE = Path(__file__).parent / "data" / "registry.json"
_LOCK = threading.Lock()

WISHLIST = [
    {
        "id": "liber",
        "numeral": "I",
        "title": "Liber",
        "subtitle": "Ein Buch von Orell Füssli",
        "url": "https://www.orellfuessli.ch/shop/home/artikeldetails/A1000104687",
        "shared": False,
    },
    {
        "id": "trench",
        "numeral": "II",
        "title": "Paenula Britannica",
        "subtitle": "Burberry Trench Coat — zum Zusammenlegen",
        "url": "https://www.ricardo.ch/de/a/magnifique-trench-coat-burberry-1312507844/",
        "shared": True,
    },
    {
        "id": "case",
        "numeral": "III",
        "title": "Theca Coriacea",
        "subtitle": "Leder-Hülle für das iPhone 17",
        "url": None,
        "shared": False,
    },
    {
        "id": "fendi",
        "numeral": "IV",
        "title": "Pera Fendiana",
        "subtitle": "Fendi Pochette aus FF-Jacquard in Braun — zum Zusammenlegen",
        "url": "https://www.fendi.com/at-de/herren/taschen/flache-pochette-mittlerer-gro%C3%9Fe-aus-ff-jacquard-pochette-aus-stoff-in-braun-7n0134afbvf1hrm",
        "shared": True,
    },
    {
        "id": "parma",
        "numeral": "V",
        "title": "Unguentum Parmense",
        "subtitle": "Ein Duft von Acqua di Parma",
        "url": None,
        "shared": False,
    },
]


# ---------------------------------------------------------------- storage
def load_registry() -> dict:
    if not DATA_FILE.exists():
        return {"guests": {}, "wishlist": {item["id"]: [] for item in WISHLIST}}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for item in WISHLIST:
        data.setdefault("wishlist", {}).setdefault(item["id"], [])
    data.setdefault("guests", {})
    return data


def save_registry(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DATA_FILE)


def update_registry(fn) -> dict:
    with _LOCK:
        data = load_registry()
        fn(data)
        save_registry(data)
        return data


# ---------------------------------------------------------------- styling
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;600&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

:root {
  --gold: #c9a24b;
  --gold-dim: #8a6d2c;
  --blood: #7a1414;
  --ink: #0b0806;
  --parchment: #e9dcc0;
}

.stApp {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(122,20,20,0.35) 0%, transparent 55%),
    radial-gradient(ellipse at 50% 100%, rgba(201,162,75,0.08) 0%, transparent 60%),
    repeating-linear-gradient(90deg, rgba(255,255,255,0.012) 0 2px, transparent 2px 120px),
    var(--ink);
  color: var(--parchment);
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container { max-width: 760px; padding-top: 3rem; }

html, body, p, li, label, .stMarkdown { font-family: 'Cormorant Garamond', serif !important; }
p, li { font-size: 1.2rem; line-height: 1.6; color: var(--parchment); }

.spqr {
  font-family: 'Cinzel Decorative', serif; letter-spacing: 0.6em;
  color: var(--gold-dim); text-align: center; font-size: 0.95rem; margin-bottom: 0.4rem;
}
.title {
  font-family: 'Cinzel Decorative', serif; font-weight: 700;
  text-align: center; font-size: clamp(2.4rem, 8vw, 4.4rem); line-height: 1.05;
  background: linear-gradient(180deg, #f3dc9a 0%, var(--gold) 45%, #6e5420 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  text-shadow: 0 0 40px rgba(201,162,75,0.15);
  animation: glow 6s ease-in-out infinite;
}
@keyframes glow { 50% { filter: drop-shadow(0 0 14px rgba(201,162,75,0.35)); } }

.subtitle {
  font-family: 'Cinzel', serif; text-align: center; letter-spacing: 0.35em;
  color: var(--gold); font-size: 1rem; margin-top: 0.4rem;
}
.whisper {
  font-style: italic; text-align: center; color: rgba(233,220,192,0.6);
  font-size: 1.15rem; margin: 1.6rem auto; max-width: 520px;
}
.divider {
  text-align: center; color: var(--gold-dim); letter-spacing: 1em;
  margin: 2.2rem 0; font-size: 1rem;
}
.section {
  font-family: 'Cinzel', serif; color: var(--gold); text-align: center;
  letter-spacing: 0.3em; font-size: 1.35rem; margin-bottom: 0.2rem;
}
.section-sub {
  text-align: center; font-style: italic; color: rgba(233,220,192,0.55);
  margin-bottom: 1.4rem;
}
.tablet {
  border: 1px solid var(--gold-dim); outline: 1px solid rgba(201,162,75,0.25);
  outline-offset: 6px; padding: 1.8rem 1.6rem; margin: 1rem 0 1.6rem;
  background: linear-gradient(180deg, rgba(201,162,75,0.05), rgba(0,0,0,0.25));
}
.facts { display: grid; grid-template-columns: 1fr 1fr; gap: 1.4rem 1rem; }
@media (max-width: 560px) { .facts { grid-template-columns: 1fr; } }
.fact-k {
  font-family: 'Cinzel', serif; color: var(--gold-dim);
  letter-spacing: 0.3em; font-size: 0.8rem;
}
.fact-v { font-family: 'Cinzel', serif; color: var(--parchment); font-size: 1.15rem; }
.fact-s { font-style: italic; color: rgba(233,220,192,0.55); font-size: 1rem; }

.greeting {
  font-family: 'Cinzel', serif; text-align: center; color: var(--parchment);
  font-size: 1.3rem; letter-spacing: 0.1em;
}
.greeting b { color: var(--gold); }

.disclaimer {
  text-align: center; font-style: italic; border-top: 1px solid rgba(201,162,75,0.2);
  border-bottom: 1px solid rgba(201,162,75,0.2); padding: 1rem 0.5rem; margin-bottom: 1.6rem;
}
.disclaimer .latin {
  font-family: 'Cinzel', serif; font-style: normal; color: var(--gold);
  letter-spacing: 0.15em; display: block; margin-bottom: 0.4rem;
}

.item-num { font-family: 'Cinzel Decorative', serif; color: var(--gold); font-size: 1.8rem; }
.item-title { font-family: 'Cinzel', serif; color: var(--parchment); font-size: 1.25rem; letter-spacing: 0.08em; }
.item-sub { font-style: italic; color: rgba(233,220,192,0.6); }
.item-badge {
  display: inline-block; font-family: 'Cinzel', serif; font-size: 0.7rem; letter-spacing: 0.2em;
  border: 1px solid var(--blood); color: #d98b8b; padding: 0.1rem 0.5rem; margin-top: 0.3rem;
}
.item-names { font-style: italic; color: var(--gold); font-size: 1.05rem; }
.item-names.empty { color: rgba(233,220,192,0.4); }
.item-link a { color: var(--gold) !important; font-family: 'Cinzel', serif; font-size: 0.85rem; letter-spacing: 0.15em; }

/* inputs & buttons */
.stTextInput div[data-baseweb="input"], .stTextInput div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }
.stTextInput input {
  background: rgba(0,0,0,0.5) !important; color: var(--parchment) !important;
  border: 1px solid var(--gold-dim) !important; border-radius: 0 !important;
  font-family: 'Cinzel', serif !important; text-align: center; letter-spacing: 0.15em;
  font-size: 1.1rem !important;
}
.stTextInput label p { font-family: 'Cinzel', serif !important; color: var(--gold-dim) !important; letter-spacing: 0.25em; font-size: 0.85rem !important; }
.stButton button, .stFormSubmitButton button {
  background: transparent !important; color: var(--gold) !important;
  border: 1px solid var(--gold) !important; border-radius: 0 !important;
  font-family: 'Cinzel', serif !important; letter-spacing: 0.25em; transition: all .3s ease;
}
.stButton button:hover, .stFormSubmitButton button:hover {
  background: var(--gold) !important; color: var(--ink) !important;
  box-shadow: 0 0 24px rgba(201,162,75,0.35);
}
[data-testid="stForm"] { border: none; padding: 0; }
.seal {
  text-align: center; font-family: 'Cinzel Decorative', serif; color: var(--blood);
  font-size: 3.4rem; line-height: 1; margin: 1rem 0;
  text-shadow: 0 0 20px rgba(122,20,20,0.6);
}
.footer {
  text-align: center; font-family: 'Cinzel', serif; color: var(--gold-dim);
  letter-spacing: 0.4em; font-size: 0.8rem; margin: 3rem 0 1rem;
}
.fade { animation: fadein 1.6s ease both; }
@keyframes fadein { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
</style>
"""

DIVIDER = '<div class="divider">✦ ✦ ✦</div>'


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


# ---------------------------------------------------------------- gate
def render_gate() -> None:
    html('<div class="spqr">S · P · Q · R</div>')
    html('<div class="seal">⚜</div>')
    html('<div class="title">Arcanum</div>')
    html(
        '<div class="whisper">Ein Siegel liegt auf dieser Botschaft.<br>'
        "Nur wer seinen Namen nennt, darf sie brechen.</div>"
    )
    html('<div class="section">Quis es?</div>')
    html('<div class="section-sub">Wer bist du, Fremder?</div>')

    with st.form("gate", clear_on_submit=False):
        name = st.text_input("NOMEN TUUM", placeholder="Dein Name", label_visibility="visible")
        submitted = st.form_submit_button("Sigillum frangere", use_container_width=True)

    if submitted:
        name = " ".join(name.split())
        if len(name) < 2:
            st.error("Die Götter verlangen einen echten Namen.")
            return

        def register(data):
            data["guests"].setdefault(name, datetime.now().isoformat(timespec="minutes"))

        update_registry(register)
        st.session_state.guest = name
        st.rerun()

    html('<div class="footer">ALEA IACTA EST</div>')


# ---------------------------------------------------------------- invitation
def render_invitation(guest: str) -> None:
    html('<div class="spqr">S · P · Q · R</div>')
    html(f'<div class="greeting fade">Salve, <b>{escape(guest)}</b>.</div>')
    html('<div class="whisper">Du wurdest gerufen. Das Siegel ist gebrochen.</div>')
    html('<div class="title fade">Gregorius<br>XXIII</div>')
    html('<div class="subtitle">ANNOS · VIGINTI · TRES · CELEBRAT</div>')

    html(DIVIDER)

    html(
        '<div class="whisper">Wenn die Sonne versinkt und die Fackeln entzündet werden, '
        "versammelt sich der Senat. Was in jener Nacht geschieht, bleibt hinter den "
        "Mauern der Villa.</div>"
    )

    html(
        """
<div class="tablet">
  <div class="facts">
    <div>
      <div class="fact-k">DIES</div>
      <div class="fact-v">XXVIII · XI · MMXXVI</div>
      <div class="fact-s">Samstag, 28. November 2026</div>
    </div>
    <div>
      <div class="fact-k">HORA</div>
      <div class="fact-v">Hora XIX</div>
      <div class="fact-s">19.00 Uhr — sei pünktlich</div>
    </div>
    <div>
      <div class="fact-k">LOCUS</div>
      <div class="fact-v">Grundwiesstrasse 7</div>
      <div class="fact-s">8700 Küsnacht</div>
    </div>
    <div>
      <div class="fact-k">VESTIS</div>
      <div class="fact-v">Toga vel Romana</div>
      <div class="fact-s">Toga oder römisch gekleidet</div>
    </div>
  </div>
</div>
"""
    )

    html(
        '<div class="whisper"><b style="font-family:Cinzel,serif;font-style:normal;'
        'color:var(--gold);letter-spacing:.15em">IN VINO VERITAS</b><br>'
        "Wein wird fliessen, ein Festmahl wird gereicht.<br>Komm hungrig. Komm durstig.</div>"
    )
    st.link_button(
        "Iter ad Villam — Route",
        "https://www.google.com/maps/search/?api=1&query=Grundwiesstrasse+7,+8700+K%C3%BCsnacht",
        use_container_width=True,
    )

    html(DIVIDER)
    render_wishlist(guest)

    html(DIVIDER)
    html(
        '<div class="whisper">Erzähle niemandem mehr, als nötig ist.<br>'
        "Wir sehen uns im Schein der Fackeln.</div>"
    )
    html('<div class="footer">AVE · GREGORIUS · XXIII</div>')

    if st.button("Nicht du? · Abmelden", type="tertiary"):
        st.session_state.pop("guest", None)
        st.rerun()


def render_wishlist(guest: str) -> None:
    html('<div class="section">Dona</div>')
    html('<div class="section-sub">Die Wunschliste</div>')
    html(
        '<div class="disclaimer"><span class="latin">PRAESENTIA TUA DONUM SATIS EST</span>'
        "Du musst mir nichts schenken — deine Anwesenheit ist Geschenk genug.<br>"
        "Wer dennoch etwas beitragen möchte, kann sich unten einschreiben. "
        "Bei den grossen Stücken legen wir zusammen.</div>"
    )

    data = load_registry()
    for item in WISHLIST:
        names = data["wishlist"].get(item["id"], [])
        joined = guest in names

        with st.container(border=True):
            col_num, col_body = st.columns([1, 6], vertical_alignment="center")
            with col_num:
                html(f'<div class="item-num">{item["numeral"]}</div>')
            with col_body:
                html(f'<div class="item-title">{item["title"]}</div>')
                html(f'<div class="item-sub">{item["subtitle"]}</div>')
                if item["shared"]:
                    html('<span class="item-badge">COLLATIO · ZUSAMMENLEGEN</span>')
                if item["url"]:
                    html(f'<div class="item-link"><a href="{item["url"]}" target="_blank">ANSEHEN →</a></div>')

            if names:
                label = "Eingeschrieben" if item["shared"] else "Reserviert von"
                html(f'<div class="item-names">{label}: {escape(", ".join(names))}</div>')
            else:
                html('<div class="item-names empty">Noch niemand hat sich eingeschrieben.</div>')

            if joined:
                if st.button("Austragen", key=f"leave-{item['id']}", use_container_width=True):
                    toggle_signup(item["id"], guest, join=False)
            else:
                text = "Mich einschreiben" if item["shared"] else "Ich übernehme das"
                if st.button(text, key=f"join-{item['id']}", use_container_width=True):
                    toggle_signup(item["id"], guest, join=True)


def toggle_signup(item_id: str, guest: str, join: bool) -> None:
    def apply(data):
        names = data["wishlist"].setdefault(item_id, [])
        if join and guest not in names:
            names.append(guest)
        elif not join and guest in names:
            names.remove(guest)

    update_registry(apply)
    st.rerun()


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


# ---------------------------------------------------------------- main
def main() -> None:
    st.set_page_config(page_title="Arcanum · XXVIII·XI", page_icon="🏛️", layout="centered")
    html(CSS)
    guest = st.session_state.get("guest")
    if guest:
        render_invitation(guest)
    else:
        render_gate()


if __name__ == "__main__":
    main()
