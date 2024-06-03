import requests
import json
from utils.prompts import VideoPrompts
from config import *

def get_response_from_cg(topic):
    cg_prompt=VideoPrompts.general__english_prompt
    cg_prompt=str(cg_prompt)
    cg_prompt=cg_prompt.format(topic=topic)

    api_key=OPENAI_API_KEY
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Or whichever model you're using, e.g., "gpt-3.5-turbo"
        "messages": [
                {"role": "system", "content": "You are a helpful assistant designed to answer the user input and give the output in the required JSON format."},
                {"role": "user", "content": cg_prompt}
            ],
        "temperature": 0.7,  # Adjust for creativity. Closer to 1.0 makes the responses more creative.
        "max_tokens": 1000,  # Adjust based on how long you expect the response to be
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        # Parsing the response content
        response_data = response.json()
        response_data=response_data["choices"][0]["message"]["content"]
        print(f"This is the Response Data from the LLM:  {response_data}")
        return response_data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


