import sys
from pathlib import Path
import os
from duckduckgo_search import DDGS

# Add parent directory to path to import shared config
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config_shared import call_llm as shared_call_llm, LLMConfig

def call_llm(prompt, config: LLMConfig = None):
    """Call LLM with prompt string"""
    messages = [{"role": "user", "content": prompt}]
    return shared_call_llm(messages, config)

def search_web_duckduckgo(query):
    results = DDGS().text(query, max_results=5)
    # Convert results to a string
    results_str = "\n\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results])
    return results_str

def search_web_brave(query):

    url = f"https://api.search.brave.com/res/v1/web/search?q={query}"
    api_key = "your brave search api key"

    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": api_key
    }

    import requests
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data['web']['results']
        results_str = "\n\n".join([f"Title: {r['title']}\nURL: {r['url']}\nDescription: {r['description']}" for r in results])     
    else:
        print(f"Request failed with status code: {response.status_code}")
    return results_str
    
if __name__ == "__main__":
    config = LLMConfig()
    
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    print(f"## Using {config.provider} with {config.model}")
    response = call_llm(prompt, config)
    print(f"## Response: {response}")

    print("## Testing search_web")
    query = "Who won the Nobel Prize in Physics 2024?"
    print(f"## Query: {query}")
    results = search_web_duckduckgo(query)
    print(f"## Results: {results}")
