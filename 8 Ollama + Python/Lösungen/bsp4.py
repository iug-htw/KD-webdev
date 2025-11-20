import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
from tkinter import scrolledtext

# SSL-Warnungen unterdrücken (nur für Testumgebungen!)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

OLLAMA_BASE_URL = "https://f2ki-h100-1.f2.htw-berlin.de:11435"

SYSTEM_PROMPT = "Du bist ein grummeliger Assistent der in Reimen antwortet. "

# Chat-Verlauf für die API (Ollama-Format)
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def ask_ollama_chat(model_name: str, messages_list):
    """
    Ruft das /api/chat-Endpoint von Ollama auf und gibt die Antwort zurück.
    messages_list ist eine Liste von {"role": "...", "content": "..."}.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model_name,
        "messages": messages_list,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=120, verify=False)
    response.raise_for_status()
    data = response.json()

    # Bei /api/chat steckt die Antwort normalerweise in data["message"]["content"]
    return data.get("message", {}).get("content", "")


def send_message(event=None):
    global messages

    model_name = model_entry.get().strip()
    user_text = input_entry.get().strip()

    if not model_name:
        append_to_chat("System", "Bitte zuerst einen Modellnamen eingeben.")
        return

    if not user_text:
        return

    # Eingabefeld leeren
    input_entry.delete(0, tk.END)

    # Im Chatfenster anzeigen
    append_to_chat("Du", user_text)

    # In den API-Verlauf einfügen
    messages.append({"role": "user", "content": user_text})

    try:
        bot_reply = ask_ollama_chat(model_name, messages)
    except Exception as e:
        append_to_chat("System", f"Fehler bei der Anfrage: {e}")
        return

    # Antwort anzeigen
    append_to_chat("Bot", bot_reply)

    # Antwort auch in den Verlauf übernehmen
    messages.append({"role": "assistant", "content": bot_reply})


def append_to_chat(sender: str, text: str):
    chat_box.insert(tk.END, f"{sender}: {text}\n")
    chat_box.see(tk.END)




# --- GUI aufbauen ---

root = tk.Tk()
root.title("Ollama Chat")

# Modell-Eingabe
model_label = tk.Label(root, text="Modellname:")
model_label.pack(anchor="w", padx=5, pady=(5, 0))

model_entry = tk.Entry(root, width=40)
model_entry.pack(fill="x", padx=5)
model_entry.insert(0, "qwen3:1.7b")  # z.B. aus deiner Liste

# Chat-Verlauf
chat_box = scrolledtext.ScrolledText(root, height=18, state="normal")
chat_box.pack(fill="both", expand=True, padx=5, pady=5)

# Unterer Bereich: Eingabe + Button
input_frame = tk.Frame(root)
input_frame.pack(fill="x", padx=5, pady=(0, 5))

input_entry = tk.Entry(input_frame)
input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
input_entry.bind("<Return>", send_message)  # Enter schickt Nachricht

send_button = tk.Button(input_frame, text="Senden", command=send_message)
send_button.pack(side="right")

# Fokus ins Eingabefeld
input_entry.focus()

if __name__ == "__main__":
    root.mainloop()

