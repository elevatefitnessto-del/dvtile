// Portfolio: filter by room and enlarge a photo. Without this script every photo shows
// and each one links to its full-size image.
(() => {
  const grid = document.querySelector(".pf-grid");
  if (!grid) return;
  const items = [...grid.querySelectorAll(".pf-item")];
  const buttons = [...document.querySelectorAll(".pf-filter")];
  const count = document.querySelector(".pf-count");

    const show = (cat) => {
    let n = 0;
    for (const li of items) {
      const on = cat === "all" || (cat === "recent" ? li.dataset.real === "1" : li.dataset.cat === cat);
      li.hidden = !on;
      if (on) n++;
    }
    for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.cat === cat));
    count.textContent = `Showing ${n} ${n === 1 ? "photo" : "photos"}`;
  };
  for (const b of buttons) b.addEventListener("click", () => show(b.dataset.cat));
  const fromHash = location.hash === "#recent" ? "recent" : "all";
  show(fromHash);

  const dialog = document.querySelector(".pf-dialog");
  if (!dialog || typeof dialog.showModal !== "function") return;
  const big = dialog.querySelector("img");
  const cap = dialog.querySelector(".pf-dialog__cap");
  let opener = null;

  grid.addEventListener("click", (e) => {
    const a = e.target.closest(".pf-link");
    if (!a) return;
    e.preventDefault();
    opener = a;
    const img = a.querySelector("img");
    big.src = a.dataset.full;
    big.alt = img.alt;
    cap.textContent = img.alt;
    dialog.showModal();
  });
  // Clicking the dark backdrop closes it too.
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener("close", () => { big.removeAttribute("src"); opener?.focus(); });
})();
