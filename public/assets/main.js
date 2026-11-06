import { MATERIALS, paint, paintZelligeWall } from './textures.js';

document.documentElement.classList.add('js');
document.getElementById('year').textContent = new Date().getFullYear();

const NOTES = {
  calacatta: ['Marble, Carrara, Italy', 'A warm white ground with bold grey and gold veining. Book-matched, it turns a wall into the room’s centrepiece.'],
  verde: ['Serpentine, Aosta Valley, Italy', 'Deep forest green crossed with fine white veins. Rich on vanities, fireplace surrounds and powder rooms.'],
  nero: ['Limestone, Basque Country, Spain', 'Near-black with sharp white veining. Polished for drama, honed for a softer, matte depth.'],
  travertine: ['Natural stone, Italy and Turkey', 'Layered, porous and warm. Honed and filled for floors; left open for texture on walls.'],
  zellige: ['Handmade glazed tile, Fez, Morocco', 'Cut and glazed by hand, so no two pieces sit quite level. The surface catches light like water.'],
  terrazzo: ['Composite, poured or tiled', 'Marble and stone chips set in a pale ground. Durable enough for entries, playful enough for baths.'],
};

// Swatch grid
const list = document.querySelector('.swatches');
for (const m of MATERIALS) {
  const li = document.createElement('li');
  const c = document.createElement('canvas');
  c.width = c.height = 640;
  c.setAttribute('role', 'img');
  c.setAttribute('aria-label', `${m.name} surface`);
  m.id === 'zellige' ? paintZelligeWall(c, 5) : paint(c, m.id, 3);
  const [origin, note] = NOTES[m.id];
  li.append(c);
  li.insertAdjacentHTML('beforeend', `<div class="swatch-text"><h3>${m.name}</h3><p class="origin">${origin}</p><p>${note}</p></div>`);
  list.append(li);
}

// Material picker
const options = document.querySelector('.picker-options');
const buttons = MATERIALS.map(m => {
  const b = document.createElement('button');
  b.type = 'button';
  b.dataset.id = m.id;
  b.setAttribute('aria-pressed', m.id === 'calacatta');
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  paint(c, m.id, 2);
  b.append(c, m.name);
  options.append(b);
  return b;
});
const mark = id => buttons.forEach(b => b.setAttribute('aria-pressed', b.dataset.id === id));

import('./hero.js').then(({ initHero }) => {
  const hero = initHero(document.querySelector('.hero-canvas'), { onMaterial: mark });
  if (!hero) { document.querySelector('.picker').hidden = true; return; }
  options.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (b) hero.setMaterial(b.dataset.id);
  });
}).catch(() => {
  document.querySelector('.hero').classList.add('no-webgl');
  document.querySelector('.picker').hidden = true;
});

// Nav background once the hero is scrolled past
const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('scrolled', scrollY > 40);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Appointment form
const form = document.getElementById('appointment');
const status = form.querySelector('.form-status');
form.addEventListener('submit', async e => {
  e.preventDefault();
  status.className = 'form-status';
  let firstBad = null;
  for (const el of form.querySelectorAll('[required]')) {
    const ok = el.value.trim() && el.checkValidity();
    el.setAttribute('aria-invalid', ok ? 'false' : 'true');
    if (!ok && !firstBad) firstBad = el;
  }
  if (firstBad) {
    status.classList.add('error');
    status.textContent = firstBad.type === 'email' && firstBad.value
      ? 'Enter an email address like name@example.com.'
      : 'Add your name and email so we can confirm a time.';
    firstBad.focus();
    return;
  }
  const btn = form.querySelector('button[type=submit]');
  btn.disabled = true;
  btn.textContent = 'Sending…';
  try {
    const res = await fetch('/api/appointment', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    if (!res.ok) throw new Error();
    form.reset();
    status.textContent = 'Request sent. We’ll confirm your appointment by email.';
  } catch {
    status.classList.add('error');
    status.textContent = 'The request didn’t go through. Try again, or email hello@dvtile.ca.';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Request appointment';
  }
});
