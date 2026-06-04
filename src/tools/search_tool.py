# src/tools/search_tool.py

# We import 'os' to read our API key from the .env file
import os

# We import 'load_dotenv' to load the .env file into our program
from dotenv import load_dotenv

# We import the Tavily client - this is the tool that searches the internet
from tavily import TavilyClient

# This line actually reads our .env file and makes the keys available
load_dotenv()


def search_company(company_name: str) -> dict:
    """
    Takes a company name and searches the internet for information about it.
    Returns a dictionary with search results organized by topic.
    
    Example:
        search_company("Adani Realty") 
        → returns dict with overview, news, and challenges info
    """
    
    # Create a Tavily client using our API key from .env
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # We search for THREE different things about the company
    # This gives us much richer information than one single search
    queries = [
        f"{company_name} company overview business operations India",
        f"{company_name} recent news expansion plans 2025 2026",
        f"{company_name} business challenges problems competition",
    ]
    
    # This dictionary will store all our search results
    all_results = {}
    
    # Loop through each query and search
    for query in queries:
        try:
            # Search and get top 5 results for each query
            response = client.search(query, max_results=5)
            
            # Store the results with the query as the key
            # We extract just the text content from each result
            all_results[query] = [
                {
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", "")
                }
                for r in response.get("results", [])
            ]
        except Exception as e:
            # If a search fails, we store an empty list and continue
            # This prevents one failed search from breaking everything
            print(f"Search failed for query '{query}': {e}")
            all_results[query] = []
    
    return all_results


# This section only runs if you run THIS file directly (for testing)
if __name__ == "__main__":
    # Test the function with one company
    print("Testing search tool...")
    results = search_company("Adani Realty")
    
    # Print how many results we got for each query
    for query, data in results.items():
        print(f"\nQuery: {query}")
        print(f"Results found: {len(data)}")
        if data:
            print(f"First result title: {data[0]['title']}")