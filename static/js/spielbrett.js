// spielbrett.js
document.addEventListener("DOMContentLoaded", () => {
  const punktButtons = document.querySelectorAll("[data-kategorie]");
  const spielenButton = document.querySelector("#spiel-controls button:last-child");
  let currentWuerfel = [];
  let gewaehlteKategorie = null;

  window.sendeWurfZurBerechnung = function (wuerfel) {
    currentWuerfel = wuerfel;
    fetch("/ajax/punkte-berechnung", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ wuerfel })
    })
      .then(res => res.json())
      .then(punkte => aktualisierePunktefelder(punkte))
      .catch(err => console.error("Fehler bei Punkte-Berechnung:", err));
  };

  function aktualisierePunktefelder(punkte) {
    // Alle Felder zurücksetzen
    punktButtons.forEach(btn => {
      btn.textContent = "0";
      btn.classList.remove("ring", "ring-yellow-400", "cursor-pointer", "hover:ring-2", "ring-green-400");
    });

    const spielfeld = document.querySelector(".grid > div");

    Object.entries(punkte).forEach(([kategorie, punktzahl]) => {
      const button = spielfeld.querySelector(`[data-kategorie="${kategorie}"]`);
      if (button) {
        button.textContent = punktzahl;
        button.classList.add("cursor-pointer");
        if (punktzahl > 0) {
          button.classList.add("ring", "ring-yellow-400", "hover:ring-2");
        }
      }
    });

    // Auswahl zurücksetzen
    gewaehlteKategorie = null;
    spielenButton.disabled = true;
    spielenButton.classList.add("opacity-50", "cursor-not-allowed");
  }

  // Kategorieauswahl
  punktButtons.forEach(button => {
    button.addEventListener("click", () => {
      if (!button.classList.contains("cursor-pointer")) return;

      const spielfeld = document.querySelector(".grid > div");
      const alleButtons = spielfeld.querySelectorAll("[data-kategorie]");

      // Vorherige Auswahl aufheben
      alleButtons.forEach(btn => btn.classList.remove("ring-green-400"));

      // Auswahl merken und markieren
      button.classList.add("ring-green-400");
      gewaehlteKategorie = button.dataset.kategorie;

      // Spielen-Button aktivieren
      spielenButton.disabled = false;
      spielenButton.classList.remove("opacity-50", "cursor-not-allowed");
    });
  });

  // SPIELEN-Button
  spielenButton?.addEventListener("click", () => {
    if (!gewaehlteKategorie || !currentWuerfel.length) return;

    const button = document.querySelector(`[data-kategorie="${gewaehlteKategorie}"]`);
    const punkt = parseInt(button.textContent);

    fetch("/ajax/zug-speichern", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        kategorie: gewaehlteKategorie,
        punkte: punkt,
        wuerfel: currentWuerfel
      })
    })
      .then(r => r.json())
      .then(res => {
        if (res.status === "ok") {
          button.classList.remove("cursor-pointer", "hover:ring-2", "ring", "ring-yellow-400");
          button.classList.add("opacity-50");
          spielenButton.disabled = true;
          spielenButton.classList.add("opacity-50", "cursor-not-allowed");
          console.log("Zug gespeichert – nächster Spieler folgt");
          location.reload(); // Temporär bis zur echten Spielerwechsel-Logik
        } else {
          alert("Fehler: " + res.msg);
        }
      })
      .catch(console.error);
  });

  // 🎲 Eventlistener für beide Würfel-Buttons
  function attachWurfListener(buttonSelector) {
    const btn = document.querySelector(buttonSelector);
    if (!btn) return;
    btn.addEventListener("click", () => {
      setTimeout(() => {
        console.log("Aktuelle Würfelwerte:", window.currentWuerfel);
        sendeWurfZurBerechnung(window.currentWuerfel);
      }, 50);
    });
  }

  attachWurfListener("#btn-wuerfeln");
  attachWurfListener("#spiel-controls button");
});