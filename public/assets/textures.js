// Procedural material textures, drawn to canvas. Shared by the 3D hero and the swatch grid.

function rng(seed) {
  let s = seed >>> 0 || 1;
  return () => ((s = Math.imul(s ^ (s >>> 15), 2246822507) ^ Math.imul(s ^ (s >>> 13), 3266489909)), (s >>> 0) / 4294967296);
}

function grain(ctx, size, amount, r) {
  const img = ctx.getImageData(0, 0, size, size);
  const d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    const n = (r() - 0.5) * amount;
    d[i] += n; d[i + 1] += n; d[i + 2] += n;
  }
  ctx.putImageData(img, 0, 0);
}

function veins(ctx, size, r, { color, count, width, blur, alpha }) {
  ctx.save();
  ctx.filter = `blur(${blur}px)`;
  ctx.strokeStyle = color;
  ctx.lineCap = 'round';
  for (let v = 0; v < count; v++) {
    ctx.globalAlpha = alpha * (0.5 + r() * 0.5);
    ctx.lineWidth = width * (0.3 + r());
    let x = r() * size * 1.4 - size * 0.2;
    let y = -size * 0.1;
    const drift = (r() - 0.3) * 1.6;
    ctx.beginPath();
    ctx.moveTo(x, y);
    while (y < size * 1.1) {
      const step = size * (0.05 + r() * 0.08);
      const nx = x + drift * step + (r() - 0.5) * step * 1.6;
      const ny = y + step;
      ctx.quadraticCurveTo(x + (r() - 0.5) * step, y + step / 2, nx, ny);
      x = nx; y = ny;
      if (r() < 0.12) { // branching hairline
        ctx.stroke(); ctx.save(); ctx.lineWidth *= 0.35;
        ctx.beginPath(); ctx.moveTo(x, y);
        ctx.quadraticCurveTo(x + step, y + step * 0.3, x + step * 2 * (r() - 0.2), y + step * 1.5);
        ctx.stroke(); ctx.restore(); ctx.beginPath(); ctx.moveTo(x, y);
      }
    }
    ctx.stroke();
  }
  ctx.restore();
}

