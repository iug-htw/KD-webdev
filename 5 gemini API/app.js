// ❗ Demo only — do NOT ship real keys in frontend code.
const API_KEY = 'your API key here';
const API_BASE = 'https://generativelanguage.googleapis.com/v1';   // ← v1 (not v1beta)
const MODEL    = 'gemini-2.5-flash';                               // ← current model id

async function askGemini(prompt) {
  const url = `${API_BASE}/models/${MODEL}:generateContent?key=${API_KEY}`;
  const body = { contents: [{ role: 'user', parts: [{ text: prompt }]}] };

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type':'application/json' },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  const data = await res.json();
  return data.candidates?.[0]?.content?.parts?.map(p => p.text).join('') || '(keine Antwort)';
}


document.getElementById('ask').addEventListener('click', async () => {
  const out = document.getElementById('out');
  const prompt = document.getElementById('prompt').value.trim();
  if (!prompt) return;
  out.textContent = '… Anfrage läuft';
  try { out.textContent = await askGemini(prompt); }
  catch (e) { out.textContent = 'Fehler: ' + e.message; }
});

