# dvtile.ca

Static site for DV Tile (Don Valley Tile), a marble, natural stone and tile flooring contractor serving Toronto and the GTA. No build step: `public/` is served as-is by Vercel, with one serverless function for the site visit form.

## Files

- `public/index.html` the page: hero, detail walkthrough, services, Olympia product catalogue, process, areas, FAQ, contact form.
- `public/styles.css` hero, navigation and glass styles. Brand colours and fonts are the variables in the `:root` block at the top.
- `public/tour.css` walkthrough layout and captions. `public/site.css` the sections below the walkthrough.
- `public/hero.js` fits the DV TILE wordmark behind the house roof. If you replace `assets/hero-bg.webp` / `hero-fg.webp`, update `ASPECT`, `ROOF_Y`, `HOUSE_CX`, `CLIP_Y`, `SKY_L` and `SKY_R` at the top.
- `public/tour.js` draws the walkthrough frames on a canvas as you scroll. `public/pager.js` pages one stop per scroll through the hero and walkthrough, then hands back normal scrolling.
- `public/form.js` validates and posts the form to `/api/appointment`, and shows the floating booking button.
- `public/assets/tour/d/` 281 landscape frames (1600 × 900), `public/assets/tour/m/` the same frames cropped portrait (640 × 1080). Frame count lives in `data-frames` on `#tour`; raise `data-version` when frames change.
- `brand/` logo files: `mark.svg`, `mark-reverse.svg`, `logo.html` (source for the lockups) and rendered PNGs.
- `public/portfolio.html` + `public/portfolio.js`: 165 photos with room filters and click-to-enlarge (works without JavaScript as plain links). The Recent work filter is 48 photographs of DV Tile jobs in `public/assets/portfolio/job-01.webp` through `job-48.webp` (each with a `-640` thumbnail). Prep shots are captioned as prep. The other photos mix earlier installations and design concepts.
- Service pages (`public/marble-natural-stone-floors.html` and six more) and `public/cost-guide.html` share `public/page.css`. They are generated from `/tmp` script data; edit the HTML directly for copy changes.
- `api/appointment.js` emails form submissions through Resend.

## Run locally

    python3 -m http.server 8080 --directory public

The form needs the Vercel function, so it only sends on a deployment (`vercel dev` also works).

## Form email

Set these in the Vercel project: `RESEND_API_KEY`, `APPOINTMENTS_TO` (the inbox that receives requests), `APPOINTMENTS_FROM` (a verified sender such as `DV Tile <website@dvtile.ca>`). Without them the form shows an error and nothing is sent.

## Before launch

- Add a phone number to the contact section and footer if you take calls.
- Confirm the address at 44 Jackes Avenue is where you want clients to find you.
- The walkthrough rooms are a rendered concept home; the footer says so. The portfolio Recent work filter, and the recent-job rows on the homepage and on the shower, backsplash, marble floor and porcelain pages, are photographs of DV Tile jobs.
