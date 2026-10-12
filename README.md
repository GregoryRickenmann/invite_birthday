# Arcanum · Gregorius XXIII

Mysteriöse römische Geburtstagseinladung als Streamlit-App.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Gäste geben zuerst ihren Namen ein (Gästeliste), danach sehen sie die Einladung
und können sich bei der Wunschliste einschreiben bzw. fürs Zusammenlegen eintragen.
Alle Einträge werden in `data/registry.json` gespeichert.

> Hinweis: Auf Streamlit Community Cloud ist das Dateisystem nicht dauerhaft —
> bei einem Neustart der App gehen Einträge verloren. Für den Ernstfall eine
> kleine Datenbank (z. B. Google Sheet oder Supabase) anbinden.
