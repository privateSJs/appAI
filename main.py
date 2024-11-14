from utils.openai_client import get_api_key, ClientOpenAI
from config.constant import INPUT_FILE_PATH, OUTPUT_FILE_PATH

def init_simple_app():
    api_key = get_api_key()
    if api_key:
        client = ClientOpenAI(api_key)
        text_content = client.read_file(INPUT_FILE_PATH)
        if text_content:
            converted_content = client.api_convert_text(text_content)
            client.save_file(OUTPUT_FILE_PATH, converted_content)


if __name__ == '__main__':
    init_simple_app()
