import base64
import html
import re
import time
from pathlib import Path

import streamlit as st

from ai_client import ask_gemini
from pitwall_prompt import build_pitwall_prompt
from scenarios import SCENARIOS


# =========================================================
# ŚCIEŻKI DO PLIKÓW
# =========================================================

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
TRACKS_DIR = ASSETS_DIR / "tracks"
UI_DIR = ASSETS_DIR / "ui"

TRACK_IMAGES = {
    "Monza": TRACKS_DIR / "monza.png",
    "Silverstone": TRACKS_DIR / "silverstone.png",
    "Spa": TRACKS_DIR / "spa.png",
    "Bahrain": TRACKS_DIR / "bahrain.png",
    "Hungaroring": TRACKS_DIR / "hungaroring.png",
    "Suzuka": TRACKS_DIR / "suzuka.png",
    "Interlagos": TRACKS_DIR / "interlagos.png",
}

UI_IMAGES = {
    "race_inputs": UI_DIR / "race_inputs.png",
    "ai_strategy": UI_DIR / "ai_strategy.png",
    "track_map": UI_DIR / "track_map.png",
    "tyre_status": UI_DIR / "tyre_status.png",
    "risk_analysis": UI_DIR / "risk_analysis.png",
    "engineer_radio": UI_DIR / "engineer_radio.png",
}

TRACK_INFO = {
    "Monza": {
        "length": "5.793 km",
        "turns": "11",
        "drs": "2",
        "country": "Italy",
    },
    "Silverstone": {
        "length": "5.891 km",
        "turns": "18",
        "drs": "2",
        "country": "United Kingdom",
    },
    "Spa": {
        "length": "7.004 km",
        "turns": "19",
        "drs": "2",
        "country": "Belgium",
    },
    "Bahrain": {
        "length": "5.412 km",
        "turns": "15",
        "drs": "3",
        "country": "Bahrain",
    },
    "Hungaroring": {
        "length": "4.381 km",
        "turns": "14",
        "drs": "1",
        "country": "Hungary",
    },
    "Suzuka": {
        "length": "5.807 km",
        "turns": "18",
        "drs": "1",
        "country": "Japan",
    },
    "Interlagos": {
        "length": "4.309 km",
        "turns": "15",
        "drs": "2",
        "country": "Brazil",
    },
    "Inny": {
        "length": "brak danych",
        "turns": "brak danych",
        "drs": "brak danych",
        "country": "brak danych",
    },
}


# =========================================================
# KONFIGURACJA STRONY
# =========================================================

st.set_page_config(
    page_title="PitWall AI",
    page_icon="🏁",
    layout="wide",
)


