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

  // 🔄 Würfeln-Button-Logik (hook in dice.js oder dupliziere Roll-Logik)
  document.getElementById("btn-wuerfeln")?.addEventListener("click", () => {
    // Warte kurz bis dice-Werte gezeichnet sind
    setTimeout(() => {
      sendeWurfZurBerechnung(window.currentWuerfel);
    }, 100);
  });

  // Zweit- und Drittwurf-Button (innerhalb #spiel-controls)
  document.querySelector("#spiel-controls button")?.addEventListener("click", () => {
    setTimeout(() => {
      sendeWurfZurBerechnung(window.currentWuerfel);
    }, 100);
  });

  // SPIELEN-Button (Aktion speichern folgt später)
  document.querySelector("#spiel-controls button:last-child")?.addEventListener("click", () => {
    // TODO: Ausgewählte Kategorie speichern und Spieler wechseln
    console.log("Ausgewählte Kategorie speichern – folgt");
  });
});