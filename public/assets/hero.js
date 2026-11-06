import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { MATERIALS, makeCanvas } from './textures.js';

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

export function initHero(canvas, { onMaterial } = {}) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch {
    canvas.closest('.hero').classList.add('no-webgl');
    return null;
  }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);

  // Soft studio light: a cool key from the window side, warm fill, and a sky/ground ambient.
  scene.add(new THREE.HemisphereLight(0xf4f6f4, 0x8c8577, 1.1));
  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  key.position.set(-6, 12, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = -14; key.shadow.camera.right = 14;
  key.shadow.camera.top = 10; key.shadow.camera.bottom = -10;
  key.shadow.radius = 6;
  key.shadow.bias = -0.0004;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xffe9cf, 0.7);
  rim.position.set(8, 4, -6);
  scene.add(rim);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.16 }));
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.06;
  ground.receiveShadow = true;
  scene.add(ground);

  // Six variants per material so neighbouring slabs differ, as real stone does.
  const VARIANTS = 6;
  const finish = { calacatta: [0.18, 0.6], verde: [0.12, 0.8], nero: [0.1, 0.9], travertine: [0.62, 0], zellige: [0.08, 1], terrazzo: [0.35, 0.3] };
  const mats = {};
  for (const { id } of MATERIALS) {
    mats[id] = Array.from({ length: VARIANTS }, (_, v) => {
      const tex = new THREE.CanvasTexture(makeCanvas(id, v + 1, 512));
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      const [roughness, clearcoat] = finish[id];
      return new THREE.MeshPhysicalMaterial({ map: tex, roughness, clearcoat, clearcoatRoughness: 0.15 });
    });
  }

  const SIZE = 1.5, GAP = 0.06;
  const geo = new RoundedBoxGeometry(SIZE, 0.11, SIZE, 3, 0.03);
  const group = new THREE.Group();
  scene.add(group);
  const tiles = [];
  let cols = 0, rows = 0;

  function build() {
    const narrow = innerWidth < 760;
    const c = narrow ? 7 : 12, r = narrow ? 9 : 8;
    if (c === cols && r === rows) return;
    cols = c; rows = r;
    tiles.forEach(t => group.remove(t.mesh));
    tiles.length = 0;
    const step = SIZE + GAP;
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
      const v = (i * 7 + j * 13) % VARIANTS;
      const mesh = new THREE.Mesh(geo, mats[current][v]);
      mesh.castShadow = mesh.receiveShadow = true;
      const x = (i - (cols - 1) / 2) * step, z = (j - (rows - 1) / 2) * step;
      mesh.position.set(x, reduce ? 0 : 7 + Math.random() * 2, z);
      group.add(mesh);
      // Intro: slabs settle along a diagonal, top-left first.
      tiles.push({ mesh, x, z, v, lift: 0, delay: reduce ? 0 : (i + j) * 0.055 + Math.random() * 0.05, flipFrom: 0, flipTo: 0, flipStart: -1, next: null });
    }
    started = performance.now();
  }

  let current = 'calacatta';
  let started = performance.now();

  function setMaterial(id) {
    if (id === current) return;
    current = id;
    onMaterial?.(id);
    const now = performance.now();
    for (const t of tiles) {
      if (reduce) { t.mesh.material = mats[id][t.v]; continue; }
      // Flip as a wave travelling out from the far-left corner.
      t.flipFrom = t.mesh.rotation.x;
      t.flipTo = Math.round(t.flipFrom / Math.PI) * Math.PI + Math.PI;
      t.flipStart = now + (t.x + t.z + 20) * 28;
      t.next = id;
    }
  }

  function layout() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const narrow = w < 760;
    camera.position.set(narrow ? 0 : -3, narrow ? 20 : 15, narrow ? 15 : 13);
    camera.lookAt(narrow ? 0 : 2.5, 0, narrow ? 1.5 : 0.5);
    camera.updateProjectionMatrix();
    build();
  }

  const pointer = new THREE.Vector2(9, 9), hit = new THREE.Vector3(999, 0, 999), target = new THREE.Vector3(999, 0, 999);
  const ray = new THREE.Raycaster(), plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  canvas.closest('.hero').addEventListener('pointermove', e => {
    const r = canvas.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(pointer, camera);
    ray.ray.intersectPlane(plane, target);
  });
  canvas.closest('.hero').addEventListener('pointerleave', () => target.set(999, 0, 999));

  const easeOutBack = x => 1 + 2.2 * Math.pow(x - 1, 3) + 1.2 * Math.pow(x - 1, 2);
  const easeInOut = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

  let visible = true, raf = 0;
  function frame(now) {
    raf = 0;
    if (!visible) return;
    hit.lerp(target, 0.12);
    const t0 = (now - started) / 1000;
    for (const t of tiles) {
      const m = t.mesh;
      // Intro drop.
      const p = Math.min(Math.max((t0 - t.delay) / 0.9, 0), 1);
      const dropY = reduce ? 0 : (1 - easeOutBack(p)) * 8;
      // Cursor lift: slabs nearest the pointer rise and tip toward it.
      const dx = t.x - hit.x, dz = t.z - hit.z, d2 = dx * dx + dz * dz;
      const want = reduce ? 0 : Math.exp(-d2 / 5) * 0.9;
      t.lift += (want - t.lift) * 0.1;
      m.position.y = dropY + t.lift;
      m.rotation.z = -dx * t.lift * 0.08;
      // Flip.
      if (t.flipStart > 0 && now >= t.flipStart) {
        const fp = Math.min((now - t.flipStart) / 700, 1);
        m.rotation.x = t.flipFrom + (t.flipTo - t.flipFrom) * easeInOut(fp);
        m.position.y += Math.sin(fp * Math.PI) * 0.9;
        if (fp >= 0.5 && t.next) { m.material = mats[t.next][t.v]; t.next = null; }
        if (fp >= 1) t.flipStart = -1;
      } else if (t.flipStart < 0) {
        m.rotation.x = t.flipTo - t.lift * dz * 0.08;
      }
    }
    renderer.render(scene, camera);
    raf = requestAnimationFrame(frame);
  }

  new IntersectionObserver(([e]) => {
    visible = e.isIntersecting;
    if (visible && !raf) raf = requestAnimationFrame(frame);
  }).observe(canvas);
  new ResizeObserver(layout).observe(canvas);
  layout();
  raf = requestAnimationFrame(frame);

  return { setMaterial };
}
