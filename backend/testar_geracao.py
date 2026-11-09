
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

cliente = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

try:
    resposta = cliente.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        contents="Explique em duas frases o que é uma equação do segundo grau."
    )

    print("RESPOSTA DO GEMINI:")
    print(resposta.text)

except Exception as erro:
    print("TIPO DO ERRO:", type(erro).__name__)
    print("DETALHES:", str(erro).replace(os.environ["GEMINI_API_KEY"], "[CHAVE OCULTA]"))
