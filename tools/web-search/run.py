import requests
from pydantic import BaseModel

class SearchResult(BaseModel):
    index: int
    title: str
    content: str
    url: str

class SearchResults(BaseModel):
    results: str

def search(query: str, searxng_url: str = "http://searxng:8080", results: int = 100) -> SearchResults:
    try:
        response = requests.get(
            f"{searxng_url}/search",
            params={"q": query, "format": "json"},
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        search_results = response.json().get("results", [])

        if not search_results:
            return SearchResults(results=f"No results found!")

        formatted_results = ""

        for i, result in enumerate(search_results[:results], 1):
            title = result.get("title", "No title")
            snippet = result.get("content", "No snippet available")
            link = result.get("url", "No URL available")
            formatted_results += f"{i}. {title}\n   {snippet}\n   URL: {link}\n\n"

        return SearchResults(results=formatted_results)
    except Exception as e:
        return SearchResults(results=f"An error occurred while searching SearXNG: {str(e)}")
