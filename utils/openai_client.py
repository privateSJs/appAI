import os
from openai import OpenAI, OpenAIError, AuthenticationError, APIConnectionError, RateLimitError
from dotenv import load_dotenv


def get_api_key():
    """Pobiera klucz API z pliku .env i zwraca go. Jeśli klucz nie istnieje, zwraca None."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Błąd: Klucz API nie został znaleziony.")
        return None
    return api_key


class ClientOpenAI:
    def __init__(self, api_key):
        if api_key is None:
            raise ValueError("Klucz API jest wymagany, ale nie został dostarczony.")
        self.client = OpenAI(api_key=api_key)
        self.raw_file = None
        self.proceed_file = None

    def read_file(self, input_path):
        """Odczytuje plik i zwraca jego zawartość jako tekst."""
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f'Błąd: Plik "{input_path}" nie został znaleziony.')
        except IOError:
            print(f'Błąd: Nie można odczytać pliku "{input_path}".')

    def save_file(self, output_path, content):
        """Zapisuje przetworzony tekst do pliku w formacie UTF-8."""
        if content is None:
            print("Błąd: Brak treści do zapisania.")
            return
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Plik został zapisany pomyślnie w lokalizacji: {output_path}")
        except IOError:
            print(f'Błąd: Nie można zapisać pliku "{output_path}".')

    def api_convert_text(self, text_content):
        """Wysyła tekst do OpenAI API w celu przekształcenia go w dobrze ustrukturyzowany kod HTML."""
        if not text_content:
            print("Błąd: Brak treści do przetworzenia.")
            return None

        prompt = f"""
            Przekształć poniższy tekst w dobrze ustrukturyzowany kod HTML zgodnie z następującymi wytycznymi:

            1. Obróbka tekstu:
                - Oczyść tekst z niepotrzebnych znaków.
                - Dodaj nagłówki (np. <h1>, <h2>, <h3>) dla sekcji i podsekcji.
                - Dodaj akapity (<p>) dla zwykłych fragmentów tekstu.
                - Dodaj listy uporządkowane (<ol>) i nieuporządkowane (<ul>) dla elementów w formie list.
                - Przetłumacz tekst na język polski.

            2. Wstawienie grafik:
                - Użyj tagu <img> z atrybutem src="image_placeholder.jpg" jako miejsca na obrazy.
                - Dodaj atrybut `alt` z opisem obrazu, np. "Pies pijący mleko".
                - Użyj <figure> i <figcaption> do podpisów pod obrazkami.

            3. Ograniczenia:
                - Wygenerowany HTML ma być przeznaczony do umieszczenia wewnątrz <body> i </body>.
                - Nie dodawaj tagów <html>, <head> ani <body>. Brak kodu CSS i JavaScript.

            Tekst do przekształcenia:
            {text_content}
        """

        try:
            response = self.client.chat.completions.create(
                model='chatgpt-4o-latest',
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
            )
            return response.choices[0].message.content
        except AuthenticationError as e:
            print('Błąd podczas autoryzacji:', e)
        except APIConnectionError as e:
            print('Błąd podczas połączenia z API:', e)
        except RateLimitError:
            print('Przekroczono limit zapytań do OpenAI API.')
        except OpenAIError as e:
            print('Błąd API:', e)
        return None
