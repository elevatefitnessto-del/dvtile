// Filter a photo or video library and enlarge a still. Without this script every
// item shows, and each still links to its full-size image. Videos stay in the page
// with their own controls and are not fetched until play (preload="none").
(() => {
  const setup = (root) => {
    const grid = root.querySelector(".pf-grid");
    const buttons = [...root.querySelectorAll(".pf-filter")];
    const count = root.querySelector(".pf-count");
    if (!grid || !count || !buttons.length) return;
    const items = [...grid.querySelectorAll(".pf-item")];
    const noun = count.dataset.noun || "photo";
    const show = (cat) => {
      let n = 0;
      for (const li of items) {
        const on = cat === "all" || (cat === "recent" ? li.dataset.real === "1" : li.dataset.cat === cat);
        li.hidden = !on;
        if (on) n++;
      }
      for (const b of buttons) b.setAttribute("aria-pressed", String(b.dataset.cat === cat));
      const word = n === 1 ? noun : noun + "s";
      count.textContent = `Showing ${n} ${word}`;
    };
    for (const b of buttons) b.addEventListener("click", () => {
      show(b.dataset.cat);
      const hash = b.dataset.cat === "all" ? "" : "#" + b.dataset.cat;
      if (location.hash !== hash) history.replaceState(null, "", hash || location.pathname + location.search);
    });
    const wanted = location.hash.replace("#", "");
    show(buttons.some((b) => b.dataset.cat === wanted) ? wanted : "all");
    window.addEventListener("hashchange", () => {
      const next = location.hash.replace("#", "");
      if (buttons.some((b) => b.dataset.cat === next)) show(next);
      else if (!next) show("all");
    });

    const dialog = document.querySelector(".pf-dialog");
    if (!dialog || typeof dialog.showModal !== "function" || grid.dataset.dialogBound) return;
    grid.dataset.dialogBound = "1";
    const big = dialog.querySelector("img");
    const cap = dialog.querySelector(".pf-dialog__cap");
    let opener = null;
    grid.addEventListener("click", (e) => {
      const a = e.target.closest(".pf-link");
      if (!a || !grid.contains(a)) return;
      e.preventDefault();
      opener = a;
      const img = a.querySelector("img");
      big.src = a.dataset.full;
      big.alt = img.alt;
      cap.textContent = img.alt;
      dialog.showModal();
    });
    if (!dialog.dataset.bound) {
      dialog.dataset.bound = "1";
      dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
      dialog.addEventListener("close", () => { big.removeAttribute("src"); opener?.focus(); });
    }
  };

  const libs = [...document.querySelectorAll(".pf-lib")];
  if (libs.length) libs.forEach(setup);
  else setup(document);
})();
