# Arcanum – Gregorius XXIII

Mysteriöse römische Geburtstagseinladung als Streamlit-App.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Gäste geben zuerst ihren Namen ein, danach sehen sie die Einladung, einen
Countdown in römischen Ziffern, das Orakel (persönliche Rolle für die Nacht)
und die Wunschliste zum Einschreiben bzw. Zusammenlegen.

## Speicherung: Google Sheet

Ohne Secrets speichert die App lokal in `data/registry.json` (nur zum Testen).
Für die geteilte Version auf Streamlit Cloud ein Google Sheet anbinden:

1. **Google Cloud:** Auf <https://console.cloud.google.com> ein Projekt anlegen
   und unter «APIs & Dienste» die **Google Sheets API** aktivieren.
2. **Service Account:** «IAM & Verwaltung» → «Dienstkonten» → Dienstkonto
   erstellen (keine Rollen nötig) → beim Konto «Schlüssel» → «Schlüssel
   hinzufügen» → **JSON**. Die Datei wird heruntergeladen.
3. **Sheet:** Ein leeres Google Sheet erstellen und über «Freigeben» mit der
   `client_email` aus der JSON-Datei als **Bearbeiter** teilen.
4. **Secrets:** In Streamlit Cloud bei der App → «Settings» → «Secrets» den
   Inhalt von `.streamlit/secrets.toml.example` einfügen, die Sheet-URL und
   die Werte aus der JSON-Datei eintragen. Speichern – die App startet neu.

Die App legt die Tabellenblätter **Gaeste** und **Wunschliste** selbst an.
Dort siehst du jederzeit, wer das Siegel gebrochen hat und wer sich wofür
eingeschrieben hat.

## Deploy auf Streamlit Cloud

share.streamlit.io → «Create app» → Repo `GregoryRickenmann/invite_birthday`,
Branch wählen, Main file `app.py` → Deploy. Danach unter «Settings» →
«Sharing» die App auf öffentlich stellen, damit Gäste ohne Login zugreifen können.
