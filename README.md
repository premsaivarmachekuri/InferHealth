2# 🏥 InferHealth: Production-Grade Medical Agent

InferHealth is a state-of-the-art AI medical assistant built with **LangGraph**, **FastAPI**, and **ChromaDB**. It uses a ReAct (Reasoning + Action) pattern to retrieve medical knowledge, find nearby hospitals, and perform web searches to provide accurate, context-aware health information.

![Production Ready](https://img.shields.io/badge/Status-Production--Ready-green)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)

---

## 🚀 Features

- **Inteligent Medical Q&A**: Uses RAG (Retrieval-Augmented Generation) over a local medical dataset.
- **Geospatial Hospital Search**: Finds the nearest medical facilities based on user location and specialty using Haversine distance.
- **Dynamic Web Search**: Perforated real-time web lookups via Serper API for the latest health news.
- **Production Architecture**: Layered design separating API, Business Logic, Agent Orchestration, and Utilities.

---

## 🛠️ Tech Stack

- **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph)
- **API Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **LLM Support**: Groq (Llama 3.1) / OpenAI
- **Search**: Serper API
- **Tooling**: `uv` for lightning-fast dependency management

---

## 📂 Project Structure

```text
├── app/
│   ├── api/v1/          # REST API endpoints
│   ├── core/
│   │   ├── config.py    # Centralized configuration & settings
│   │   ├── agents/      # LangGraph state machine & AI tools
│   │   └── prompts/     # Externalized system prompts
│   ├── services/        # Business logic (Medical & Data services)
│   └── utils/           # Shared helpers (Geocoding/Math)
├── data/                # CSV Data (Hospitals, Medical QA)
├── main.py              # Local CLI Entry point
└── requirements.txt     # Dependency list
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.13+ 
- [uv](https://github.com/astral-sh/uv) (Recommended) or `pip`

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/InferHealth.git
cd InferHealth
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
OPEN_AI_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
SERPER_API_KEY=your_serper_key
GEOCODE_API_KEY=your_geocode_key
```

### 4. Install Dependencies
```bash
uv sync
# OR
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Option A: Local CLI Mode (Testing)
Run the agent directly in your terminal to see the ReAct thought process:
```bash
python main.py
```

### Option B: Production API Mode
Start the FastAPI server:
```bash
uvicorn app.api.v1.endpoints:app --reload
```
View the interactive API docs at: `http://127.0.0.1:8000/docs`

---

## 🧪 API Usage Example

**Request:**
```powershell
curl.exe -X POST "http://127.0.0.1:8000/v1/chat" `
  -H "Content-Type: application/json" `
  -d '{"query": "Where is the nearest cardiologist in New York?"}'
```

**Response:**
```json
{
  "response": "The nearest cardiologist is at NYU Langone Health, located 1.2km from you.",
  "steps": 3
}
```

---

## ⚖️ Disclaimer
*InferHealth is an AI-powered assistant for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.*

---
Designed with ❤️ by Premsai Varma
