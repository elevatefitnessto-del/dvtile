# dvtile.ca

Static site for DVTile, a private by-appointment tile and stone showroom at 44 Jackes Avenue, Toronto.
No build step: `public/` is served as-is, with one Cloudflare Pages Function for the appointment form.

- `public/index.html` page
- `public/assets/hero.js` Three.js slab field (intro drop, cursor lift, material flip)
- `public/assets/textures.js` procedural stone and tile textures (used by the hero and the collection grid)
- `functions/api/appointment.js` emails form submissions via Cloudflare Email Routing

## Run locally

    npx wrangler pages dev

## Deploy to Cloudflare Pages

1. In Cloudflare, enable **Email Routing** on dvtile.ca and verify the showroom inbox as a destination.
2. Put that address in both places in `wrangler.toml`.
3. `npx wrangler login`, then `npx wrangler pages deploy` (first run creates the `dvtile` project).
4. In the Pages project, add the custom domains `dvtile.ca` and `www.dvtile.ca`.

## Before launch

- Confirm the material list and descriptions match what the showroom actually carries.
- Confirm `hello@dvtile.ca` exists (used in the form's error message), or change it in `public/assets/main.js`.
- Add a phone number to the Visit section and footer if you want calls.
