from openai import OpenAI
import os

# Initialize Ollama client
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def call_llm(prompt: str) -> str:
    """Call Ollama API with Llama 3.2 to analyze text
    
    Args:
        prompt (str): Input prompt for the model
        
    Returns:
        str: Model response
    """
    try:
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling LLM API: {str(e)}")
        return ""

if __name__ == "__main__":
    # Test LLM call
    response = call_llm("What is web crawling?")
    print("Response:", response)