const painters = {
  calacatta(ctx, s, r) {
    const g = ctx.createLinearGradient(0, 0, s, s);
    g.addColorStop(0, '#f6f5f1'); g.addColorStop(1, '#ecebe6');
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
    veins(ctx, s, r, { color: '#a19d96', count: 4, width: s * 0.007, blur: s * 0.006, alpha: 0.4 });
    veins(ctx, s, r, { color: '#8a7a62', count: 2, width: s * 0.008, blur: s * 0.002, alpha: 0.5 });
    veins(ctx, s, r, { color: '#b5b1a9', count: 7, width: s * 0.003, blur: 0.5, alpha: 0.7 });
    grain(ctx, s, 6, r);
  },
  verde(ctx, s, r) {
    ctx.fillStyle = '#1d3832'; ctx.fillRect(0, 0, s, s);
    for (let i = 0; i < 40; i++) { // cloudy serpentine patches
      ctx.fillStyle = `rgba(${40 + r() * 40},${80 + r() * 50},${66 + r() * 30},${0.15 + r() * 0.25})`;
      ctx.save(); ctx.filter = `blur(${s * 0.03}px)`;
      ctx.beginPath(); ctx.ellipse(r() * s, r() * s, s * (0.04 + r() * 0.12), s * (0.02 + r() * 0.06), r() * 3, 0, 7); ctx.fill();
      ctx.restore();
    }
    veins(ctx, s, r, { color: '#e3ece6', count: 4, width: s * 0.003, blur: 0.4, alpha: 0.8 });
    veins(ctx, s, r, { color: '#9fb9ad', count: 4, width: s * 0.012, blur: s * 0.006, alpha: 0.35 });
    grain(ctx, s, 8, r);
  },
  nero(ctx, s, r) {
    ctx.fillStyle = '#1b1c1d'; ctx.fillRect(0, 0, s, s);
    veins(ctx, s, r, { color: '#f1f0ec', count: 4, width: s * 0.004, blur: 0.4, alpha: 0.9 });
    veins(ctx, s, r, { color: '#8d8f90', count: 6, width: s * 0.01, blur: s * 0.008, alpha: 0.25 });
    grain(ctx, s, 7, r);
  },
  travertine(ctx, s, r) {
    ctx.fillStyle = '#cfc6b6'; ctx.fillRect(0, 0, s, s);
    for (let y = 0; y < s; y += 1 + r() * 4) { // horizontal bedding bands
      ctx.fillStyle = `rgba(${150 + r() * 70},${135 + r() * 60},${110 + r() * 50},${0.08 + r() * 0.18})`;
      ctx.fillRect(0, y + Math.sin(y * 0.05) * 3, s, 1 + r() * 3);
    }
    for (let i = 0; i < 60; i++) { // honed pores
      ctx.fillStyle = `rgba(120,104,82,${0.15 + r() * 0.3})`;
      ctx.beginPath(); ctx.ellipse(r() * s, r() * s, s * (0.004 + r() * 0.02), s * (0.002 + r() * 0.004), 0, 0, 7); ctx.fill();
    }
    grain(ctx, s, 10, r);
  },
  zellige(ctx, s, r) {
    const hue = 158 + r() * 12;
    const light = 24 + r() * 10;
    const g = ctx.createRadialGradient(s * (0.3 + r() * 0.4), s * (0.3 + r() * 0.4), s * 0.05, s / 2, s / 2, s * 0.75);
    g.addColorStop(0, `hsl(${hue} 42% ${light + 14}%)`);
    g.addColorStop(0.7, `hsl(${hue} 48% ${light}%)`);
    g.addColorStop(1, `hsl(${hue} 50% ${light - 8}%)`);
    ctx.fillStyle = g; ctx.fillRect(0, 0, s, s);
    for (let i = 0; i < 25; i++) { // glaze pooling
      ctx.save(); ctx.filter = `blur(${s * 0.02}px)`;
      ctx.fillStyle = `hsla(${hue} 50% ${light - 10 + r() * 25}% / ${0.2 + r() * 0.3})`;
      ctx.beginPath(); ctx.arc(r() * s, r() * s, s * (0.02 + r() * 0.08), 0, 7); ctx.fill();
      ctx.restore();
    }
    grain(ctx, s, 12, r);
  },
  terrazzo(ctx, s, r) {
    ctx.fillStyle = '#e6e3dc'; ctx.fillRect(0, 0, s, s);
    const chips = ['#22403a', '#8c6b44', '#2a2d2e', '#b8b2a6', '#f7f6f2', '#6f7c76'];
    for (let i = 0; i < 160; i++) {
      ctx.fillStyle = chips[Math.floor(r() * chips.length)];
      const cx = r() * s, cy = r() * s, rad = s * (0.006 + r() * r() * 0.05);
      ctx.beginPath();
      const n = 5 + Math.floor(r() * 4);
      for (let k = 0; k < n; k++) {
        const a = (k / n) * Math.PI * 2, rr = rad * (0.6 + r() * 0.6);
        k ? ctx.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr) : ctx.moveTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
      }
      ctx.fill();
    }
    grain(ctx, s, 8, r);
  },
};

export const MATERIALS = [
  { id: 'calacatta', name: 'Calacatta' },
  { id: 'verde', name: 'Verde Alpi' },
  { id: 'nero', name: 'Nero Marquina' },
  { id: 'travertine', name: 'Travertine' },
  { id: 'zellige', name: 'Zellige' },
  { id: 'terrazzo', name: 'Terrazzo' },
];

export function paint(canvas, id, seed = 1) {
  const s = canvas.width;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  painters[id](ctx, s, rng(seed * 7919 + id.length * 104729));
  return canvas;
}

// A wall of small handmade pieces; used where zellige is shown large.
export function paintZelligeWall(canvas, n = 4) {
  const s = canvas.width, ctx = canvas.getContext('2d');
  const g = Math.max(2, s / 160), step = (s - g) / n;
  ctx.fillStyle = '#cfc9bd'; ctx.fillRect(0, 0, s, s);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const piece = makeCanvas('zellige', i * n + j + 11, 128);
    ctx.drawImage(piece, g + i * step, g + j * step, step - g, step - g);
  }
  return canvas;
}

export function makeCanvas(id, seed, size = 512) {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  return paint(c, id, seed);
}
