from tools.rest_countries import fetch_country_data
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from graph.state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

SUPPORTED_FIELDS = [
    "capital",
    "population",
    "currency",
    "region",
    "languages"
]

def intent_extraction_node(state: AgentState) -> AgentState:
    question = state["question"]

    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_template(
        """
Extract the country and requested fields from the user question.

User question:
{question}

Supported fields:
capital, population, currency, region, languages

Return JSON in this format:
{{
 "country": "<country name>",
 "fields": ["field1", "field2"]
}}
"""
    )

    chain = prompt | llm | parser

    try:
        result = chain.invoke({"question": question})

        state["country"] = result.get("country")
        state["fields"] = result.get("fields")

    except Exception as e:
        state["error"] = f"Intent extraction failed: {str(e)}"

    return state


def country_api_node(state: AgentState) -> AgentState:
    country = state.get("country")

    if not country:
        state["error"] = "No country identified in the query."
        return state

    data = fetch_country_data(country)

    if not data:
        state["error"] = f"Could not find data for country: {country}"
        return state

    state["api_data"] = data

    return state

def answer_synthesis_node(state: AgentState) -> AgentState:

    if state.get("error"):
        return state

    data = state.get("api_data")
    fields = state.get("fields")

    if not data or not fields:
        state["error"] = "Missing API data or requested fields."
        return state

    extracted = {}

    for field in fields:

        if field == "capital":
            extracted["capital"] = data.get("capital", ["Unknown"])[0]

        elif field == "population":
            extracted["population"] = data.get("population")

        elif field == "currency":
            currencies = data.get("currencies", {})
            if currencies:
                extracted["currency"] = list(currencies.values())[0]["name"]

        elif field == "region":
            extracted["region"] = data.get("region")

        elif field == "languages":
            langs = data.get("languages", {})
            extracted["languages"] = ", ".join(langs.values())

    state["extracted_data"] = extracted

    country = state.get("country")

    answer_parts = []

    for key, value in extracted.items():

        if key == "population":
            answer_parts.append(f"The population of {country} is {value:,}")

        else:
            answer_parts.append(f"The {key} of {country} is {value}")

    state["answer"] = ". ".join(answer_parts) + "."

    return state