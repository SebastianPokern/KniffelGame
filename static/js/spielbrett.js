// static/js/spielbrett.js

document.addEventListener("DOMContentLoaded", () => {
  // Globale State-Variablen
  window.currentWuerfel = [];
  window.gewaehlteKategorie = null;
  // aktiverTeilnehmer initial aus dem Template ziehen
  const startField = document.querySelector(".player-field:not(.opacity-50)");
  window.aktiverTeilnehmer = startField
    ? Number(startField.dataset.teilnehmerId)
    : null;

  const punktButtons = document.querySelectorAll("[data-kategorie]");
  const spielenButton = document.querySelector("#spiel-controls button:last-child");

  // Ajax-Aufruf zur Punkte‑Berechnung
  window.sendeWurfZurBerechnung = function (wuerfel) {
    window.currentWuerfel = wuerfel;
    fetch("/ajax/punkte-berechnung", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ wuerfel })
    })
      .then(res => res.json())
      .then(punkte => aktualisierePunktefelder(punkte))
      .catch(err => console.error("Fehler bei Punkte-Berechnung:", err));
  };

  // Punktvorschau nach Würfelwurf
  function aktualisierePunktefelder(punkte) {
    // Reset aller Buttons
    punktButtons.forEach(btn => {
      btn.textContent = "0";
      btn.disabled = true;
      btn.classList.remove("ring", "ring-yellow-400", "hover:ring-2", "ring-green-400");
    });

    // Nur auf dem aktuellen Spielerfeld anzeigen
    const aktuellesFeld = document.querySelector(
      `.player-field[data-teilnehmer-id="${window.aktiverTeilnehmer}"]`
    );
    Object.entries(punkte).forEach(([kategorie, punktzahl]) => {
      const btn = aktuellesFeld.querySelector(`[data-kategorie="${kategorie}"]`);
      if (!btn) return;
      btn.textContent = punktzahl;
      btn.disabled = false;
      btn.classList.add("cursor-pointer");
      if (punktzahl > 0) {
        btn.classList.add("ring", "ring-yellow-400", "hover:ring-2");
      }
    });

    // Reset Kategorieauswahl
    window.gewaehlteKategorie = null;
    spielenButton.disabled = true;
    spielenButton.classList.add("opacity-50", "cursor-not-allowed");
  }

  // Kategorieauswahl auf dem aktiven Feld
  punktButtons.forEach(button => {
    button.addEventListener("click", () => {
      if (button.disabled) return;
      const feld = document.querySelector(
        `.player-field[data-teilnehmer-id="${window.aktiverTeilnehmer}"]`
      );
      // Reset aller grünen Ränder in diesem Feld
      feld.querySelectorAll("[data-kategorie]").forEach(b => {
        b.classList.remove("ring-green-400");
      });
      // Neue Auswahl markieren
      button.classList.add("ring-green-400");
      window.gewaehlteKategorie = button.dataset.kategorie;
      // Spielen-Button aktivieren
      spielenButton.disabled = false;
      spielenButton.classList.remove("opacity-50", "cursor-not-allowed");
    });
  });

  // 🎲 Würfeln-Button-Listener (hook in deine Würfellogik)
  attachWurfListener("#btn-wuerfeln");
  attachWurfListener("#spiel-controls button");

  // SPIELEN-Button: Spielzug speichern und dynamisch updaten
  spielenButton.addEventListener("click", () => {
    if (!window.gewaehlteKategorie || !window.currentWuerfel.length) return;

    const payload = {
      kategorie: window.gewaehlteKategorie,
      punkte: parseInt(
        document
          .querySelector(`.player-field[data-teilnehmer-id="${window.aktiverTeilnehmer}"]`)
          .querySelector(`[data-kategorie="${window.gewaehlteKategorie}"]`)
          .textContent,
        10
      ),
      wuerfel: window.currentWuerfel
    };

    fetch("/ajax/zug-speichern", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(r => r.json())
      .then(res => {
        if (res.status === "ok") {
          aktualisiereSpielbrett(res);
        } else if (res.status === "fertig") {
          window.location.href = res.redirect;
        } else {
          alert("Fehler: " + res.msg);
        }
      })
      .catch(console.error);
  });
});

/**
 * Komplettes Redraw des Spielbretts nach Serverantwort
 */
function aktualisiereSpielbrett(res) {
  const nextId = res.next_player;    // spielteilnehmer.id des neuen Aktiven
  const spieler = res.spieler;       // Array mit {teilnehmer_id, ist_aktiv, punkte}

  // 1) Kopf‑Badges updaten
  document.querySelectorAll(".player-badge").forEach(badge => {
    const tid = Number(badge.dataset.teilnehmerId);
    const info = spieler.find(s => s.teilnehmer_id === tid);
    badge.querySelector(".punkte").textContent = info.punkte;
    badge.classList.toggle("bg-red-500",   tid === nextId);
    badge.classList.toggle("text-white",    tid === nextId);
    badge.classList.toggle("bg-gray-200",   tid !== nextId);
    badge.classList.toggle("text-gray-600", tid !== nextId);
  });

  // 2) Spielfelder aktiv/inaktiv setzen
  document.querySelectorAll(".player-field").forEach(field => {
    const tid = Number(field.dataset.teilnehmerId);
    field.classList.toggle("opacity-50", tid !== nextId);
  });

  // 3) Kategorie‑Buttons zurücksetzen & nur neues Feld aktivieren
  document.querySelectorAll(".player-field button[data-kategorie]").forEach(btn => {
    btn.disabled = true;
    btn.textContent = "0";
    btn.classList.remove("ring","ring-yellow-400","ring-red-500","cursor-pointer","hover:ring-2");
  });
  const neuesFeld = document.querySelector(`.player-field[data-teilnehmer-id="${nextId}"]`);
  neuesFeld.querySelectorAll("button[data-kategorie]").forEach(btn => {
    btn.disabled = false;
  });

  // 4) Würfel‑UI zurücksetzen
  window.currentWuerfel = [];
  window.gewaehlteKategorie = null;
  window.aktiverTeilnehmer = nextId;

  document.querySelectorAll(".dice-row img").forEach(img => {
    img.classList.remove("ring-4","ring-yellow-400");
    // img.dataset.baseSrc muss im Template gesetzt sein
    img.src = img.dataset.baseSrc;
  });
  document.getElementById("spiel-controls").classList.add("hidden");
  document.getElementById("btn-wuerfeln").classList.remove("hidden");
}

/**
 * Hilfsfunktion für Deine bereits bestehende Würfellogik
 */
function attachWurfListener(selector) {
  const btn = document.querySelector(selector);
  if (!btn) return;
  btn.addEventListener("click", () => {
    setTimeout(() => {
      window.sendeWurfZurBerechnung(window.currentWuerfel);
    }, 50);
  });
}