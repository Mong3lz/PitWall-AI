import streamlit as st
from pitwall_prompt import build_pitwall_prompt
from ai_client import ask_gemini

# -----------------------------
# KONFIGURACJA STRONY
# -----------------------------

st.set_page_config(
    page_title="PitWall AI",
    page_icon="🏎️",
    layout="wide"
)


# -----------------------------
# FUNKCJA ANALIZUJĄCA STRATEGIĘ
# Na razie to wersja testowa bez API.
# W tygodniu 3 podmienimy tę logikę na odpowiedź modelu AI.
# -----------------------------

def analizuj_strategie(
    tor,
    aktualne_okrazenie,
    liczba_okrazen,
    pozycja,
    opony,
    zuzycie_opon,
    pogoda,
    safety_car,
    strata_do_przodu,
    przewaga_nad_tylem,
    styl_strategii
):
    """
    Funkcja przyjmuje dane z formularza i zwraca prostą rekomendację strategiczną.
    Na tym etapie działa na prostych zasadach, bez użycia modelu AI.
    """

    # Obliczamy, jaka część wyścigu już minęła
    procent_wyscigu = aktualne_okrazenie / liczba_okrazen

    # Domyślne wartości odpowiedzi
    decyzja = "Zostań na torze"
    strategia_a = "Kontynuuj obecny stint i obserwuj tempo rywali."
    strategia_b = "Przygotuj alternatywny pit stop w przypadku zmiany sytuacji na torze."
    ryzyko = "Niskie"
    uzasadnienie = "Sytuacja jest stabilna, dlatego nie ma potrzeby wykonywania natychmiastowego pit stopu."
    komunikat = "Keep pushing. Tyres are looking okay for now."

    # Logika dla Safety Cara
    if safety_car:
        decyzja = "Zjedź do pit stopu"
        strategia_a = f"Wykorzystaj Safety Car i zmień opony z {opony} na Hard lub Medium."
        strategia_b = "Jeżeli pit lane jest zatłoczone, zostań na torze jeszcze jedno okrążenie."
        ryzyko = "Średnie"
        uzasadnienie = "Safety Car zmniejsza stratę czasową podczas pit stopu, dlatego jest to dobra okazja na zmianę opon."
        komunikat = "Box, box. Safety Car window is open."

    # Logika dla bardzo zużytych opon
    elif zuzycie_opon >= 75:
        decyzja = "Zjedź do pit stopu"
        strategia_a = "Zjedź jak najszybciej i załóż świeższy komplet opon."
        strategia_b = "Zostań na torze maksymalnie 1-2 okrążenia, jeżeli chcesz uniknąć ruchu po pit stopie."
        ryzyko = "Wysokie"
        uzasadnienie = "Zużycie opon jest bardzo wysokie, co może powodować dużą utratę tempa i ryzyko błędu."
        komunikat = "Box this lap. Tyre degradation is too high."

    # Logika dla deszczu
    elif pogoda == "Deszcz":
        decyzja = "Rozważ natychmiastowy pit stop"
        strategia_a = "Jeżeli tor jest mokry, zmień opony na Intermediate lub Wet."
        strategia_b = "Jeżeli deszcz jest lekki, zostań na torze i obserwuj czasy sektorów."
        ryzyko = "Wysokie"
        uzasadnienie = "Zmiana pogody może mocno wpłynąć na przyczepność i tempo jazdy."
        komunikat = "Rain reported. Watch the grip and prepare for inters."

    # Logika dla średniego zużycia opon
    elif 50 <= zuzycie_opon < 75:
        decyzja = "Przygotuj pit stop w najbliższych okrążeniach"
        strategia_a = "Zostań na torze jeszcze 2-4 okrążenia i zjedź po świeże opony."
        strategia_b = "Zjedź wcześniej, jeżeli rywale rozpoczną undercut."
        ryzyko = "Średnie"
        uzasadnienie = "Opony są już wyraźnie zużyte, ale nie wymagają natychmiastowej zmiany."
        komunikat = "Tyres are dropping. Target pit window in a few laps."

    # Logika dla końcówki wyścigu
    if procent_wyscigu > 0.80 and zuzycie_opon < 70 and not safety_car:
        decyzja = "Zostań na torze do końca"
        strategia_a = "Nie zjeżdżaj, jeżeli tempo jest stabilne."
        strategia_b = "Zjedź tylko w przypadku dużej utraty tempa lub Safety Cara."
        ryzyko = "Średnie"
        uzasadnienie = "Do końca wyścigu zostało niewiele okrążeń, więc pit stop może kosztować zbyt dużo pozycji."
        komunikat = "Stay out. Bring the car home."

    # Korekta pod styl strategii
    if styl_strategii == "Agresywna":
        strategia_b += " Można też rozważyć wcześniejszy pit stop, aby spróbować undercutu."
    elif styl_strategii == "Bezpieczna":
        strategia_b += " Priorytetem jest utrzymanie pozycji i unikanie ryzyka."
    else:
        strategia_b += " Strategia powinna balansować tempo i ryzyko."

    # Dodatkowe info o rywalach
    sytuacja_rywali = (
        f"Strata do kierowcy z przodu: {strata_do_przodu} s. "
        f"Przewaga nad kierowcą z tyłu: {przewaga_nad_tylem} s."
    )

    return {
        "decyzja": decyzja,
        "strategia_a": strategia_a,
        "strategia_b": strategia_b,
        "ryzyko": ryzyko,
        "uzasadnienie": uzasadnienie,
        "komunikat": komunikat,
        "sytuacja_rywali": sytuacja_rywali
    }


