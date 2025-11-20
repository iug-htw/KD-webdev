import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
import tkinter as tk
from tkinter import scrolledtext, filedialog
import base64
import os

# SSL-Warnungen unterdrücken (nur für Testumgebung!)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

OLLAMA_BASE_URL = "https://f2ki-h100-1.f2.htw-berlin.de:11435"

def ask_ollama(model_name: str, prompt: str, image_path: str | None = None) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    # Falls ein Bild ausgewählt wurde: als base64 mitsenden
    if image_path:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload["images"] = [image_b64]

    response = requests.post(url, json=payload, timeout=60, verify=False)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")

def on_send():
    model_name = model_entry.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    img_path = selected_image_path.get().strip()

    if not model_name or not prompt:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Bitte Modell und Prompt eingeben.\n")
        return

    output_text.delete("1.0", tk.END)
    if img_path:
        output_text.insert(tk.END, f"Sende Anfrage mit Bild: {os.path.basename(img_path)}\n")
    else:
        output_text.insert(tk.END, "Sende Anfrage (ohne Bild)...\n")

    try:
        answer = ask_ollama(model_name, prompt, image_path=img_path if img_path else None)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, answer)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Fehler bei der Anfrage:\n{e}")

def on_select_image():
    path = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=[
            ("Bilddateien", "*.png;*.jpg;*.jpeg;*.webp;*.bmp"),
            ("Alle Dateien", "*.*")
        ]
    )
    if path:
        selected_image_path.set(path)
        image_label.config(text=f"Bild: {os.path.basename(path)}")
    else:
        selected_image_path.set("")
        image_label.config(text="Kein Bild ausgewählt")

# --- GUI aufbauen ---

root = tk.Tk()
root.title("Ollama Bildbeschreibung Demo")

selected_image_path = tk.StringVar()

# Modell-Eingabe
model_label = tk.Label(root, text="Modellname:")
model_label.pack(anchor="w", padx=5, pady=(5, 0))

model_entry = tk.Entry(root, width=40)
model_entry.pack(fill="x", padx=5)
model_entry.insert(0, "llama3.2-vision:11b")  # Multimodales Modell

# Bildauswahl
image_frame = tk.Frame(root)
image_frame.pack(fill="x", padx=5, pady=(5, 0))

image_button = tk.Button(image_frame, text="Bild auswählen", command=on_select_image)
image_button.pack(side="left")

image_label = tk.Label(image_frame, text="Kein Bild ausgewählt")
image_label.pack(side="left", padx=10)

# Prompt-Eingabe
prompt_label = tk.Label(root, text="Prompt (z.B. 'Beschreibe das Bild in 2 Sätzen auf Deutsch'):")
prompt_label.pack(anchor="w", padx=5, pady=(5, 0))

prompt_text = scrolledtext.ScrolledText(root, height=5)
prompt_text.pack(fill="both", expand=True, padx=5)

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
