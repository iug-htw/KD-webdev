// ❗ Demo only — do NOT ship real keys in frontend code.
const API_KEY = 'api-key-here';  // ← REPLACE with your API key
const API_BASE = 'https://generativelanguage.googleapis.com/v1';   // ← v1 (not v1beta)
const MODEL    = 'gemini-2.5-flash-lite';                               // ← current model id
// neu Chat History
let chatHistory = []; 


function buildPromptWithHistory(userText) {
  const historyText = chatHistory
    .map(m => `${m.role.toUpperCase()}: ${m.text}`)
    .join('\n');

  const current = `USER: ${userText || 'Describe the image.'}`;

  return historyText ? historyText + '\n' + current : current;
}

// --- helper: file -> base64 (without the "data:...;base64," prefix)
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => {
      const base64 = String(r.result).split(',')[1]; // strip header
      resolve(base64);
    };
    r.onerror = reject;
    r.readAsDataURL(file);
  });
}

// --- ask Gemini with image + text
async function askGeminiWithImage(file, textPrompt) {
  const base64 = await fileToBase64(file);
  const url = `${API_BASE}/models/${MODEL}:generateContent?key=${API_KEY}`;


  // Prompt inkl. Verlauf bauen
  const finalPrompt = buildPromptWithHistory(textPrompt);

  const body = {
    contents: [{
      role: 'user',
      parts: [
        { text: finalPrompt },
        { inline_data: { mime_type: file.type || 'image/png', data: base64 } }
      ]
    }]
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type':'application/json' },
    body: JSON.stringify(body)
  });

  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  const data = await res.json();

  // HIER erst die Antwort extrahieren und in `answer` speichern
  const answer =
    data.candidates?.[0]?.content?.parts?.map(p => p.text).join('') || '(no answer)';

  // Verlauf aktualisieren – jetzt existiert `answer`
  chatHistory.push({
    role: 'user',
    text: textPrompt || 'Describe the image.'
  });
  chatHistory.push({
    role: 'assistant',
    text: answer
  });
  console.log(finalPrompt); // optional

  return {answer, finalPrompt};
}




// --- wire up the button
document.getElementById('sendImg').addEventListener('click', async () => {
  const f = document.getElementById('img').files?.[0];
  const p = document.getElementById('imgPrompt').value.trim();
  const out = document.getElementById('imgOut');


  if (!f) { out.textContent = 'Please choose an image.'; return; }
  out.textContent = '… sending';
   try {
    const { answer, finalPrompt } = await askGeminiWithImage(f, p);

    // Hier zeigst du nur den Prompt an
    out.textContent = finalPrompt+'\n'+answer;

    // Optional: Falls du irgendwann auch die Antwort brauchst, ist sie in `answer`
    console.log('Antwort erhalten von Gemini:', answer);
  } catch (e) {
    out.textContent = 'Error: ' + e.message;
  }
});
