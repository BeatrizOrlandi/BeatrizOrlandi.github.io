/* Interações locais. Sem analytics, chamadas de API ou armazenamento de dados. */
"use strict";

const controls = document.querySelector("[data-project-controls]");
if (controls) {
  const cards = [...document.querySelectorAll("[data-project]")];
  const buttons = [...document.querySelectorAll("[data-filter]")];
  const input = document.querySelector("[data-search-input]");
  const count = document.querySelector("[data-filter-count]");
  const empty = document.querySelector("[data-empty]");
  let selected = "todos";
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const applyFilters = () => {
    const query = normalize(input.value.trim());
    let shown = 0;
    for (const card of cards) {
      const matches = (selected === "todos" || card.dataset.group === selected) &&
        normalize(card.dataset.search).includes(query);
      card.hidden = !matches;
      if (matches) shown += 1;
    }
    count.textContent = `${shown} de ${cards.length} projetos`;
    empty.hidden = shown > 0;
    for (const button of buttons) {
      const active = button.dataset.filter === selected;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }
  };
  for (const button of buttons) {
    button.addEventListener("click", () => { selected = button.dataset.filter; applyFilters(); });
  }
  input.addEventListener("input", applyFilters);
  controls.hidden = false;
  count.hidden = false;
  applyFilters();
}

const printButton = document.querySelector("[data-print]");
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener("click", () => window.print());
}
