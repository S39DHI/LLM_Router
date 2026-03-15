import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(question: str, model_used: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model_used,
            messages=[{"role": "user", "content": question}],
            max_tokens=256
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI Error: {str(e)}"