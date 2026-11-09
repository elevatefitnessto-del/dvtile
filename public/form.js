// Site visit request: validates in place, posts JSON to the Vercel function.
(() => {
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Floating booking button: visible once the hero is gone, hidden while the form is on screen.
  const dock = document.querySelector(".dock");
  const heroEl = document.getElementById("hero");
  const contact = document.getElementById("contact");
  if (dock && heroEl && contact && "IntersectionObserver" in window) {
    dock.hidden = false;
    let pastHero = false, atForm = false;
    const sync = () => dock.classList.toggle("is-on", pastHero && !atForm);
    new IntersectionObserver(([e]) => { pastHero = !e.isIntersecting; sync(); }, { threshold: 0.15 }).observe(heroEl);
    new IntersectionObserver(([e]) => { atForm = e.isIntersecting; sync(); }, { threshold: 0.05 }).observe(contact);
  }

  const form = document.getElementById("appointment");
  if (!form) return;
  const status = form.querySelector(".form-status");
  const btn = form.querySelector("button[type=submit]");
  const label = btn.textContent;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.className = "form-status";
    let firstBad = null;
    for (const el of form.querySelectorAll("[required]")) {
      const ok = el.value.trim() && el.checkValidity();
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !firstBad) firstBad = el;
    }
    if (firstBad) {
      status.classList.add("error");
      status.textContent = firstBad.type === "email" && firstBad.value
        ? "Enter an email address like name@example.com."
        : "Add your name and email so we can arrange the visit.";
      firstBad.focus();
      return;
    }
    btn.disabled = true;
    btn.textContent = "Sending…";
    try {
      const res = await fetch("/api/appointment", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      status.classList.add("ok");
      status.textContent = "Request sent. We’ll reply within one business day to arrange your site visit.";
    } catch {
      status.classList.add("error");
      status.textContent = "The request didn’t send. Check your connection and try again.";
    } finally {
      btn.disabled = false;
      btn.textContent = label;
    }
  });
})();
