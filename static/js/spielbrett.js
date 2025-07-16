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
            // dynamisch alles neu aufbauen
            aktualisiereSpielbrett(res);
          }
          else if (res.status === "fertig") {
            // Spielende → Gewinnerseite
            window.location.href = res.redirect;
          }
          else {
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

  // Dynamische Aktualisierung des Spielbretts
  function aktualisiereSpielbrett(res) {
      const { next_player, spieler } = res;

      // 1) Header-Badges updaten
      document.querySelectorAll(".player-badge").forEach(badge => {
        const tid = parseInt(badge.dataset.teilnehmerId, 10);
        const data = spieler.find(s => s.teilnehmer_id === tid);
        if (!data) return;
        // Punkte aktualisieren
        badge.querySelector(".punkte").textContent = data.punkte;

        // aktiver Spieler?
        if (tid === next_player) {
          badge.classList.add("bg-red-500","text-white");
          badge.classList.remove("bg-gray-200","text-gray-600");
        } else {
          badge.classList.remove("bg-red-500","text-white");
          badge.classList.add("bg-gray-200","text-gray-600");
        }
      });

      // 2) Spielfläche wechseln: nur das erste .grid > div ist aktiv
      //    Wir gehen davon aus, dass die Spielerfelder in der gleichen Reihenfolge wie badges aufgebaut sind.
      const felder = Array.from(document.querySelectorAll(".grid > div"));
      felder.forEach((feld, idx) => {
        const tId = parseInt(feld.dataset.teilnehmerId, 10);
        if (tId === next_player) {
          feld.classList.remove("opacity-50");
          feld.querySelectorAll("button[data-kategorie]").forEach(b=>b.disabled=false);
        } else {
          feld.classList.add("opacity-50");
          feld.querySelectorAll("button[data-kategorie]").forEach(b=>b.disabled=true);
        }
      });

      // 3) Würfel‑UI zurücksetzen
      currentWuerfel = [];
      lockedDice.fill(false);
      document.querySelectorAll(".dice-row img").forEach(img => {
        img.classList.remove("ring-4","ring-yellow-400");
        img.src = img.src.replace("-white.svg",".svg"); // ggf. Theme‑SVG anpassen
      });
      document.getElementById("spiel-controls").classList.add("hidden");
      document.getElementById("btn-wuerfeln").classList.remove("hidden");

      // 4) Kategorie-Buttons löschen & neu berechnen bei erstem Wurf
      document.querySelectorAll("[data-kategorie]").forEach(btn => {
        btn.textContent = "0";
        btn.classList.remove("ring","ring-yellow-400","ring-red-500","cursor-pointer","hover:ring-2");
      });
    }

  attachWurfListener("#btn-wuerfeln");
  attachWurfListener("#spiel-controls button");
});