from typing import TypedDict, List, Optional, Dict, Any


class AgentState(TypedDict):
    # Original user query
    question: str

    # Extracted country from the question
    country: Optional[str]

    # Requested fields like population, capital, currency
    fields: Optional[List[str]]

    # Raw API response from REST Countries
    api_data: Optional[Dict[str, Any]]

    # Extracted data after processing
    extracted_data: Optional[Dict[str, Any]]

    # Final answer returned to the user
    answer: Optional[str]

    # Error message if something fails
    error: Optional[str]