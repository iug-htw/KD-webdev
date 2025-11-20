import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# SSL-Warnungen unterdrücken (nur für Testumgebungen!)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

OLLAMA_BASE_URL = "https://f2ki-h100-1.f2.htw-berlin.de:11435"

def list_models():
    url = f"{OLLAMA_BASE_URL}/api/tags"
    print("Abrufen der Modelle von:", url)

    response = requests.get(url, timeout=30, verify=False)
    response.raise_for_status()

    data = response.json()

    print("\nVerfügbare Modelle:")
    for model in data.get("models", []):
        print(" -", model.get("name"))

if __name__ == "__main__":
    list_models()
