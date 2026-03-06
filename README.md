# Country Information AI Agent

An AI agent that answers questions about countries using public data from the **REST Countries API**.

The system is implemented using **LangGraph** to orchestrate a multi-step agent workflow consisting of:

* Intent / Field Identification
* Tool Invocation
* Answer Synthesis

The agent is exposed as a **FastAPI service** and deployed publicly so it can be tested through an API endpoint.

---

# Live Demo

Video Walkthrough:

https://www.loom.com/share/f00c6f60ac1c477fa9c81fa737c4c9cc

The application is hosted on **Render** and can be tested directly.

API Homepage:

https://country-ai-agent.onrender.com/docs

You can test queries directly from the Swagger interface.

Example query:

```json
{
  "question": "What is the capital of Japan?"
}
```

Example response:

```json
{
  "answer": "The capital of Japan is Tokyo."
}
```

---

# Example Questions

The AI agent can answer questions such as:

* What is the population of Germany?
* What currency does Japan use?
* What is the capital and population of Brazil?
* What languages are spoken in Spain?

---

# System Architecture

The system follows a **structured LangGraph workflow** rather than relying on a single prompt.

```
User Query
   │
   ▼
FastAPI Endpoint (/ask)
   │
   ▼
LangGraph Agent Workflow
   │
   ├── Intent Extraction Node
   │       └─ Uses Gemini to identify:
   │           • Country name
   │           • Requested fields
   │
   ├── Country API Tool Node
   │       └─ Calls REST Countries API
   │           https://restcountries.com/v3.1/name/{country}
   │
   └── Answer Synthesis Node
           └─ Extracts requested fields
           └─ Formats human-readable response
   │
   ▼
Final Response
```

### Step 1 — Intent Identification

The user question is analyzed using the Gemini model to extract:

* country name
* requested fields

Example:

Question:

```
What is the capital of Brazil?
```

Extracted intent:

```json
{
 "country": "Brazil",
 "fields": ["capital"]
}
```

---

### Step 2 — Tool Invocation

The agent retrieves country information using the public REST Countries API.

```
https://restcountries.com/v3.1/name/{country}
```

Example request:

```
https://restcountries.com/v3.1/name/japan
```

The API returns structured data about the country including:

* capital
* population
* currencies
* region
* languages

---

### Step 3 — Answer Synthesis

The relevant fields are extracted from the API response and formatted into a human-readable answer.

Example:

```
The capital of Japan is Tokyo.
```

---

# Tech Stack

* Python
* LangGraph
* LangChain
* Gemini API
* FastAPI
* REST Countries API
* Render (deployment)

---

# Project Structure

```
country-ai-agent
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── graph
│   ├── agent_graph.py
│   ├── nodes.py
│   └── state.py
│
└── tools
    └── rest_countries.py
```

### Component Description

| File               | Description                                      |
| ------------------ | ------------------------------------------------ |
| app.py             | FastAPI application and API endpoints            |
| agent_graph.py     | LangGraph workflow definition                    |
| nodes.py           | Agent nodes (intent, API call, answer synthesis) |
| state.py           | Shared state across graph nodes                  |
| rest_countries.py  | REST Countries API integration                   |

---

# Running the Project Locally

### 1. Clone the Repository

```
git clone https://github.com/Prathameshh24/AI-Agent-CountryInformation.git
cd country-ai-agent
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

---

### 3. Activate Virtual Environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

---

### 4. Install Dependencies

```
pip install -r requirements.txt
```

---

### 5. Add Gemini API Key

Create a `.env` file in the root directory.

```
GOOGLE_API_KEY=your_gemini_api_key
```

Generate a key from:

https://aistudio.google.com/app/apikey

---

### 6. Start the API Server

```
uvicorn app:app --reload
```

Open the documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Usage

Endpoint:

```
POST /ask
```

Example Request

```json
{
 "question": "What is the population of Germany?"
}
```

Example Response

```json
{
 "answer": "The population of Germany is 83,200,000."
}
```

---

# Root Endpoint

The root endpoint confirms the service is running.

```
GET /
```

Example response:

```json
{
 "message": "Country Information AI Agent is running",
 "docs": "/docs",
 "usage": "Send a POST request to /ask with a country question"
}
```

---

# Error Handling

The system gracefully handles invalid inputs.

Example:

Question:

```
What is the population of Wakanda?
```

Response:

```json
{
 "error": "Could not find data for country: Wakanda"
}
```

---

## Deployment

The API is deployed using Render and is publicly accessible.

Live API:

https://country-ai-agent.onrender.com/docs

---

# Production Considerations

The project was designed with production principles:

* modular architecture
* separation of agent nodes and tools
* stateless service
* external API integration
* structured workflow using LangGraph

---

# Limitations

* Only supports fields:

  * capital
  * population
  * currency
  * region
  * languages
* Depends on availability of REST Countries API
* No caching layer implemented
* No request rate limiting

---

# Possible Future Improvements

* Add caching for API responses
* Expand supported country attributes
* Add monitoring and logging
* Implement rate limiting
* Improve response formatting using LLM summarization

---

# Assignment Requirement Mapping

| Requirement        | Implementation                  |
| ------------------ | ------------------------------- |
| LangGraph workflow | Implemented in `agent_graph.py` |
| Intent extraction  | Gemini model                    |
| Tool invocation    | REST Countries API              |
| Answer synthesis   | Structured data processing      |
| Production service | FastAPI deployment              |
| Hosted API         | Render deployment               |

---

# Author

Prathmesh Kadam

---

# License

This project is for demonstration and educational purposes.
