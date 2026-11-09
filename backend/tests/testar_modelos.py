import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    chave = os.getenv("GEMINI_API_KEY")
    if not chave:
        print("Configure GEMINI_API_KEY no backend/.env para listar modelos.")
        return

    cliente = genai.Client(api_key=chave)
    print("Modelos disponíveis para gerar texto:\n")
    for modelo in cliente.models.list():
        if "generateContent" in (modelo.supported_actions or []):
            print(modelo.name)


if __name__ == "__main__":
    main()