# -----------------------------
# NAGŁÓWEK APLIKACJI
# -----------------------------

st.title("🏎️ PitWall AI")
st.subheader("Inteligentny asystent strategii wyścigowej F1")

st.write(
    """
    Aplikacja analizuje sytuację wyścigową i generuje rekomendację strategiczną.
    Na tym etapie projekt działa jako wersja testowa bez połączenia z API.
    W kolejnym tygodniu logika zostanie rozszerzona o model AI/LLM.
    """
)

st.divider()


# -----------------------------
# UKŁAD STRONY
# -----------------------------

lewa_kolumna, prawa_kolumna = st.columns([1, 1])


# -----------------------------
# FORMULARZ DANYCH WYŚCIGOWYCH
# -----------------------------

with lewa_kolumna:
    st.header("Dane wyścigowe")

    with st.form("formularz_strategii"):
        tor = st.selectbox(
            "Wybierz tor",
            ["Monza", "Silverstone", "Spa", "Bahrain", "Hungaroring", "Suzuka", "Interlagos", "Inny"]
        )

        aktualne_okrazenie = st.number_input(
            "Aktualne okrążenie",
            min_value=1,
            max_value=100,
            value=24
        )

        liczba_okrazen = st.number_input(
            "Liczba okrążeń w wyścigu",
            min_value=1,
            max_value=100,
            value=53
        )

        pozycja = st.number_input(
            "Aktualna pozycja kierowcy",
            min_value=1,
            max_value=20,
            value=6
        )

        opony = st.selectbox(
            "Aktualna mieszanka opon",
            ["Soft", "Medium", "Hard", "Intermediate", "Wet"]
        )

        zuzycie_opon = st.slider(
            "Zużycie opon (%)",
            min_value=0,
            max_value=100,
            value=62
        )

        pogoda = st.selectbox(
            "Warunki pogodowe",
            ["Sucho", "Lekki deszcz", "Deszcz"]
        )

        safety_car = st.checkbox("Safety Car / Virtual Safety Car na torze")

        strata_do_przodu = st.number_input(
            "Strata do kierowcy z przodu (sekundy)",
            min_value=0.0,
            max_value=120.0,
            value=5.8,
            step=0.1
        )

        przewaga_nad_tylem = st.number_input(
            "Przewaga nad kierowcą z tyłu (sekundy)",
            min_value=0.0,
            max_value=120.0,
            value=3.2,
            step=0.1
        )

        styl_strategii = st.radio(
            "Styl strategii",
            ["Agresywna", "Zbalansowana", "Bezpieczna"],
            index=1
        )

        przycisk = st.form_submit_button("Analizuj strategię")


# -----------------------------
# WYNIK ANALIZY
# -----------------------------

with prawa_kolumna:
    st.header("Rekomendacja PitWall AI")

    if przycisk:
        if aktualne_okrazenie > liczba_okrazen:
            st.error("Aktualne okrążenie nie może być większe niż liczba okrążeń w wyścigu.")
        else:
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
                "styl_strategii": styl_strategii
            }

            prompt = build_pitwall_prompt(dane)

            with st.spinner("PitWall AI analizuje strategię przez Gemini API..."):
                odpowiedz_ai = ask_gemini(prompt)

            st.success("Analiza AI została wygenerowana.")
            st.markdown(odpowiedz_ai)

            with st.expander("Podgląd promptu wysłanego do modelu"):
                st.code(prompt, language="text")

    else:
        st.info("Uzupełnij dane po lewej stronie i kliknij przycisk „Analizuj strategię”.")





# -----------------------------
# STOPKA
# -----------------------------

st.divider()

st.caption(
    "PitWall AI — projekt na przedmiot Sztuczna Inteligencja. "
    "Wersja 0.1: interfejs i testowa logika bez API."
)