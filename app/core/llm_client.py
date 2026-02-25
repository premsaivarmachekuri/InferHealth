import openai
from app.core.config import settings

client_llm = openai.OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url=settings.GROQ_BASE_URL
)

def get_llm_response(prompt: str, model: str = settings.DEFAULT_MODEL) -> str:
    """
    Production-ready wrapper for LLM calls with error handling.
    """
    try:
        response = client_llm.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        # In production, we would log this to a proper observability tool
        print(f"Error calling LLM: {str(e)}")
        return f"Error: {str(e)}"
