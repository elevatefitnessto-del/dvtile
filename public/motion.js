// Scroll motion for the sections below the walkthrough (GSAP + ScrollTrigger).
// Every element is visible by default: if GSAP fails to load, or the visitor prefers
// reduced motion, nothing is hidden and nothing moves.
(() => {
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  const ease = "power3.out";
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    // Section headings rise in once, in page order.
    gsap.utils.toArray(".sheet .section-head").forEach((head) => {
      gsap.from(head.children, {
        y: 28, autoAlpha: 0, duration: 0.9, ease, stagger: 0.08,
        scrollTrigger: { trigger: head, start: "top 85%", once: true },
      });
    });

    // Recent work: each photo opens from a slight crop.
    ScrollTrigger.batch(".work > .work__grid .work__item, .work__ideas .work__item", {
      start: "top 88%",
      once: true,
      onEnter: (items) => {
        gsap.fromTo(items,
          { clipPath: "inset(10% 10% 10% 10% round 8px)", scale: 1.04 },
          { clipPath: "inset(0% 0% 0% 0% round 8px)", scale: 1, duration: 1.1, ease: "expo.out", stagger: 0.08, clearProps: "clipPath,transform" });
      },
    });

    // Neighbourhoods settle in as one line of type.
    gsap.from(".area-list li", {
      y: 14, autoAlpha: 0, duration: 0.6, ease, stagger: 0.025,
      scrollTrigger: { trigger: ".area-list", start: "top 85%", once: true },
    });

    // Partner logos.
    gsap.from(".partners__logos li", {
      y: 12, autoAlpha: 0, duration: 0.7, ease, stagger: 0.1,
      scrollTrigger: { trigger: ".partners", start: "top 90%", once: true },
    });

    // Footer wordmark tightens as it arrives.
    gsap.fromTo(".footer__mark", { letterSpacing: "0.34em" }, {
      letterSpacing: "0.18em", ease: "none",
      scrollTrigger: { trigger: ".footer", start: "top bottom", end: "top 55%", scrub: 0.6 },
    });
  });

  // Signature moment, desktop only: a bronze line draws across the five process
  // steps as you scroll, lighting each step as the line reaches it.
  mm.add("(prefers-reduced-motion: no-preference) and (min-width: 1181px)", () => {
    const steps = document.querySelector(".process .steps");
    if (!steps) return;
    const line = document.createElement("span");
    line.className = "steps__line";
    line.setAttribute("aria-hidden", "true");
    steps.prepend(line);
    const items = gsap.utils.toArray(".process .steps li");
    gsap.set(items, { "--lit": 0.28 });
    const tl = gsap.timeline({
      scrollTrigger: { trigger: steps, start: "top 75%", end: "bottom 55%", scrub: 0.8 },
    });
    tl.fromTo(line, { scaleX: 0 }, { scaleX: 1, ease: "none", duration: items.length });
    items.forEach((li, i) => tl.to(li, { "--lit": 1, duration: 0.35, ease: "none" }, i + 0.1));
    return () => line.remove();
  });

  // Positions depend on fonts and late-loading images.
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
  window.addEventListener("load", () => ScrollTrigger.refresh());
})();
