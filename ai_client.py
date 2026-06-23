import os

import streamlit as st
from google import genai
from google.genai import types


def get_gemini_api_key():
    """
    Pobiera klucz API Gemini.

    Najpierw próbuje pobrać klucz z pliku:
    .streamlit/secrets.toml

    Jeśli go tam nie ma, sprawdza zmienną środowiskową:
    GEMINI_API_KEY
    """

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    return api_key


def extract_text_from_response(response):
    """
    Bezpiecznie wyciąga tekst z odpowiedzi Gemini.

    Najpierw sprawdza response.text.
    Jeśli tam nie ma tekstu, próbuje pobrać tekst z candidates/parts.
    """

    try:
        if hasattr(response, "text") and response.text:
            return response.text
    except Exception:
        pass

    try:
        candidates = getattr(response, "candidates", [])

        if candidates:
            content = candidates[0].content
            parts = content.parts

            texts = []

            for part in parts:
                if hasattr(part, "text") and part.text:
                    texts.append(part.text)

            if texts:
                return "\n".join(texts)

    except Exception:
        pass

    return f"""
⚠️ Model odpowiedział, ale nie udało się odczytać tekstu.

Podgląd techniczny odpowiedzi:
{response}
"""


def ask_gemini(prompt):
    """
    Wysyła prompt do Gemini API i zwraca odpowiedź tekstową.

    Aplikacja korzysta z modelu gemini-2.5-flash-lite,
    ponieważ jest szybki i dobrze nadaje się do projektu studenckiego.
    """

    api_key = get_gemini_api_key()

    if not api_key:
        return """
❌ Brak klucza API.

Dodaj klucz do pliku:

.streamlit/secrets.toml

W formacie:

GEMINI_API_KEY = "TWÓJ_KLUCZ"
"""

    try:
        client = genai.Client(api_key=api_key)

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    max_output_tokens=3000,
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=0
                    )
                )
            )

        except TypeError:
            # Fallback dla starszej wersji biblioteki google-genai,
            # gdyby thinking_config nie był obsługiwany.
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    max_output_tokens=3000
                )
            )

        return extract_text_from_response(response)

    except Exception as error:
        return f"""
❌ Wystąpił błąd podczas połączenia z Gemini API.

Szczegóły błędu:
{error}

Możliwe przyczyny:
- zły lub nieaktywny klucz API,
- przekroczony limit zapytań,
- brak internetu,
- chwilowy problem po stronie API.
"""