'use strict'; 
/* 
  'use strict' hilft, häufige Fehler früh zu erkennen 
  (z. B. ungewollte globale Variablen). 
*/

/* ----------------------------------------------------
   1) DOM-REFERENZEN HOLEN
   - Wir suchen die Elemente, die wir später verändern oder anklicken.
   - querySelector nimmt einen CSS-Selektor (wie in CSS).
---------------------------------------------------- */

// Zitat-Text der KI (im HTML: <blockquote class="quote"><p>…</p></blockquote>)
const quote = document.querySelector('.quote p');

// Erster <p> direkt NACH der Überschrift „Kurator*in antwortet …“
// (im HTML steht ein <h2> und danach ein <p> – der Selektor 'h2 + p' greift genau diesen)
const curator = document.querySelector('h2 + p');

// Die beiden Buttons, die wir im HTML eingefügt haben:
const btnSwap   = document.getElementById('btnSwap');    // tauscht Texte zwischen KI & Kurator*in
const btnAccent = document.getElementById('btnAccent');  // ändert die Akzentfarbe (CSS-Variable)

// Farbliste für den Wechsel der Akzentfarbe (CSS-Variable --accent)
const accents = ['#0b5cff', '#d6336c', '#008f5a', '#b58900'];
let i = 0; // Merker, welche Farbe aktuell aktiv ist (Index in 'accents')

/* ----------------------------------------------------
   3) EVENT-LISTENER HINZUFÜGEN
   - addEventListener('click', handler) reagiert auf Mausklicks
   - Im Handler ändern wir den DOM (Text) oder CSS-Variablen
---------------------------------------------------- */

// SAFETY: Erst prüfen, ob die Elemente existieren, bevor wir Listener registrieren
if (btnSwap && quote && curator) {
  btnSwap.addEventListener('click', () => {
    /* 
      Beim Klick: Texte zwischen KI und Kurator*in tauschen.
      1) Aktuellen Text der KI-Zeile zwischenspeichern
      2) KI-Text durch Kurator*in-Text ersetzen
      3) Kurator*in-Text durch den alten KI-Text ersetzen
    */
    const kiTextAktuell = quote.textContent;
    quote.textContent   = curator.textContent;
    curator.textContent = kiTextAktuell;

    // Optionales Feedback in der Konsole, gut für Debugging:
    console.log('Texte getauscht: KI ↔ Kurator*in');
  });
} else {
  console.warn('Hinweis: btnSwap, quote oder curator wurde nicht gefunden – bitte HTML prüfen.');
}

if (btnAccent) {
  btnAccent.addEventListener('click', () => {
    /*
      Beim Klick: CSS-Variable --accent ändern.
      - document.documentElement ist das <html>-Element
      - style.setProperty('--accent', wert) setzt zur Laufzeit eine Variable
      - UI reagiert sofort, wenn in CSS var(--accent) genutzt wird
    */
    i = (i + 1) % accents.length; // zum nächsten Farbwert springen (Ring)
    const next = accents[i];

    // Globale CSS-Variable setzen:
    document.documentElement.style.setProperty('--accent', next);

    console.log('Akzentfarbe gewechselt auf', next);
  });
} else {
  console.warn('Hinweis: btnAccent wurde nicht gefunden – bitte HTML prüfen.');
}