# =========================================================
# CSS / WYGLĄD APLIKACJI
# =========================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #080c13;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1580px;
        }

        /* HEADER */

        .pitwall-header {
            background:
                radial-gradient(circle at top left, rgba(225, 6, 0, 0.18), transparent 28%),
                linear-gradient(90deg, #111824 0%, #0b1018 58%, #270707 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 22px;
            padding: 22px 28px;
            margin-bottom: 18px;
            box-shadow: 0 0 34px rgba(225, 6, 0, 0.14);
        }

        .header-grid {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 22px;
        }

        .brand-left {
            display: flex;
            align-items: center;
            gap: 22px;
        }

        .logo-mark {
            width: 88px;
            height: 52px;
            position: relative;
            flex-shrink: 0;
        }

        .logo-mark::before {
            content: "";
            position: absolute;
            left: 2px;
            top: 6px;
            width: 76px;
            height: 14px;
            background: linear-gradient(90deg, #e10600, #ff3b30);
            transform: skewX(-24deg);
            border-radius: 3px;
            box-shadow: 0 0 20px rgba(225, 6, 0, 0.55);
        }

        .logo-mark::after {
            content: "";
            position: absolute;
            left: 20px;
            top: 27px;
            width: 54px;
            height: 12px;
            background: linear-gradient(90deg, #ffffff, #b8c0cc);
            transform: skewX(-24deg);
            border-radius: 3px;
            opacity: 0.95;
        }

        .brand-kicker {
            color: #ff4545;
            font-size: 12px;
            font-weight: 950;
            letter-spacing: 2.4px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .pitwall-title {
            font-size: 42px;
            font-weight: 950;
            color: #ffffff;
            line-height: 1.0;
            margin: 0;
            letter-spacing: 0.3px;
        }

        .pitwall-subtitle {
            font-size: 15px;
            color: #aeb7c2;
            margin-top: 6px;
        }

        .status-pill {
            display: inline-block;
            padding: 8px 13px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.13);
            color: #55ef82;
            border: 1px solid rgba(34, 197, 94, 0.36);
            font-weight: 850;
            font-size: 12px;
            white-space: nowrap;
        }

        /* SECTION HEADERS */

        .section-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 0 0 14px 0;
        }

        .section-icon {
            width: 34px;
            height: 34px;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 0 14px rgba(225, 6, 0, 0.25);
        }

        .section-title {
            font-size: 20px;
            font-weight: 950;
            color: #ffffff;
            letter-spacing: 0.7px;
            margin: 0;
            text-transform: uppercase;
        }

        .subsection-title {
            font-size: 20px;
            font-weight: 950;
            color: #ffffff;
            letter-spacing: 0.7px;
            margin: 22px 0 14px 0;
            text-transform: uppercase;
        }

        .small-muted {
            color: #8b95a3;
            font-size: 13px;
            line-height: 1.5;
        }

        /* PANELS */

        .scenario-box {
            background: #101720;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 14px 16px;
            margin: 12px 0 18px 0;
        }

        .panel {
            background: #101720;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 17px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 0 18px rgba(0,0,0,0.22);
        }

        /* TOP METRICS */

        .top-metric-card {
            background: linear-gradient(180deg, #141c27 0%, #101720 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 14px 16px;
            margin-bottom: 16px;
            min-height: 82px;
        }

        .top-metric-label {
            font-size: 12px;
            color: #8b95a3;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }

        .top-metric-value {
            font-size: 21px;
            color: #ffffff;
            font-weight: 950;
            line-height: 1.15;
        }

        /* AI CARDS */

        .metric-card {
            background: linear-gradient(180deg, #151e2a 0%, #101720 100%);
            border: 1px solid rgba(255,255,255,0.09);
            border-left: 4px solid #e10600;
            border-radius: 17px;
            padding: 18px;
            min-height: 150px;
            height: auto;
            overflow: visible;
            box-shadow: 0 0 18px rgba(225, 6, 0, 0.08);
            margin-bottom: 14px;
        }

        .metric-label {
            font-size: 12px;
            color: #aeb7c2;
            font-weight: 950;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 11px;
        }

        .metric-value {
            font-size: 25px;
            font-weight: 950;
            color: #ffffff;
            margin-bottom: 10px;
            line-height: 1.18;
        }

        .metric-text {
            color: #dce3ee;
            font-size: 14px;
            line-height: 1.55;
            word-break: normal;
            overflow-wrap: break-word;
        }

        .metric-text p {
            margin: 0 0 8px 0;
        }

        .metric-text ul {
            margin: 6px 0 0 0;
            padding-left: 18px;
        }

        .metric-text li {
            margin-bottom: 6px;
        }

        .radio-card {
            background: linear-gradient(90deg, #181f2b 0%, #111720 100%);
            border: 1px solid rgba(225, 6, 0, 0.38);
            border-radius: 17px;
            padding: 18px;
            margin-top: 12px;
            margin-bottom: 16px;
        }

        .radio-label {
            color: #ff4b4b;
            font-weight: 950;
            letter-spacing: 0.9px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .radio-message {
            color: #ffffff;
            font-size: 16px;
            font-style: italic;
            line-height: 1.55;
        }

        .risk-low {
            color: #4ade80;
            font-weight: 950;
        }

        .risk-medium {
            color: #facc15;
            font-weight: 950;
        }

        .risk-high {
            color: #fb4444;
            font-weight: 950;
        }

        /* TRACK MAP */

        .track-image-wrap {
            position: relative;
            background: #0b111a;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            overflow: hidden;
            padding: 0;
            margin-bottom: 12px;
            box-shadow: 0 0 18px rgba(0,0,0,0.25);
        }

        .track-image-wrap img {
            width: 100%;
            display: block;
            border-radius: 16px;
        }

        .driver-marker {
            position: absolute;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #e10600;
            border: 3px solid #ffffff;
            box-shadow: 0 0 18px rgba(225, 6, 0, 0.95);
            transform: translate(-50%, -50%);
        }

        .driver-marker::after {
            content: "P";
            color: white;
            font-size: 11px;
            font-weight: 950;
            position: absolute;
            left: 5px;
            top: 2px;
        }

        .track-info-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
            margin-bottom: 18px;
        }

        .track-info-item {
            background: #0d131c;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 10px;
        }

        .track-info-label {
            color: #8b95a3;
            font-size: 11px;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .track-info-value {
            color: #ffffff;
            font-size: 15px;
            font-weight: 900;
        }

        /* STREAMLIT DEFAULT COMPONENTS */

        div[data-testid="stMetric"] {
            background-color: #101720;
            border: 1px solid rgba(255,255,255,0.08);
            padding: 12px;
            border-radius: 14px;
        }

        .stProgress > div > div > div > div {
            background-color: #e10600;
        }

        button[kind="formSubmit"] {
            font-weight: 900;
            border-radius: 999px;
        }

        div[data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 13px;
            background: #101720;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNKCJE POMOCNICZE
# =========================================================

def safe_html(text):
    """
    Zabezpiecza tekst przed problemami z HTML-em.

    Dzięki temu tekst z formularza lub odpowiedzi AI może być bezpiecznie
    wstawiony do własnych elementów HTML.
    """

    if text is None or text == "":
        return "Brak danych."

    return html.escape(str(text))


def markdown_to_html(text):
    """
    Zamienia prosty Markdown na HTML.

    AI często zwraca pogrubienia jako **tekst**.
    W kartach dashboardu chcemy zobaczyć normalne pogrubienie,
    a nie gwiazdki.
    """

    if not text:
        return "Brak danych."

    escaped = html.escape(str(text))

    # Zamiana **tekst** na <strong>tekst</strong>
    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)

    lines = escaped.splitlines()
    result = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                result.append("<ul>")
                in_list = True

            result.append(f"<li>{stripped[2:].strip()}</li>")

        elif stripped:
            if in_list:
                result.append("</ul>")
                in_list = False

            result.append(f"<p>{stripped}</p>")

        else:
            if in_list:
                result.append("</ul>")
                in_list = False

    if in_list:
        result.append("</ul>")

    return "\n".join(result)


def extract_section(text, heading):
    """
    Wyciąga konkretną sekcję z odpowiedzi AI.

    Przykład:
    Z odpowiedzi zawierającej:
    ## Główna decyzja
    ## Strategia A
    ## Strategia B

    można wyciągnąć tylko sekcję 'Strategia A'.
    """

    if not text:
        return ""

    pattern = rf"##\s*{re.escape(heading)}\s*(.*?)(?=\n##\s|\Z)"
    match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def detect_risk_level(text):
    """
    Wykrywa poziom ryzyka na podstawie tekstu odpowiedzi AI.

    Funkcja szuka słów:
    - Wysokie
    - Średnie
    - Niskie

    i dobiera odpowiednią klasę CSS.
    """

    lower_text = text.lower() if text else ""

    if "wysokie" in lower_text:
        return "Wysokie", "risk-high"

    if "średnie" in lower_text or "srednie" in lower_text:
        return "Średnie", "risk-medium"

    if "niskie" in lower_text:
        return "Niskie", "risk-low"

    return "Nieokreślone", "risk-medium"


@st.cache_data
def image_to_base64(path_str):
    """
    Wczytuje obrazek i zamienia go na Base64.

    Dzięki temu grafiki z folderu assets można wstawiać do HTML-a
    jako <img src="data:image/png;base64,...">.
    """

    path = Path(path_str)

    if not path.exists():
        return None

    return base64.b64encode(path.read_bytes()).decode("utf-8")


def make_card(label, value, text):
    """
    Tworzy stylizowaną kartę dashboardu.

    Używana do:
    - Main Decision
    - Strategy A
    - Strategy B
    - Risk Level
    """

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_html(label)}</div>
            <div class="metric-value">{safe_html(value)}</div>
            <div class="metric-text">{markdown_to_html(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def generate_demo_response(dane):
    """
    Tryb demo bez API.

    Jeśli Gemini API nie działa, skończył się limit albo nie ma internetu,
    aplikacja może wygenerować przykładową odpowiedź lokalnie.
    """

    return f"""
## Główna decyzja
Przygotować pit stop w najbliższych 1-2 okrążeniach.

## Strategia A
Rekomendowana strategia to zjazd do boksu około okrążenia {dane["aktualne_okrazenie"] + 1} lub {dane["aktualne_okrazenie"] + 2} i zmiana opon na Hard. Aktualne opony {dane["opony"]} są zużyte w {dane["zuzycie_opon"]}%, więc dalsze przedłużanie stintu może powodować spadek tempa.

## Strategia B
Alternatywnie można zostać na torze jeszcze kilka okrążeń i spróbować overcutu, ale ta strategia ma sens tylko wtedy, gdy tempo pozostaje stabilne albo pojawi się Safety Car / VSC.

## Poziom ryzyka
Średnie. Ryzyko wynika głównie ze zużycia opon, możliwej utraty tempa oraz przewagi nad kierowcą z tyłu wynoszącej {dane["przewaga_nad_tylem"]} s.

## Uzasadnienie
Na torze {dane["tor"]} kluczowe jest utrzymanie tempa i uniknięcie wyjazdu w ruch po pit stopie. Strata do kierowcy z przodu wynosi {dane["strata_do_przodu"]} s, dlatego zbyt późny pit stop może utrudnić walkę o pozycję.

## Co może pójść źle?
- Rywal z tyłu może spróbować undercutu.
- Zużycie opon może gwałtownie pogorszyć tempo.
- Pit stop wykonany w złym momencie może wypuścić kierowcę w ruch na torze.

## Komunikat radiowy dla kierowcy
"Box window is opening. Keep the tyres alive and prepare for a possible stop in the next two laps."

## Podsumowanie dla zespołu
Najbezpieczniejszą decyzją jest przygotowanie pit stopu w krótkim oknie strategicznym i przejście na twardą mieszankę.
"""


def tyre_status_text(zuzycie):
    """
    Zwraca opis stanu opon na podstawie procentowego zużycia.
    """

    if zuzycie < 35:
        return "Opony są w dobrym stanie. Można kontynuować stint."

    if zuzycie < 65:
        return "Opony są w średnim stanie. Trzeba obserwować tempo."

    if zuzycie < 80:
        return "Opony są mocno zużyte. Pit window jest blisko."

    return "Opony są krytycznie zużyte. Pit stop jest pilny."


def risk_value_from_inputs(zuzycie, pogoda, safety_car, przewaga_nad_tylem):
    """
    Lokalnie wylicza wartości ryzyka do pasków w dashboardzie.

    To nie jest odpowiedź AI, tylko prosta logika aplikacji.
    """

    tyre_risk = min(100, int(zuzycie))

    weather_risk = 15
    if pogoda == "Lekki deszcz":
        weather_risk = 55
    elif pogoda == "Deszcz":
        weather_risk = 85

    position_risk = 25
    if przewaga_nad_tylem < 1.5:
        position_risk = 80
    elif przewaga_nad_tylem < 3:
        position_risk = 55

    safety_car_risk = 65 if safety_car else 25

    overall = int((tyre_risk + weather_risk + position_risk + safety_car_risk) / 4)

    return tyre_risk, weather_risk, position_risk, overall


def marker_position_for_sector(sektor):
    """
    Zwraca pozycję markera kierowcy na grafice toru.

    Pozycje są orientacyjne i służą do wizualizacji sektora.
    """

    positions = {
        "Sektor 1": ("72%", "38%"),
        "Sektor 2": ("48%", "33%"),
        "Sektor 3": ("29%", "61%"),
        "Pit entry": ("68%", "72%"),
        "Pit exit": ("53%", "70%"),
    }

    return positions.get(sektor, ("50%", "45%"))


def render_logo_header():
    """
    Renderuje górny nagłówek aplikacji z logo i statusem API.
    """

    st.markdown(
        """
        <div class="pitwall-header">
            <div class="header-grid">
                <div class="brand-left">
                    <div class="logo-mark"></div>
                    <div>
                        <div class="brand-kicker">F1 Strategy Dashboard</div>
                        <div class="pitwall-title">PitWall AI</div>
                        <div class="pitwall-subtitle">
                            AI Race Strategy Assistant — system wspierający decyzje strategiczne w wyścigu
                        </div>
                    </div>
                </div>
                <div class="status-pill">● Gemini API connected</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title, image_key=None):
    """
    Renderuje nagłówek sekcji z opcjonalną mini grafiką.

    Jeśli plik grafiki istnieje w assets/ui, zostanie pokazany.
    Jeśli nie istnieje, aplikacja pokaże sam tytuł.
    """

    image_html = ""

    if image_key and image_key in UI_IMAGES:
        image_path = UI_IMAGES[image_key]

        if image_path.exists():
            image_b64 = image_to_base64(str(image_path))
            image_html = (
                f'<img class="section-icon" '
                f'src="data:image/png;base64,{image_b64}" '
                f'alt="{safe_html(title)} icon">'
            )

    st.markdown(
        f"""
        <div class="section-header">
            {image_html}
            <div class="section-title">{safe_html(title)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_track_preview(tor, sektor):
    """
    Renderuje grafikę toru i marker aktualnego sektora kierowcy.
    """

    track_data = TRACK_INFO.get(tor, TRACK_INFO["Inny"])
    image_path = TRACK_IMAGES.get(tor)
    marker_left, marker_top = marker_position_for_sector(sektor)

    render_section_header("Track Map", "track_map")

    if image_path and image_path.exists():
        image_b64 = image_to_base64(str(image_path))

        st.markdown(
            f"""
            <div class="track-image-wrap">
                <img src="data:image/png;base64,{image_b64}" alt="{safe_html(tor)} track map">
                <div class="driver-marker" style="left:{marker_left}; top:{marker_top};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            f"Brak grafiki toru dla: {tor}. "
            f"Sprawdź, czy plik istnieje w folderze assets/tracks."
        )

    st.markdown(
        f"""
        <div class="track-info-row">
            <div class="track-info-item">
                <div class="track-info-label">Sector</div>
                <div class="track-info-value">{safe_html(sektor)}</div>
            </div>
            <div class="track-info-item">
                <div class="track-info-label">Length</div>
                <div class="track-info-value">{safe_html(track_data["length"])}</div>
            </div>
            <div class="track-info-item">
                <div class="track-info-label">Turns / DRS</div>
                <div class="track-info-value">{safe_html(track_data["turns"])} / {safe_html(track_data["drs"])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_metric(label, value):
    """
    Renderuje górny kafelek z najważniejszą informacją.
    """

    st.markdown(
        f"""
        <div class="top-metric-card">
            <div class="top-metric-label">{safe_html(label)}</div>
            <div class="top-metric-value">{safe_html(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HEADER
# =========================================================

render_logo_header()


# =========================================================
# WYBÓR SCENARIUSZA
# =========================================================

scenario_name = st.selectbox(
    "Wybierz szybki scenariusz testowy",
    list(SCENARIOS.keys()),
)

scenario = SCENARIOS[scenario_name]

st.markdown(
    f"""
    <div class="scenario-box">
        <b>Aktywny scenariusz:</b> {safe_html(scenario_name)}<br>
        <span class="small-muted">
            Scenariusze pomagają szybko testować aplikację bez ręcznego wpisywania wszystkich danych.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GŁÓWNY UKŁAD
# =========================================================

left_col, center_col, right_col = st.columns([0.95, 1.45, 1.08])


# =========================================================
# LEWY PANEL — RACE INPUTS
# =========================================================

with left_col:
    render_section_header("Race Inputs", "race_inputs")

    with st.form("race_form"):
        tor_options = [
            "Monza",
            "Silverstone",
            "Spa",
            "Bahrain",
            "Hungaroring",
            "Suzuka",
            "Interlagos",
            "Inny",
        ]

        tyre_options = [
            "Soft",
            "Medium",
            "Hard",
            "Intermediate",
            "Wet",
        ]

        weather_options = [
            "Sucho",
            "Lekki deszcz",
            "Deszcz",
        ]

        strategy_options = [
            "Agresywna",
            "Zbalansowana",
            "Bezpieczna",
        ]

        sector_options = [
            "Sektor 1",
            "Sektor 2",
            "Sektor 3",
            "Pit entry",
            "Pit exit",
        ]

        tor = st.selectbox(
            "Tor",
            tor_options,
            index=tor_options.index(scenario["tor"]) if scenario["tor"] in tor_options else 0,
        )

        aktualne_okrazenie = st.number_input(
            "Aktualne okrążenie",
            min_value=1,
            max_value=100,
            value=int(scenario["aktualne_okrazenie"]),
        )

        liczba_okrazen = st.number_input(
            "Liczba okrążeń",
            min_value=1,
            max_value=100,
            value=int(scenario["liczba_okrazen"]),
        )

        pozycja = st.number_input(
            "Pozycja kierowcy",
            min_value=1,
            max_value=20,
            value=int(scenario["pozycja"]),
        )

        opony = st.selectbox(
            "Aktualna mieszanka opon",
            tyre_options,
            index=tyre_options.index(scenario["opony"]) if scenario["opony"] in tyre_options else 1,
        )

        zuzycie_opon = st.slider(
            "Zużycie opon (%)",
            min_value=0,
            max_value=100,
            value=int(scenario["zuzycie_opon"]),
        )

        pogoda = st.selectbox(
            "Pogoda",
            weather_options,
            index=weather_options.index(scenario["pogoda"]) if scenario["pogoda"] in weather_options else 0,
        )

        safety_car = st.checkbox(
            "Safety Car / VSC",
            value=bool(scenario["safety_car"]),
        )

        sektor = st.selectbox(
            "Aktualny sektor toru",
            sector_options,
            index=sector_options.index(scenario["sektor"]) if scenario["sektor"] in sector_options else 0,
        )

        strata_do_przodu = st.number_input(
            "Strata do kierowcy z przodu (s)",
            min_value=0.0,
            max_value=120.0,
            value=float(scenario["strata_do_przodu"]),
            step=0.1,
        )

        przewaga_nad_tylem = st.number_input(
            "Przewaga nad kierowcą z tyłu (s)",
            min_value=0.0,
            max_value=120.0,
            value=float(scenario["przewaga_nad_tylem"]),
            step=0.1,
        )

        styl_strategii = st.radio(
            "Styl strategii",
            strategy_options,
            index=strategy_options.index(scenario["styl_strategii"])
            if scenario["styl_strategii"] in strategy_options
            else 1,
        )

        tryb_demo = st.checkbox(
            "Tryb demo bez API",
            value=False,
            help="Użyj, gdy skończy się limit API albo chcesz pokazać aplikację bez wysyłania zapytania do Gemini.",
        )

        submit = st.form_submit_button("Update Analysis")


# =========================================================
# DANE DO PROMPTU
# =========================================================

dane = {
    "tor": tor,
    "aktualne_okrazenie": aktualne_okrazenie,
    "liczba_okrazen": liczba_okrazen,
    "pozycja": pozycja,
    "opony": opony,
    "zuzycie_opon": zuzycie_opon,
    "pogoda": pogoda,
    "safety_car": "Tak" if safety_car else "Nie",
    "strata_do_przodu": strata_do_przodu,
    "przewaga_nad_tylem": przewaga_nad_tylem,
    "styl_strategii": styl_strategii,
}


# =========================================================
# TOP METRICS
# =========================================================

tm1, tm2, tm3, tm4 = st.columns(4)

with tm1:
    render_top_metric("Track", tor)

with tm2:
    render_top_metric("Race position", f"P{pozycja}")

with tm3:
    render_top_metric("Tyre compound", f"{opony} · {zuzycie_opon}%")

with tm4:
    sc_text = "SC/VSC" if safety_car else "No SC"
    render_top_metric("Conditions", f"{pogoda} · {sc_text}")


# =========================================================
# PRAWY PANEL — TOR, OPONY, RYZYKO
# =========================================================

with right_col:
    render_track_preview(tor, sektor)

    render_section_header("Tyre Status", "tyre_status")

    st.metric("Mieszanka", opony)
    st.metric("Zużycie opon", f"{zuzycie_opon}%")
    st.progress(zuzycie_opon / 100)
    st.write(tyre_status_text(zuzycie_opon))

    tyre_risk, weather_risk, position_risk, overall_risk = risk_value_from_inputs(
        zuzycie_opon,
        pogoda,
        safety_car,
        przewaga_nad_tylem,
    )

    render_section_header("Risk Analysis", "risk_analysis")

    st.write("Ryzyko degradacji opon")
    st.progress(tyre_risk / 100)

    st.write("Ryzyko pogodowe")
    st.progress(weather_risk / 100)

    st.write("Ryzyko utraty pozycji")
    st.progress(position_risk / 100)

    st.write("Ogólne ryzyko strategii")
    st.progress(overall_risk / 100)


# =========================================================
# ŚRODKOWY PANEL — AI STRATEGY
# =========================================================

with center_col:
    render_section_header("AI Strategy Recommendation", "ai_strategy")

    if not submit:
        st.info("Ustaw dane wyścigowe po lewej stronie i kliknij „Update Analysis”, aby wygenerować rekomendację.")

    else:
        if aktualne_okrazenie > liczba_okrazen:
            st.error("Aktualne okrążenie nie może być większe niż liczba wszystkich okrążeń.")

        else:
            prompt = build_pitwall_prompt(dane)

            if tryb_demo:
                with st.spinner("PitWall AI generuje analizę w trybie demo..."):
                    time.sleep(1.0)
                    odpowiedz_ai = generate_demo_response(dane)

                st.warning("Tryb demo: odpowiedź wygenerowana bez użycia Gemini API.")

            else:
                with st.spinner("PitWall AI analizuje strategię przez Gemini API..."):
                    odpowiedz_ai = ask_gemini(prompt)

                st.success("Analiza AI została wygenerowana.")

            main_decision = extract_section(odpowiedz_ai, "Główna decyzja")
            strategy_a = extract_section(odpowiedz_ai, "Strategia A")
            strategy_b = extract_section(odpowiedz_ai, "Strategia B")
            risk = extract_section(odpowiedz_ai, "Poziom ryzyka")
            justification = extract_section(odpowiedz_ai, "Uzasadnienie")
            problems = extract_section(odpowiedz_ai, "Co może pójść źle?")
            radio = extract_section(odpowiedz_ai, "Komunikat radiowy dla kierowcy")
            summary = extract_section(odpowiedz_ai, "Podsumowanie dla zespołu")

            risk_label, risk_class = detect_risk_level(risk)

            card_col_1, card_col_2 = st.columns(2)

            with card_col_1:
                make_card(
                    "Main Decision",
                    main_decision if main_decision else "Brak decyzji",
                    f"Lap {aktualne_okrazenie}/{liczba_okrazen} | P{pozycja} | {opony}",
                )

            with card_col_2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Risk Level</div>
                        <div class="metric-value {risk_class}">{safe_html(risk_label)}</div>
                        <div class="metric-text">{markdown_to_html(risk)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="subsection-title">Strategy Cards</div>', unsafe_allow_html=True)

            strat_col_1, strat_col_2 = st.columns(2)

            with strat_col_1:
                make_card(
                    "Strategy A",
                    "Plan A",
                    strategy_a if strategy_a else "Brak strategii A.",
                )

            with strat_col_2:
                make_card(
                    "Strategy B",
                    "Plan B",
                    strategy_b if strategy_b else "Brak strategii B.",
                )

            if radio:
                render_section_header("Race Engineer Radio", "engineer_radio")

                st.markdown(
                    f"""
                    <div class="radio-card">
                        <div class="radio-label">Radio Message</div>
                        <div class="radio-message">{markdown_to_html(radio)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="subsection-title">Strategic Details</div>', unsafe_allow_html=True)

            with st.expander("Uzasadnienie decyzji", expanded=True):
                st.markdown(justification if justification else "Brak uzasadnienia.")

            with st.expander("Co może pójść źle?", expanded=True):
                st.markdown(problems if problems else "Brak listy ryzyk.")

            with st.expander("Podsumowanie dla zespołu", expanded=False):
                st.markdown(summary if summary else "Brak podsumowania.")

            with st.expander("Pełna odpowiedź AI", expanded=False):
                st.markdown(odpowiedz_ai)

            with st.expander("Podgląd promptu wysłanego do modelu", expanded=False):
                st.code(prompt, language="text")


# =========================================================
# STOPKA
# =========================================================

st.divider()

st.caption(
    "PitWall AI — projekt - Sztuczna Inteligencja. "
    "Autor: Bartosz Łach TKiMS"
)