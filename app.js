import * as THREE from './vendor/three/three.module.js';
import { OrbitControls } from './vendor/three/OrbitControls.js';
import { STLLoader } from './vendor/three/STLLoader.js';
import { run } from './calc.js';

/* ---------------- 3D viewer ---------------- */
const box = document.getElementById('viewer');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.localClippingEnabled = true;
renderer.setClearColor(0xffffff);
box.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.add(new THREE.HemisphereLight(0xffffff, 0xb0aea6, 1.7));
const sun = new THREE.DirectionalLight(0xffffff, 2.0); sun.position.set(-300, 500, 400); scene.add(sun);
const camera = new THREE.PerspectiveCamera(32, 1, 1, 20000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
const root = new THREE.Group(); root.rotation.x = -Math.PI / 2; scene.add(root);
const loader = new STLLoader();
const cache = new Map();
const clip = new THREE.Plane(new THREE.Vector3(0, 0, -1), 1000);

function mat(color, opts = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: opts.rough ?? 0.55, metalness: opts.metal ?? 0.1,
    side: THREE.DoubleSide, clippingPlanes: opts.clip ? [clip] : [], transparent: opts.opacity !== undefined, opacity: opts.opacity ?? 1 });
}
async function part(file, color, opts = {}) {
  if (!cache.has(file)) cache.set(file, loader.loadAsync('models/' + file).then(g => { g.computeVertexNormals(); return g; }));
  const mesh = new THREE.Mesh(await cache.get(file), mat(color, opts));
  if (opts.pos) mesh.position.set(...opts.pos);
  return mesh;
}
function fit() {
  const b = new THREE.Box3().setFromObject(root), s = b.getSize(new THREE.Vector3()), c = b.getCenter(new THREE.Vector3());
  const d = Math.max(s.x, s.y, s.z) * 1.6 / Math.min(1, Math.max(camera.aspect, 0.45));
  camera.position.set(c.x - d * 0.45, c.y + d * 0.55, c.z + d * 0.9); camera.near = d / 100; camera.far = d * 20; camera.updateProjectionMatrix();
  controls.target.copy(c); controls.update();
}
function resize() { const w = box.clientWidth, h = box.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
new ResizeObserver(resize).observe(box);
(function loop() { controls.update(); renderer.render(scene, camera); requestAnimationFrame(loop); })();

const ctl = document.getElementById('scene-controls'), cap = document.getElementById('scene-caption');
function slider(label, min, max, val, unit, onInput) {
  const l = document.createElement('label');
  l.innerHTML = `${label} <b><span>${val}</span>${unit}</b><input type="range" min="${min}" max="${max}" value="${val}">`;
  const input = l.querySelector('input'), out = l.querySelector('span');
  input.addEventListener('input', () => { out.textContent = input.value; onInput(+input.value); });
  ctl.appendChild(l); onInput(val);
}
let token = 0;
async function show(name) {
  const my = ++token;
  document.querySelectorAll('[data-scene]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.scene === name)));
  box.querySelector('.loading').style.display = 'flex';
  ctl.innerHTML = ''; clip.constant = 1000;
  let parts = [];
  if (name === 'module') {
    const housing = await part('display_grateheat_housing_1to10.stl', 0xb87333, { metal: 0.45, rough: 0.35, clip: true });
    const lid = await part('display_sidewalk_grate_lid_1to10.stl', 0x2f2f2d, { metal: 0.5 });
    parts = [housing, lid];
    if (my !== token) return;
    root.clear(); parts.forEach(p => root.add(p)); lid.position.z = 55; fit();
    slider('Lift the sidewalk grate', 0, 80, 30, ' mm', v => { lid.position.z = 55 + v; });
    slider('Cut the module open', 0, 100, 0, '%', v => { clip.constant = v === 0 ? 1000 : 45 - v * 0.8; });
    cap.textContent = 'Copper-colored parts: wavy fins around 9 rows of glycol tubes. The right-hand bay holds one-way louvers, so air pulled back into the tunnel and any emergency airflow skip the coil. Real size about 1.6 × 0.9 × 0.55 m.';
  } else if (name === 'street') {
    const spec = [['ground', 0xcfc7b8, { opacity: 0.999 }], ['sidewalk', 0xe7e4dc], ['train', 0x9aa3ab, { metal: 0.3 }], ['rails', 0x5b5b58],
      ['grate', 0x3a3a38, { metal: 0.5 }], ['module', 0xeb6834], ['pipe', 0xeb6834], ['heatpump', 0x2a78d6], ['bore', 0x1baf7a], ['school', 0xb5654a]];
    parts = await Promise.all(spec.map(([n, c, o]) => part(`street_${n}.stl`, c, o || {})));
    if (my !== token) return;
    root.clear(); parts.forEach(p => root.add(p)); fit();
    slider('See-through ground', 0, 90, 0, '%', v => { parts[0].material.opacity = 1 - v / 100; parts[0].material.depthWrite = v < 10; });
    cap.textContent = 'Orange: the grate module and the pipe loop under the sidewalk. Blue: the heat pump in the school basement. Green: boreholes that store summer tunnel heat for winter.';
  } else {
    const inlet = await part('rig_inlet_section.stl', 0x9aa3ab, { clip: true, pos: [0, 0, 0] });
    const flat = await part('rig_insert_flat_fins.stl', 0x2a78d6, { clip: true });
    const wavy = await part('rig_insert_wavy_fins.stl', 0xeb6834, { clip: true });
    const outlet = await part('rig_outlet_section.stl', 0x9aa3ab, { clip: true });
    parts = [inlet, flat, wavy, outlet];
    if (my !== token) return;
    root.clear(); parts.forEach(p => root.add(p));
    const place = gap => { inlet.position.set(-220 - gap, 0, 50); flat.position.set(-75 - gap / 3, 0, 0); wavy.position.set(40 + gap / 3, 0, 0); outlet.position.set(160 + gap, 0, 0); };
    place(20); fit();
    slider('Spread the parts', 0, 80, 20, ' mm', place);
    slider('Cut the rig open', 0, 1, 1, '', v => { clip.constant = v ? 0 : 1000; });
    cap.textContent = 'Left to right: the inlet (fits a 60 mm fan or hair dryer), the flat-fin insert (control), the wavy-fin insert and the outlet. Copper tube runs through the holes carrying ice water. Every part prints without supports.';
  }
  box.querySelector('.loading').style.display = 'none';
}
document.querySelectorAll('[data-scene]').forEach(b => b.addEventListener('click', () => show(b.dataset.scene)));
show('module').catch(e => { box.querySelector('.loading').textContent = 'Could not load the 3D model: ' + e.message; });

/* ---------------- Map ---------------- */
const [schools, tunnels] = await Promise.all([fetch('data/schools.json').then(r => r.json()), fetch('data/tunnels.json').then(r => r.json())]);
const map = L.map('map', { scrollWheelZoom: false }).setView([40.745, -73.945], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
tunnels.forEach(s => L.polyline([[s[0], s[1]], [s[2], s[3]]], { color: '#8A8984', weight: 4, opacity: 0.8 }).addTo(map));
const layer = L.layerGroup().addTo(map);
const markers = new Map();
const fmt = n => n.toLocaleString('en-US');
function popup(s) {
  const more = s.k > 1 ? ` <span style="color:#6B7480">(+${s.k - 1} more in this building)</span>` : '';
  return `<b>${s.n || 'School building'}</b>${more}<br>Building ${s.c} · about ${s.d} m from the tunnel<br>` +
    `Disadvantaged community: ${s.dac ? 'yes' : 'no'} · Burned oil in 2024: ${s.oil ? 'yes' : 'no'}<br>` +
    (s.yb ? `Built ${s.yb}` : 'Year built: no data') + (s.heat ? ` · Fossil heating fuel ${fmt(s.heat)} MMBtu/yr` : '') +
    (s.p ? '<br><b style="color:#B8461B">One of the first 19</b>' : '');
}
function draw(filter) {
  layer.clearLayers(); markers.clear();
  const shown = schools.filter(s => filter === 'p' ? s.p : s.d <= +filter);
  shown.forEach(s => {
    const color = s.d > 150 ? '#B9B8B2' : s.dac ? '#EB6834' : '#2A78D6';
    const m = L.circleMarker([s.la, s.lo], { radius: s.p ? 8 : 6, color: s.p ? '#15202B' : '#FFFFFF', weight: s.p ? 3 : 1.5, fillColor: color, fillOpacity: 0.95 })
      .bindPopup(popup(s)).addTo(layer);
    markers.set(s.c, m);
  });
  const rows = [...shown].sort((a, b) => (b.p - a.p) || (a.d - b.d));
  document.getElementById('rows').innerHTML = rows.map(s =>
    `<tr data-code="${s.c}"><td>${s.p ? '<b style="color:#B8461B">&#9679;</b> ' : ''}${s.n || s.c}<br><span style="color:#6B7480">${s.c}</span></td><td>${s.d} m</td><td>${s.yb || '?'}</td></tr>`).join('');
}
document.getElementById('rows').addEventListener('click', e => {
  const tr = e.target.closest('tr[data-code]'); if (!tr) return;
  const m = markers.get(tr.dataset.code); map.flyTo(m.getLatLng(), 16, { duration: 0.8 }); setTimeout(() => m.openPopup(), 850);
  document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'center' });
});
document.querySelectorAll('input[name=f]').forEach(r => r.addEventListener('change', () => draw(r.value)));
draw('150');

/* ---------------- Calculator ---------------- */
const ids = ['speed', 'area', 'outShare', 'modules', 'elecPrice', 'fuel', 'bank'];
const el = Object.fromEntries(ids.map(i => [i, document.getElementById(i)]));
const presets = { low: { speed: 0.6, area: 3, outShare: 40 }, mid: { speed: 1.2, area: 5, outShare: 50 }, high: { speed: 2.0, area: 7, outShare: 55 } };
document.querySelectorAll('[data-preset]').forEach(b => b.addEventListener('click', () => {
  Object.entries(presets[b.dataset.preset]).forEach(([k, v]) => el[k].value = v); update();
}));
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function stat(n, l) { return `<div class="stat"><div class="n">${n}</div><div class="l">${l}</div></div>`; }
function update() {
  const inp = { speed: +el.speed.value, area: +el.area.value, outShare: +el.outShare.value / 100, modules: +el.modules.value,
    elecPrice: +el.elecPrice.value, fuel: el.fuel.value, bank: el.bank.checked };
  document.getElementById('v-speed').textContent = inp.speed.toFixed(1);
  document.getElementById('v-area').textContent = inp.area;
  document.getElementById('v-out').textContent = el.outShare.value;
  document.getElementById('v-mod').textContent = inp.modules;
  document.getElementById('v-price').textContent = inp.elecPrice.toFixed(2);
  const r = run(inp);
  const fuelName = inp.fuel === 'oil' ? 'oil' : 'gas';
  const save = r.savingPerModule * inp.modules;
  document.getElementById('stats').innerHTML =
    stat(`${Math.round(r.total)} MWh`, `heat a year from ${inp.modules} module${inp.modules > 1 ? 's' : ''} (${Math.round(r.perModule)} each)`) +
    stat(`${Math.round(r.share * 100)}%`, 'of a typical near-tunnel school&rsquo;s yearly heat, on paper') +
    stat(`${Math.round(r.co2)} t`, `CO2e avoided a year, replacing ${fuelName}`) +
    stat(`${save >= 0 ? '' : '&minus;'}$${fmt(Math.abs(Math.round(save / 100) * 100))}`, save >= 0 ? `saved a year on energy vs ${fuelName}` : `more a year than ${fuelName} to run`) +
    stat(`${r.scop.toFixed(2)}`, `heat pump efficiency (COP), vs ${r.scopAshp.toFixed(2)} for a standard air-source unit`);
  const maxH = Math.max(...r.monthly.map(m => m.heat)) || 1;
  const bw = 200 / 12;
  document.getElementById('months').innerHTML = `<p style="font-size:14px;color:#3E4A56;margin-bottom:6px">Heat made each month. It dips in the coldest months because the coil is kept above freezing.${inp.bank ? ' Summer months charge the boreholes instead.' : ''}</p>` +
    `<svg viewBox="0 0 200 46" width="100%" style="max-width:760px;display:block" role="img" aria-label="Heat delivered by month">` +
    r.monthly.map((m, i) => { const h = m.heat / maxH * 34; return `<rect x="${i * bw + 2}" y="${38 - h}" width="${bw - 4}" height="${h}" rx="1" fill="#EB6834"><title>${MON[i]}: ${Math.round(m.heat * inp.modules)} MWh</title></rect><text x="${i * bw + bw / 2}" y="44.5" font-size="4" text-anchor="middle" fill="#6B7480">${MON[i]}</text>`; }).join('') + `</svg>`;
}
ids.forEach(i => el[i].addEventListener('input', update)); el.fuel.addEventListener('change', update);
update();
