<script>
document.addEventListener("DOMContentLoaded", function () {
  const diceCount = 5;
  const diceDark = document.querySelectorAll("img[src*='-white.svg']");
  const diceLight = document.querySelectorAll("img:not([src*='-white.svg'])");
  const wuerfelnBtn = document.getElementById("btn-wuerfeln");

  function rollDice() {
    for (let i = 0; i < diceCount; i++) {
      const randomValue = Math.floor(Math.random() * 6) + 1;

      // 💡 Pfade dynamisch setzen
      diceDark[i].src = `/static/img/dice/dice${randomValue}-white.svg`;
      diceLight[i].src = `/static/img/dice/dice${randomValue}.svg`;
    }

    // TODO: Steuerung anzeigen (Dioden + neue Buttons)
    document.getElementById("spiel-controls").classList.remove("hidden");
    wuerfelnBtn.classList.add("hidden");
  }

  if (wuerfelnBtn) {
    wuerfelnBtn.addEventListener("click", rollDice);
  }
});
</script>