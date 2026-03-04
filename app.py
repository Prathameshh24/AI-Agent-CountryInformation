from fastapi import FastAPI
from pydantic import BaseModel

from graph.agent_graph import build_agent

app = FastAPI(title="Country Information AI Agent")

# Build the LangGraph agent
agent = build_agent()


class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Country Information AI Agent is running",
        "docs": "/docs",
        "usage": "Send a POST request to /ask with a question about a country"
    }


@app.post("/ask")
def ask_country_agent(request: QuestionRequest):

    state = {
        "question": request.question,
        "country": None,
        "fields": None,
        "api_data": None,
        "extracted_data": None,
        "answer": None,
        "error": None
    }

    result = agent.invoke(state)

    if result.get("error"):
        return {"error": result["error"]}

    return {"answer": result["answer"]}