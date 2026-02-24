import os
import openai
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY missing—fix your env, scrub!")

client_llm = openai.OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

def get_llm_response(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    try:
        response = client_llm.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        if "model" in str(e).lower():
            return "Model dead—switch to llama-3.1-8b-instant or check https://console.groq.com/docs/models"
        raise

prompt = "Explain the impact of GenAI on healthcare in 30 words"
print(get_llm_response(prompt))
