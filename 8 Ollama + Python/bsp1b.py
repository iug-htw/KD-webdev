import requests
import json
#neu: 
import warnings
from urllib3.exceptions import InsecureRequestWarning

# SSL-Warnungen unterdrücken (nur für Testumgebungen!)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

OLLAMA_BASE_URL = "https://f2ki-h100-1.f2.htw-berlin.de:11435"
MODEL_NAME = "llama3.1:8b"

def ask_ollama(prompt: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # easier to handle: one complete response
    }
    print("Sending request to:", url)  # debug output
    response = requests.post(url, json=payload, timeout=60, verify=False)
    #print("Status code:", response.status_code)  # debug output

    #response.raise_for_status()

    data = response.json()
    return data.get("response", "")


if __name__ == "__main__":
    prompt = "Say hello from the H100 server in one sentence."
    answer = ask_ollama(prompt)
    print("Model answer:\n", answer)
