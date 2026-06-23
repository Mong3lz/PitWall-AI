# PitWall AI

PitWall AI to aplikacja przygotowana na przedmiot **Sztuczna Inteligencja**.
Projekt przedstawia inteligentnego asystenta strategii wyścigowej Formuły 1, który pomaga analizować sytuację na torze i generuje rekomendacje strategiczne przy użyciu modelu AI Gemini.

Aplikacja została wykonana w Pythonie z użyciem biblioteki Streamlit oraz integracji z Gemini API.

---

## 1. Cel projektu

Celem projektu jest pokazanie praktycznego zastosowania istniejącego modelu językowego AI/LLM.

Aplikacja nie trenuje własnego modelu sztucznej inteligencji. Zamiast tego korzysta z gotowego modelu Gemini przez API.

Podstawowy przepływ działania wygląda następująco:

```text
Dane z formularza → Prompt → Gemini API → Odpowiedź AI → Dashboard
```

Użytkownik wpisuje dane dotyczące aktualnej sytuacji wyścigowej, a aplikacja generuje rekomendację dotyczącą strategii, pit stopu, opon, ryzyka oraz możliwych problemów.

---

## 2. Funkcje aplikacji

Aplikacja umożliwia:

* wybór gotowego scenariusza wyścigowego,
* ręczne wprowadzenie danych wyścigowych,
* wybór toru,
* określenie aktualnego okrążenia,
* wybór mieszanki opon,
* określenie zużycia opon,
* wybór warunków pogodowych,
* zaznaczenie Safety Cara lub VSC,
* analizę ryzyka,
* wyświetlenie mapy toru,
* pokazanie statusu opon,
* wygenerowanie rekomendacji strategii przez AI,
* pokazanie strategii A i strategii B,
* wygenerowanie komunikatu radiowego dla kierowcy,
* uruchomienie trybu demo bez API.

---

## 3. Technologie

Projekt wykorzystuje:

* Python,
* Streamlit,
* Google Gemini API,
* bibliotekę `google-genai`,
* HTML/CSS osadzone w Streamlit,
* lokalne grafiki w folderze `assets`.

---

## 4. Struktura projektu

Folder projektu powinien wyglądać w podobny sposób:

```text
PitWall/
│
├── app.py
├── ai_client.py
├── pitwall_prompt.py
├── scenarios.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── secrets.toml
│
└── assets/
    ├── tracks/
    │   ├── monza.png
    │   ├── silverstone.png
    │   ├── spa.png
    │   ├── bahrain.png
    │   ├── hungaroring.png
    │   ├── suzuka.png
    │   └── interlagos.png
    │
    └── ui/
        ├── race_inputs.png
        ├── ai_strategy.png
        ├── track_map.png
        ├── tyre_status.png
        ├── risk_analysis.png
        └── engineer_radio.png
```

---

## 5. Opis najważniejszych plików

### `app.py`

Główny plik aplikacji.

Odpowiada za:

* wygląd aplikacji,
* formularz danych wyścigowych,
* dashboard,
* wyświetlanie grafik,
* status opon,
* analizę ryzyka,
* prezentację odpowiedzi AI.

---

### `ai_client.py`

Plik odpowiedzialny za połączenie z Gemini API.

Odpowiada za:

* pobranie klucza API,
* wysłanie promptu do Gemini,
* odebranie odpowiedzi,
* obsługę błędów API.

---

### `pitwall_prompt.py`

Plik odpowiedzialny za budowanie promptu.

Dane wpisane przez użytkownika są zamieniane na instrukcję dla modelu AI.

---

### `scenarios.py`

Plik z gotowymi scenariuszami wyścigowymi.

Dzięki niemu można szybko testować aplikację bez ręcznego wpisywania wszystkich danych.

---

### `requirements.txt`

Plik zawierający listę bibliotek potrzebnych do uruchomienia projektu.

Przykładowa zawartość:

```txt
streamlit
google-genai
```

---

### `.streamlit/secrets.toml`

Plik z kluczem API Gemini.

Ten plik nie powinien być udostępniany publicznie.

---

## 6. Przygotowanie projektu do uruchomienia

### Krok 1: Otwórz folder projektu

Najpierw należy otworzyć terminal w folderze projektu.

Przykład w PowerShell:

```powershell
cd D:\Vsc\PitWall
```

Ścieżka może być inna w zależności od tego, gdzie znajduje się projekt.

---

### Krok 2: Utwórz środowisko wirtualne

Jeśli środowisko wirtualne jeszcze nie istnieje, należy je utworzyć:

```powershell
python -m venv .venv
```

Po tej komendzie w folderze projektu powinien pojawić się folder `.venv`.

---

### Krok 3: Aktywuj środowisko wirtualne

W PowerShell:

```powershell
.venv\Scripts\activate
```

Jeśli PowerShell blokuje uruchomienie skryptu, można tymczasowo pozwolić na jego wykonanie:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Następnie ponownie aktywować środowisko:

```powershell
.venv\Scripts\activate
```

Po poprawnej aktywacji w terminalu powinno pojawić się coś podobnego:

```text
(.venv) PS D:\Vsc\PitWall>
```

---

### Krok 4: Zainstaluj wymagane biblioteki

