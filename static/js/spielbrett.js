document.addEventListener("DOMContentLoaded", () => {
  const punktButtons = document.querySelectorAll("[data-kategorie]");
  let currentWuerfel = [];

  window.sendeWurfZurBerechnung = function(wuerfel) {
    fetch("/ajax/punkte-berechnung", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ wuerfel: wuerfel })
    })
    .then(res => res.json())
    .then(punkte => {
      aktualisierePunktefelder(punkte);
    })
    .catch(err => console.error("Fehler bei Punkte-Berechnung:", err));
  }

  function aktualisierePunktefelder(punkte) {
    // Alle Felder zurücksetzen
    punktButtons.forEach(btn => {
      btn.textContent = "0";
      btn.classList.remove("ring", "ring-yellow-400", "cursor-pointer", "hover:ring-2");
    });

    // Nur für aktuellen Spieler (erste Spielfläche)
    const spielfeld = document.querySelector(".grid > div");

    Object.entries(punkte).forEach(([kategorie, punktzahl]) => {
      const button = spielfeld.querySelector(`[data-kategorie="${kategorie}"]`);
      if (button) {
        button.textContent = punktzahl;
        if (punktzahl > 0) {
          button.classList.add("ring", "ring-yellow-400", "cursor-pointer", "hover:ring-2");
        }
      }
    });
  }

    // 🎲 Wenn ein Wurf abgeschlossen ist (Start- oder Folgewurf), Punkte berechnen
  function attachWurfListener(buttonSelector) {
    const btn = document.querySelector(buttonSelector);
    if (!btn) return;
    btn.addEventListener("click", () => {
      // kleine Verzögerung, damit die UI (Würfelbilder) fertig ist
      setTimeout(() => {
        console.log("Aktuelle Würfelwerte:", window.currentWuerfel);
        sendeWurfZurBerechnung(window.currentWuerfel);
      }, 50);
    });
  }

  // Haupt-Würfel-Button
  attachWurfListener("#btn-wuerfeln");
  // Erster Folgewurf-Button (innerhalb spiel-controls)
  attachWurfListener("#spiel-controls button");

  // SPIELEN-Button (Aktion speichern folgt später)
  document.querySelector("#spiel-controls button:last-child")?.addEventListener("click", () => {
    // TODO: Ausgewählte Kategorie speichern und Spieler wechseln
    console.log("Ausgewählte Kategorie speichern – folgt");
  });
});