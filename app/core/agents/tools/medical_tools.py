from langchain_community.utilities import GoogleSerperAPIWrapper
from app.core.config import settings
from app.services.medical_service import medical_service

# Initialize Serper
search = GoogleSerperAPIWrapper(serper_api_key=settings.SERPER_API_KEY)

def retrieve_context_tool(query: str):
    print(f"--- TOOL: Retrieving Context for '{query}' ---")
    return medical_service.retrieve_context(query)

def search_hospital_tool(user_location: str, specialty: str = None, top_n: int = 3):
    print(f"--- TOOL: Searching Hospitals near '{user_location}' ---")
    return medical_service.search_nearest_hospital(user_location, specialty, top_n)

def web_search_tool(query: str):
    print(f"--- TOOL: Web Searching for '{query}' ---")
    search_results = search.run(query=query)
    return {"context": search_results, "source": "Web Search"}

def ask_user_tool(question: str):
    print(f"--- TOOL: Agent needs more info: {question} ---")
    return {
        "context": f"PLEASE PROVIDE MORE INFO: {question}", 
        "source": "User Query Required"
    }