Po aktywacji środowiska należy zainstalować biblioteki z pliku `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Jeśli plik `requirements.txt` nie istnieje, można zainstalować biblioteki ręcznie:

```powershell
python -m pip install streamlit google-genai
```

---

## 7. Konfiguracja klucza Gemini API

Aby aplikacja mogła korzystać z Gemini API, potrzebny jest klucz API.

W folderze projektu należy utworzyć folder:

```text
.streamlit
```

W nim należy utworzyć plik:

```text
secrets.toml
```

Pełna ścieżka powinna wyglądać tak:

```text
PitWall/.streamlit/secrets.toml
```

W pliku `secrets.toml` należy wkleić:

```toml
GEMINI_API_KEY = "TUTAJ_WKLEJ_SWÓJ_KLUCZ_API"
```

Przykład:

```toml
GEMINI_API_KEY = "AIza..."
```

Ważne: klucza API nie należy pokazywać publicznie ani wrzucać do repozytorium.

---

## 8. Uruchomienie aplikacji

Po zainstalowaniu bibliotek i dodaniu klucza API należy uruchomić aplikację komendą:

```powershell
python -m streamlit run app.py
```

Po uruchomieniu aplikacja powinna automatycznie otworzyć się w przeglądarce.

Jeśli nie otworzy się sama, można wejść ręcznie pod adres:

```text
http://localhost:8501
```

---

## 9. Jak korzystać z aplikacji

Po uruchomieniu aplikacji należy:

1. Wybrać gotowy scenariusz testowy albo zostawić własne ustawienia.
2. Uzupełnić dane w sekcji **Race Inputs**.
3. Sprawdzić mapę toru, status opon i analizę ryzyka.
4. Kliknąć przycisk **Update Analysis**.
5. Poczekać na odpowiedź AI.
6. Odczytać rekomendację strategii w sekcji **AI Strategy Recommendation**.

Aplikacja pokaże między innymi:

* główną decyzję strategiczną,
* strategię A,
* strategię B,
* poziom ryzyka,
* uzasadnienie,
* potencjalne problemy,
* komunikat radiowy dla kierowcy.

---

## 10. Tryb demo bez API

Aplikacja posiada tryb demo bez API.

Można go włączyć w formularzu poprzez zaznaczenie opcji:

```text
Tryb demo bez API
```

Po włączeniu tej opcji aplikacja nie wysyła zapytania do Gemini API, tylko generuje przykładową odpowiedź lokalnie.

Tryb demo jest przydatny, gdy:

* skończy się limit API,
* nie ma internetu,
* klucz API nie działa,
* API chwilowo zwraca błąd,

---

## 11. Możliwe problemy i rozwiązania

### Problem: aplikacja nie widzi biblioteki Streamlit

Błąd może wyglądać tak:

```text
ModuleNotFoundError: No module named 'streamlit'
```

Rozwiązanie:

```powershell
python -m pip install streamlit
```

---

### Problem: aplikacja nie widzi biblioteki google-genai

Błąd może wyglądać tak:

```text
ModuleNotFoundError: No module named 'google.genai'
```

Rozwiązanie:

```powershell
python -m pip install google-genai
```

---

### Problem: brak klucza API

Jeśli aplikacja pokazuje informację o braku klucza API, trzeba sprawdzić, czy istnieje plik:

```text
.streamlit/secrets.toml
```

oraz czy zawiera:

```toml
GEMINI_API_KEY = "TWÓJ_KLUCZ_API"
```

---

### Problem: przekroczony limit API

Jeśli Gemini zwraca błąd limitu, można włączyć:

```text
Tryb demo bez API
```

Dzięki temu aplikacja nadal będzie działała.

---

### Problem: nie wyświetlają się grafiki torów

Należy sprawdzić, czy pliki znajdują się w folderze:

```text
assets/tracks/
```

oraz czy mają dokładnie takie nazwy:

```text
monza.png
silverstone.png
spa.png
bahrain.png
hungaroring.png
suzuka.png
interlagos.png
```

---

### Problem: nie wyświetlają się mini grafiki sekcji

Należy sprawdzić, czy pliki znajdują się w folderze:

```text
assets/ui/
```

oraz czy mają dokładnie takie nazwy:

```text
race_inputs.png
ai_strategy.png
track_map.png
tyre_status.png
risk_analysis.png
engineer_radio.png
```

---

## 12. Główny przepływ działania aplikacji

```text
1. Użytkownik wybiera scenariusz albo wpisuje dane ręcznie.
2. Dane trafiają do formularza Streamlit.
3. Aplikacja tworzy słownik z danymi.
4. Funkcja build_pitwall_prompt() tworzy prompt.
5. Funkcja ask_gemini() wysyła prompt do Gemini API.
6. Model AI generuje odpowiedź.
7. Aplikacja dzieli odpowiedź na sekcje.
8. Dashboard pokazuje wynik w czytelnej formie.
```

---

## 13. Podsumowanie

PitWall AI to aplikacja pokazująca praktyczne użycie modelu AI w kontekście strategii wyścigowej Formuły 1.

Projekt łączy:

* interaktywny formularz,
* model językowy Gemini,
* gotowe scenariusze,
* dashboard,
* lokalną analizę ryzyka,
* grafiki torów,
* komunikaty strategiczne.

Aplikacja może zostać zaprezentowana jako praktyczny przykład wykorzystania AI do wspierania decyzji w dynamicznym środowisku wyścigowym.
