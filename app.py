from fastapi import FastAPI
from pydantic import BaseModel
import logging

from graph.agent_graph import build_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app configuration
app = FastAPI(
    title="Country Information AI Agent",
    description="An AI agent built with LangGraph that answers questions about countries using the REST Countries API.",
    version="1.0.0"
)

# Build the LangGraph agent
agent = build_agent()


class QuestionRequest(BaseModel):
    question: str


@app.get("/", tags=["System"])
def home():
    return {
        "message": "Country Information AI Agent is running",
        "docs": "/docs",
        "health": "/health",
        "usage": "Send a POST request to /ask with a question about a country"
    }


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy"}


@app.post("/ask", tags=["Country Agent"])
def ask_country_agent(request: QuestionRequest):

    logger.info(f"Received question: {request.question}")

    state = {
        "question": request.question,
        "country": None,
        "fields": None,
        "api_data": None,
        "extracted_data": None,
        "answer": None,
        "error": None
    }

    try:
        result = agent.invoke(state)

        if result.get("error"):
            logger.error(result["error"])
            return {"error": result["error"]}

        return {"answer": result["answer"]}

    except Exception as e:
        logger.exception("Agent execution failed")
        return {"error": "Internal server error"}
