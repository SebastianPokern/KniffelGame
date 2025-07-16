document.addEventListener("DOMContentLoaded", () => {
  const diceImages = document.querySelectorAll(".dice-row img");
  const rollButton = document.getElementById("btn-wuerfeln");
  const controlSection = document.getElementById("spiel-controls");
  const diodes = controlSection?.querySelectorAll("div > div");
  const secondRollBtn = controlSection?.querySelectorAll("button")[0];
  const playBtn = controlSection?.querySelectorAll("button")[1];

  let currentRoll = 0;
  const maxRolls = 3;
  const diceValues = [0, 0, 0, 0, 0];
  const lockedDice = [false, false, false, false, false];

  // Würfel klickbar machen: Sperren/Entsperren nach dem ersten Wurf
  diceImages.forEach((img, index) => {
    img.addEventListener("click", () => {
      if (currentRoll === 0) return;
      lockedDice[index] = !lockedDice[index];
      img.classList.toggle("ring-4");
      img.classList.toggle("ring-yellow-400");
    });
  });

  // Start-Wurf
  rollButton?.addEventListener("click", () => {
    currentRoll = 1;
    rollDice();
    rollButton.classList.add("hidden");
    controlSection.classList.remove("hidden");
    updateDiodes();
  });

  // Weitere Würfe (max. 3)
  secondRollBtn?.addEventListener("click", () => {
    if (currentRoll >= maxRolls) return;
    currentRoll++;
    rollDice();
    updateDiodes();
    if (currentRoll >= maxRolls) {
      secondRollBtn.classList.add("opacity-50", "cursor-not-allowed");
      secondRollBtn.disabled = true;
    }
  });

  function rollDice() {
    diceImages.forEach((img, i) => {
      if (!lockedDice[i]) {
        const value = Math.floor(Math.random() * 6) + 1;
        diceValues[i] = value;
        img.src = `/static/img/dice/dice${value}.svg`;
        img.alt = `Würfel ${value}`;
      }
    });

    // 🧠 Ergebnis global merken
    window.currentWuerfel = [...diceValues];

    // 🔁 Punkte berechnen lassen
    if (typeof window.sendeWurfZurBerechnung === "function") {
      window.sendeWurfZurBerechnung(diceValues);
    }
  }

  function updateDiodes() {
    if (!diodes) return;
    diodes.forEach((dot, index) => {
      if (index < currentRoll) {
        dot.classList.remove("bg-green-500");
        dot.classList.add("bg-gray-500");
      } else {
        dot.classList.remove("bg-gray-500");
        dot.classList.add("bg-green-500");
      }
    });
  }
});