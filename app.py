"""Invitatio — Gregorius XXIII. A Roman birthday invitation in Streamlit."""

import hashlib
import html as html_lib

import streamlit as st
import streamlit.components.v1 as components

import storage

EVENT_ISO = "2026-11-28T19:00:00+01:00"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=Grundwiesstrasse+7,+8700+K%C3%BCsnacht"

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
        "subtitle": "Burberry Trench Coat, zum Zusammenlegen",
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
        "subtitle": "Fendi Pochette aus FF-Jacquard in Braun, zum Zusammenlegen",
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

# Oraculum: every guest is assigned a fixed role and omen, derived from their name.
TITULI = [
    ("Custos Vini", "Hüter des Weins"),
    ("Augur Noctis", "Seher der Nacht"),
    ("Haruspex", "Deuter der Zeichen"),
    ("Tribunus Convivii", "Tribun des Gelages"),
    ("Praefectus Saltationis", "Präfekt des Tanzes"),
    ("Poeta Laureatus", "Lorbeergekrönter Dichter"),
    ("Legatus Risus", "Gesandter des Gelächters"),
    ("Quaestor Poculorum", "Verwalter der Becher"),
    ("Magister Epularum", "Meister des Festmahls"),
    ("Consul Noctis", "Konsul der Nacht"),
    ("Gladiator Honoris", "Gladiator der Ehre"),
    ("Senator Arcanus", "Geheimer Senator"),
    ("Orator Maximus", "Grösster Redner"),
    ("Speculator", "Späher im Schatten"),
    ("Pontifex Festi", "Hohepriester des Festes"),
    ("Centurio Cantus", "Zenturio des Gesangs"),
]

OMINA = [
    ("Fortes fortuna adiuvat.", "Den Mutigen hilft das Glück. Heute Nacht wirst du mutig sein."),
    ("Carpe noctem.", "Nutze die Nacht. Sie gehört dir mehr, als du ahnst."),
    ("Veritas in calice latet.", "Die Wahrheit verbirgt sich im Becher. Trinke weise."),
    ("Nemo saltat sobrius.", "Niemand tanzt nüchtern. Die Götter zählen auf dich."),
    ("Omnia vincit amicitia.", "Freundschaft besiegt alles, auch den Morgen danach."),
    ("Audentes deus ipse iuvat.", "Den Wagemutigen hilft der Gott selbst. Wage einen Toast."),
    ("Tacita sunt quae fient.", "Was geschehen wird, bleibt verschwiegen."),
    ("Signum in umbra videbis.", "Du wirst ein Zeichen im Schatten sehen. Achte darauf."),
    ("Lupa tecum ambulat.", "Die Wölfin wacht über dich. Fürchte nichts."),
    ("Ultimus discedes.", "Du wirst als Letzter gehen. So steht es geschrieben."),
]


def to_roman(n: int) -> str:
    if n <= 0:
        return "N"
    out = ""
    for value, sym in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                       (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= value:
            out += sym
            n -= value
    return out


def oraculum(name: str) -> dict:
    digest = hashlib.sha256(name.strip().lower().encode()).digest()
    titulus = TITULI[digest[0] % len(TITULI)]
    omen = OMINA[digest[1] % len(OMINA)]
    numerus = digest[2] % 99 + 1
    return {"titulus": titulus, "omen": omen, "numerus": numerus}


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
    var(--ink);
  color: var(--parchment);
}
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }

.block-container { max-width: 720px; padding: 3rem 1.5rem 2rem; }
@media (max-width: 640px) { .block-container { padding: 1.6rem 1rem 1.5rem; } }

html, body, p, li, label, .stMarkdown { font-family: 'Cormorant Garamond', serif !important; }
p, li { font-size: 1.2rem; line-height: 1.6; color: var(--parchment); }
a { color: var(--gold) !important; }

