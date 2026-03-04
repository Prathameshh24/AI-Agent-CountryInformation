# Country Information AI Agent

An AI agent that answers questions about countries using public data from the REST Countries API.

The system is built using **LangGraph** to orchestrate an agent workflow consisting of:

1. **Intent / Field Identification**
2. **Tool Invocation**
3. **Answer Synthesis**

The agent is exposed as a **FastAPI service**, allowing users to query it through a simple API endpoint.

---

# Example Questions

The agent can answer questions such as:

* What is the population of Germany?
* What currency does Japan use?
* What is the capital and population of Brazil?

Example response:

```json
{
  "answer": "The capital of Japan is Tokyo."
}
```

---

# System Architecture

The agent follows a structured workflow using **LangGraph**.

```
User Question
      ↓
Intent Extraction (Gemini)
      ↓
REST Countries API Tool
      ↓
Answer Synthesis
      ↓
Response
```

### Workflow Steps

#### 1. Intent / Field Identification

Uses **Gemini** to extract:

* country
* requested fields

Example:

```
"What is the capital of Brazil?"
```

Extracted intent:

```json
{
 "country": "Brazil",
 "fields": ["capital"]
}
```

---

#### 2. Tool Invocation

The system queries the **REST Countries API**:

```
https://restcountries.com/v3.1/name/{country}
```

Example request:

```
https://restcountries.com/v3.1/name/japan
```

The API returns structured data about the country.

---

#### 3. Answer Synthesis

Relevant information is extracted from the API response and converted into a human-readable answer.

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

---

# Project Structure

```
country-ai-agent
│
├── app.py
├── requirements.txt
├── README.md
│
├── graph
│   ├── agent_graph.py
│   ├── nodes.py
│   └── state.py
│
├── tools
│   └── rest_countries.py
│
├── services
│
└── utils
```

### Key Components

| File              | Purpose                               |
| ----------------- | ------------------------------------- |
| app.py            | FastAPI application                   |
| agent_graph.py    | LangGraph workflow                    |
| nodes.py          | Agent nodes (intent, tool, synthesis) |
| state.py          | Shared agent state                    |
| rest_countries.py | API integration                       |

---

# Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/country-ai-agent.git
cd country-ai-agent
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate the Environment

Windows:

```bash
venv\Scripts\activate
```

Mac / Linux:

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Set the Gemini API Key

Create a `.env` file in the project root.

```
GOOGLE_API_KEY=your_gemini_api_key
```

You can generate an API key from:

```
https://aistudio.google.com/app/apikey
```

---

### 6. Run the API Server

```bash
uvicorn app:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

# API Usage

### Endpoint

```
POST /ask
```

### Example Request

```json
{
 "question": "What is the capital of Japan?"
}
```

### Example Response

```json
{
 "answer": "The capital of Japan is Tokyo."
}
```

---

# API Documentation

FastAPI provides interactive documentation.

Open in browser:

```
http://127.0.0.1:8000/docs
```

This interface allows you to test the API directly.

---

# Error Handling

The system handles invalid or unsupported inputs gracefully.

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

# Production Considerations

The system was designed following production principles:

### Modular Architecture

Separate modules for agent logic, tools, and API service.

### Stateless Design

No database required.

### API-Based Data Retrieval

Answers are grounded using the REST Countries API.

### Error Handling

Handles missing data and invalid countries.

### Extensibility

Additional fields and tools can easily be added.

---

# Deployment

The API can be deployed to cloud platforms such as:

* Render
* Railway
* Fly.io

Example deployed endpoint:

```
https://country-ai-agent.onrender.com/docs
```

This allows users to interact with the agent directly.

---

# Limitations

* Supports only the following fields:

  * capital
  * population
  * currency
  * region
  * languages
* Dependent on REST Countries API availability
* No caching implemented
* No rate limiting implemented

---

# Possible Future Improvements

* Add caching layer for API responses
* Support additional country attributes
* Implement monitoring and logging
* Add request validation and rate limiting
* Improve natural language response formatting

---

# Assignment Requirements Mapping

| Requirement             | Implementation                  |
| ----------------------- | ------------------------------- |
| LangGraph workflow      | Implemented in `agent_graph.py` |
| Intent identification   | Gemini-based extraction         |
| Tool invocation         | REST Countries API              |
| Answer synthesis        | Structured data processing      |
| Production-style design | Modular architecture + FastAPI  |
| Hosted service          | Deployable FastAPI API          |

---

# Author

Prathmesh Kadam

---

# License

This project is for demonstration and educational purposes.
