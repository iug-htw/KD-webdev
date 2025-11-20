// ❗ Demo only — do NOT ship real keys in frontend code.
const API_KEY = 'YOUR_API_KEY';
const API_BASE = 'https://generativelanguage.googleapis.com/v1';   // ← v1 (not v1beta)
const MODEL    = 'gemini-2.5-flash-lite';                               // ← current model id

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
//-new: image preview
const imgInput       = document.getElementById('img');
const previewWrapper = document.getElementById('previewWrapper');
const previewImg     = document.getElementById('imgPreview');

imgInput.addEventListener('change', async () => {
  const file = imgInput.files?.[0];
  if (!file) {
    previewWrapper.style.display = 'none';
    previewImg.removeAttribute('src');
    return;
  }

  try {
    const base64 = await fileToBase64(file);            // dein Helper
    previewImg.src = `data:${file.type};base64,${base64}`;
    previewWrapper.style.display = 'block';
  } catch (e) {
    console.error('Preview error:', e);
  }
});


// --- ask Gemini with image + text
async function askGeminiWithImage(file, textPrompt) {
  const base64 = await fileToBase64(file);
  const url = `${API_BASE}/models/${MODEL}:generateContent?key=${API_KEY}`;
  const body = {
    contents: [{
      role: 'user',
      parts: [
        { text: textPrompt || 'Describe the image.' },
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
  return data.candidates?.[0]?.content?.parts?.map(p => p.text).join('') || '(no answer)';
}

// --- wire up the button
document.getElementById('sendImg').addEventListener('click', async () => {
  const f = document.getElementById('img').files?.[0];
  const p = document.getElementById('imgPrompt').value.trim();
  const out = document.getElementById('imgOut');
  
  if (!f) { out.textContent = 'Please choose an image.'; 
     return; }
    out.textContent = '… sending';
  try {
    out.textContent = await askGeminiWithImage(f, p);
  } catch (e) {
    out.textContent = 'Error: ' + e.message;
  }
});