/* wax seal */
.seal {
  width: 112px; height: 112px; margin: 0.5rem auto 1.2rem; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #a52222 0%, #6d1010 55%, #3d0707 100%);
  box-shadow: 0 0 0 5px rgba(109,16,16,0.55), 0 0 40px rgba(122,20,20,0.6), inset 0 -6px 14px rgba(0,0,0,0.5);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  animation: pulse 4s ease-in-out infinite;
}
.seal .g { font-family: 'Cinzel Decorative', serif; font-weight: 700; color: #e8b8a0; font-size: 2.6rem; line-height: 1; text-shadow: 0 2px 2px rgba(0,0,0,0.5); }
.seal .n { font-family: 'Cinzel', serif; color: #d79a86; font-size: 0.75rem; letter-spacing: 0.3em; margin-top: 2px; }
@keyframes pulse { 50% { box-shadow: 0 0 0 5px rgba(109,16,16,0.55), 0 0 70px rgba(160,30,30,0.75), inset 0 -6px 14px rgba(0,0,0,0.5); } }

.title {
  font-family: 'Cinzel Decorative', serif; font-weight: 700;
  text-align: center; font-size: clamp(2.3rem, 11vw, 4.4rem); line-height: 1.05;
  background: linear-gradient(180deg, #f3dc9a 0%, var(--gold) 45%, #6e5420 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: glow 6s ease-in-out infinite; word-break: break-word;
}
@keyframes glow { 50% { filter: drop-shadow(0 0 14px rgba(201,162,75,0.35)); } }

.subtitle {
  font-family: 'Cinzel', serif; text-align: center; letter-spacing: 0.3em;
  color: var(--gold); font-size: clamp(0.75rem, 3.4vw, 1rem); margin-top: 0.5rem;
}
.whisper {
  font-style: italic; text-align: center; color: rgba(233,220,192,0.65);
  font-size: 1.15rem; margin: 1.4rem auto; max-width: 520px;
}
.rule {
  height: 1px; margin: 2.4rem auto; width: 70%;
  background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
}
.section {
  font-family: 'Cinzel', serif; color: var(--gold); text-align: center;
  letter-spacing: 0.3em; font-size: 1.35rem; margin-bottom: 0.2rem;
}
.section-sub {
  text-align: center; font-style: italic; color: rgba(233,220,192,0.55);
  margin-bottom: 1.2rem;
}
.tablet {
  border: 1px solid var(--gold-dim); outline: 1px solid rgba(201,162,75,0.25);
  outline-offset: 5px; padding: 1.6rem 1.4rem; margin: 1rem 6px 1.6rem;
  background: linear-gradient(180deg, rgba(201,162,75,0.05), rgba(0,0,0,0.25));
}
.facts { display: grid; grid-template-columns: 1fr 1fr; gap: 1.4rem 1rem; }
@media (max-width: 560px) {
  .facts { grid-template-columns: 1fr; text-align: center; }
  .tablet { padding: 1.3rem 1rem; }
}
.fact-k { font-family: 'Cinzel', serif; color: var(--gold-dim); letter-spacing: 0.3em; font-size: 0.8rem; }
.fact-v { font-family: 'Cinzel', serif; color: var(--parchment); font-size: 1.15rem; }
.fact-s { font-style: italic; color: rgba(233,220,192,0.6); font-size: 1rem; }

.greeting {
  font-family: 'Cinzel', serif; text-align: center; color: var(--parchment);
  font-size: 1.3rem; letter-spacing: 0.08em; margin-bottom: 0.4rem;
}
.greeting b { color: var(--gold); }

/* gold button / link */
.btn-gold, .stButton button, .stFormSubmitButton button {
  display: block; width: 100%; text-align: center; box-sizing: border-box;
  background: transparent !important; color: var(--gold) !important;
  border: 1px solid var(--gold) !important; border-radius: 0 !important;
  font-family: 'Cinzel', serif !important; letter-spacing: 0.22em;
  padding: 0.7rem 0.8rem; font-size: 0.95rem; text-decoration: none !important;
  transition: all .3s ease;
}
.btn-gold:hover, .stButton button:hover, .stFormSubmitButton button:hover {
  background: var(--gold) !important; color: var(--ink) !important;
  box-shadow: 0 0 24px rgba(201,162,75,0.35);
}
.stButton button p, .stFormSubmitButton button p { font-family: 'Cinzel', serif !important; font-size: 0.95rem; }
.stButton button[kind="tertiary"], .stButton button[kind="tertiary"] p {
  border: none !important; color: rgba(233,220,192,0.4) !important; letter-spacing: 0.1em;
}
.stButton button[kind="tertiary"]:hover { background: transparent !important; color: var(--gold) !important; box-shadow: none; }

/* oracle */
.oracle {
  text-align: center; padding: 1.6rem 1rem; margin: 0.6rem 0 0.4rem;
  border: 1px solid rgba(122,20,20,0.7);
  background: radial-gradient(ellipse at 50% 0%, rgba(122,20,20,0.25), transparent 70%);
  animation: reveal 1.4s ease both;
}
.oracle .k { font-family: 'Cinzel', serif; color: var(--gold-dim); letter-spacing: 0.3em; font-size: 0.75rem; }
.oracle .t { font-family: 'Cinzel Decorative', serif; color: var(--gold); font-size: clamp(1.4rem, 6vw, 2rem); margin: 0.2rem 0; }
.oracle .tde { font-style: italic; color: rgba(233,220,192,0.65); margin-bottom: 1rem; }
.oracle .la { font-family: 'Cinzel', serif; color: var(--parchment); font-size: 1.1rem; letter-spacing: 0.06em; }
.oracle .de { font-style: italic; color: rgba(233,220,192,0.7); margin-top: 0.3rem; }
.oracle .num { font-family: 'Cinzel', serif; color: #d98b8b; margin-top: 1rem; letter-spacing: 0.2em; font-size: 0.9rem; }
@keyframes reveal { from { opacity: 0; filter: blur(8px); transform: scale(0.97); } to { opacity: 1; filter: none; transform: none; } }

/* wishlist */
.disclaimer {
  text-align: center; font-style: italic; border-top: 1px solid rgba(201,162,75,0.2);
  border-bottom: 1px solid rgba(201,162,75,0.2); padding: 1rem 0.5rem; margin-bottom: 1.4rem;
}
.disclaimer .latin {
  font-family: 'Cinzel', serif; font-style: normal; color: var(--gold);
  letter-spacing: 0.12em; display: block; margin-bottom: 0.4rem;
}
.item { display: flex; gap: 1rem; align-items: flex-start; }
.item-num { font-family: 'Cinzel Decorative', serif; color: var(--gold); font-size: 1.7rem; min-width: 2.6rem; line-height: 1.2; }
.item-body { flex: 1; min-width: 0; }
.item-title { font-family: 'Cinzel', serif; color: var(--parchment); font-size: 1.2rem; letter-spacing: 0.06em; }
.item-sub { font-style: italic; color: rgba(233,220,192,0.6); }
.item-badge {
  display: inline-block; font-family: 'Cinzel', serif; font-size: 0.68rem; letter-spacing: 0.18em;
  border: 1px solid var(--blood); color: #d98b8b; padding: 0.1rem 0.5rem; margin: 0.3rem 0;
}
.item-link a { font-family: 'Cinzel', serif; font-size: 0.82rem; letter-spacing: 0.15em; }
.item-names { font-style: italic; color: var(--gold); font-size: 1.05rem; margin: 0.4rem 0 0.2rem; }
.item-names.empty { color: rgba(233,220,192,0.4); }
[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(201,162,75,0.25) !important; border-radius: 0 !important; }

/* inputs */
.stTextInput div[data-baseweb="input"], .stTextInput div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }
.stTextInput input {
  background: rgba(0,0,0,0.5) !important; color: var(--parchment) !important;
  border: 1px solid var(--gold-dim) !important; border-radius: 0 !important;
  font-family: 'Cinzel', serif !important; text-align: center; letter-spacing: 0.12em;
  font-size: 1.1rem !important; padding: 0.8rem !important;
}
.stTextInput label p { font-family: 'Cinzel', serif !important; color: var(--gold-dim) !important; letter-spacing: 0.25em; font-size: 0.85rem !important; }
[data-testid="stForm"] { border: none; padding: 0; }

.census {
  text-align: center; font-family: 'Cinzel', serif; color: rgba(233,220,192,0.55);
  letter-spacing: 0.15em; font-size: 0.85rem;
}
.census b { color: var(--gold); font-weight: 400; }
.footer {
  text-align: center; font-family: 'Cinzel', serif; color: var(--gold-dim);
  letter-spacing: 0.4em; font-size: 0.8rem; margin: 2.6rem 0 0.6rem;
}
.fade { animation: fadein 1.6s ease both; }
@keyframes fadein { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
</style>
"""

RULE = '<div class="rule"></div>'
SEAL = '<div class="seal"><span class="g">G</span><span class="n">XXIII</span></div>'

COUNTDOWN_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<style>
  html, body { margin: 0; background: transparent; }
  .wrap { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; font-family: 'Cinzel', serif; }
  .u { flex: 1 1 0; min-width: 64px; max-width: 150px; text-align: center; padding: 10px 4px;
       border: 1px solid rgba(201,162,75,0.35); background: rgba(0,0,0,0.3); }
  .v { color: #c9a24b; font-size: clamp(15px, 4.6vw, 22px); letter-spacing: 1px; min-height: 28px; }
  .l { color: #8a6d2c; font-size: 10px; letter-spacing: 3px; margin-top: 4px; }
  .done { color: #c9a24b; text-align: center; font-family: 'Cinzel', serif; letter-spacing: 4px; padding: 18px; }
</style>
<div id="c" class="wrap"></div>
<script>
  const target = new Date("__EVENT__").getTime();
  const R = [[1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],[100,"C"],[90,"XC"],[50,"L"],[40,"XL"],[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]];
  const roman = n => { if (n <= 0) return "N"; let s = ""; for (const [v, r] of R) while (n >= v) { s += r; n -= v; } return s; };
  const el = document.getElementById("c");
  function tick() {
    let d = Math.floor((target - Date.now()) / 1000);
    if (d <= 0) { el.outerHTML = '<div class="done">ALEA IACTA EST</div>'; return; }
    const parts = [[Math.floor(d / 86400), "DIES"], [Math.floor(d % 86400 / 3600), "HORAE"],
                   [Math.floor(d % 3600 / 60), "MINUTA"], [d % 60, "SECUNDA"]];
    el.innerHTML = parts.map(([v, l]) => `<div class="u"><div class="v">${roman(v)}</div><div class="l">${l}</div></div>`).join("");
  }
  tick(); setInterval(tick, 1000);
</script>
""".replace("__EVENT__", EVENT_ISO)


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def esc(text: str) -> str:
    return html_lib.escape(text, quote=True)


# ---------------------------------------------------------------- gate
def render_gate(db) -> None:
    html(SEAL)
    html('<div class="title">Arcanum</div>')
    html(
        '<div class="whisper">Ein Siegel liegt auf dieser Botschaft.<br>'
        "Nur wer seinen Namen nennt, darf sie brechen.</div>"
    )
    html('<div class="section">Quis es?</div>')
    html('<div class="section-sub">Wer bist du, Fremder?</div>')

    with st.form("gate", clear_on_submit=False):
        name = st.text_input("NOMEN TUUM", placeholder="Dein Name")
        submitted = st.form_submit_button("Sigillum frangere", use_container_width=True)

    if submitted:
        name = " ".join(name.split())
        if len(name) < 2:
            st.error("Die Götter verlangen einen echten Namen.")
            return
        with st.spinner("Das Siegel bricht ..."):
            db.add_guest(name, oraculum(name)["titulus"][0])
        st.session_state.guest = name
        st.rerun()

    html('<div class="footer">ALEA IACTA EST</div>')


# ---------------------------------------------------------------- invitation
def render_invitation(db, guest: str) -> None:
    html(SEAL)
    html(f'<div class="greeting fade">Salve, <b>{esc(guest)}</b>.</div>')
    html('<div class="whisper" style="margin-top:0.2rem">Du wurdest gerufen. Das Siegel ist gebrochen.</div>')
    html('<div class="title fade">Gregorius<br>XXIII</div>')
    html('<div class="subtitle">Annos viginti tres celebrat</div>')

    html(RULE)
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
      <div class="fact-v">XXVIII XI MMXXVI</div>
      <div class="fact-s">Samstag, 28. November 2026</div>
    </div>
    <div>
      <div class="fact-k">HORA</div>
      <div class="fact-v">Hora XIX</div>
      <div class="fact-s">19.00 Uhr, sei pünktlich</div>
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
    html(f'<a class="btn-gold" href="{MAPS_URL}" target="_blank" rel="noopener">Iter ad Villam</a>')

    html('<div class="section" style="margin-top:2.2rem">Tempus fugit</div>')
    html('<div class="section-sub">Bis die Tore sich öffnen</div>')
    components.html(COUNTDOWN_HTML, height=80)

    html(
        '<div class="whisper"><span style="font-family:Cinzel,serif;font-style:normal;'
        'color:var(--gold);letter-spacing:.15em">IN VINO VERITAS</span><br>'
        "Wein wird fliessen, ein Festmahl wird gereicht.<br>Komm hungrig. Komm durstig.</div>"
    )

    html(RULE)
    render_oracle(guest)

    html(RULE)
    render_wishlist(db, guest)

    html(RULE)
    count = len(db.guests())
    if count:
        html(f'<div class="census">Siegel bereits gebrochen: <b>{to_roman(count)}</b></div>')
    html(
        '<div class="whisper">Erzähle niemandem mehr, als nötig ist.<br>'
        "Wir sehen uns im Schein der Fackeln.</div>"
    )
    html('<div class="footer">AVE GREGORIUS</div>')

    if st.button("Nicht du? Abmelden", type="tertiary", use_container_width=True):
        st.session_state.clear()
        st.rerun()


def render_oracle(guest: str) -> None:
    html('<div class="section">Oraculum</div>')
    html('<div class="section-sub">Die Götter haben dir für diese Nacht eine Rolle bestimmt</div>')

    if not st.session_state.get("oracle_open"):
        if st.button("Das Orakel befragen", use_container_width=True):
            st.session_state.oracle_open = True
            st.rerun()
        return

    o = oraculum(guest)
    (t_la, t_de), (om_la, om_de) = o["titulus"], o["omen"]
    html(
        f"""
<div class="oracle">
  <div class="k">TITULUS TUUS</div>
  <div class="t">{t_la}</div>
  <div class="tde">{t_de}</div>
  <div class="la">«{om_la}»</div>
  <div class="de">{om_de}</div>
  <div class="num">NUMERUS FATALIS {to_roman(o["numerus"])}</div>
</div>
<div class="section-sub" style="margin-top:0.6rem;font-size:1rem">
  Erscheine als {t_la}. Niemand sonst muss es wissen.
</div>
"""
    )


def render_wishlist(db, guest: str) -> None:
    html('<div class="section">Dona</div>')
    html('<div class="section-sub">Die Wunschliste</div>')
    html(
        '<div class="disclaimer"><span class="latin">Praesentia tua donum satis est</span>'
        "Du musst mir nichts schenken. Deine Anwesenheit ist Geschenk genug.<br>"
        "Wer dennoch etwas beitragen möchte, kann sich unten einschreiben. "
        "Bei den grossen Stücken legen wir zusammen.</div>"
    )

    signups = db.signups()
    for item in WISHLIST:
        names = signups.get(item["id"], [])
        badge = '<div><span class="item-badge">COLLATIO</span></div>' if item["shared"] else ""
        link = (
            f'<div class="item-link"><a href="{item["url"]}" target="_blank" rel="noopener">Ansehen</a></div>'
            if item["url"] else ""
        )
        if names:
            label = "Eingeschrieben" if item["shared"] else "Reserviert von"
            who = f'<div class="item-names">{label}: {esc(", ".join(names))}</div>'
        else:
            who = '<div class="item-names empty">Noch niemand hat sich eingeschrieben.</div>'

        with st.container(border=True):
            html(
                f'<div class="item"><div class="item-num">{item["numeral"]}</div>'
                f'<div class="item-body"><div class="item-title">{item["title"]}</div>'
                f'<div class="item-sub">{item["subtitle"]}</div>{badge}{link}{who}</div></div>'
            )
            if guest in names:
                if st.button("Austragen", key=f"leave-{item['id']}", use_container_width=True):
                    with st.spinner(""):
                        db.remove_signup(item["id"], guest)
                    st.rerun()
            elif names and not item["shared"]:
                pass  # single gift already taken
            else:
                text = "Mich einschreiben" if item["shared"] else "Ich übernehme das"
                if st.button(text, key=f"join-{item['id']}", use_container_width=True):
                    with st.spinner(""):
                        db.add_signup(item["id"], item["title"], guest)
                    st.rerun()


# ---------------------------------------------------------------- main
def main() -> None:
    st.set_page_config(page_title="Arcanum", page_icon="🏛️", layout="centered")
    html(CSS)
    db = storage.backend()
    guest = st.session_state.get("guest")
    if guest:
        render_invitation(db, guest)
    else:
        render_gate(db)


if __name__ == "__main__":
    main()
