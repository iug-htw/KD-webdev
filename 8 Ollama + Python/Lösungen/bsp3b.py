import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
from tkinter import scrolledtext

# SSL-Warnungen unterdrücken (nur für Testumgebung!)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

OLLAMA_BASE_URL = "https://f2ki-h100-1.f2.htw-berlin.de:11435"

def ask_ollama(model_name: str, prompt: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=60, verify=False)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")

def on_send():
    model_name = model_entry.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()

    if not model_name or not prompt:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Bitte Modell und Prompt eingeben.\n")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Sende Anfrage...\n")

    # Button-Text ändern
    send_button.config(text="Bitte warten...", state="disabled")
    root.update_idletasks()
    
    try:
        answer = ask_ollama(model_name, prompt)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, answer)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Fehler bei der Anfrage:\n{e}")

# --- GUI aufbauen ---

root = tk.Tk()
root.title("Ollama Demo")

# Modell-Eingabe
model_label = tk.Label(root, text="Modellname:")
model_label.pack(anchor="w", padx=5, pady=(5, 0))

model_entry = tk.Entry(root, width=40)
model_entry.pack(fill="x", padx=5)
model_entry.insert(0, "qwen3:1.7b")  # Hier Modell auswählen

# Prompt-Eingabe
prompt_label = tk.Label(root, text="Prompt:")
prompt_label.pack(anchor="w", padx=5, pady=(5, 0))

prompt_text = scrolledtext.ScrolledText(root, height=8)
prompt_text.pack(fill="both", expand=True, padx=5)
# Standardprompt einfügen
prompt_text.insert("1.0", "Erkläre KI in einem Satz auf Deutsch.")

# Senden-Button
send_button = tk.Button(root, text="Senden", command=on_send)
send_button.pack(pady=5)

# Ausgabe
output_label = tk.Label(root, text="Antwort:")
output_label.pack(anchor="w", padx=5, pady=(5, 0))

output_text = scrolledtext.ScrolledText(root, height=10)
output_text.pack(fill="both", expand=True, padx=5, pady=(0, 5))

if __name__ == "__main__":
    root.mainloop()
