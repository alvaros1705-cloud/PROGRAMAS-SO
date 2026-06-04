/* ══════════════════════════════════════════════
   DeadlockOS — shared.js
══════════════════════════════════════════════ */

// ── Marcar enlace activo en navbar ────────────
function setActiveNav() {
  const path = window.location.pathname.replace('/', '') || 'desktop';
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href').replace('/', '') || 'desktop';
    a.classList.toggle('active', href === path || path.startsWith(href));
  });
}

// ── Reloj ─────────────────────────────────────
function startClock() {
  const els = document.querySelectorAll('.nav-clock, #nav-clock, .tb-clock');
  const tick = () => {
    const t = new Date().toLocaleTimeString('es-CO', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
    els.forEach(el => { if (el) el.textContent = t; });
  };
  tick(); setInterval(tick, 1000);
}

// ── API helper ────────────────────────────────
const API = {
  async get(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  },
  async post(url, body) {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({ detail: r.statusText }));
      throw new Error(err.detail || 'Error del servidor');
    }
    return r.json();
  }
};

// ── Notificaciones flotantes ──────────────────
function showNotif(icon, title, body, duration = 3500) {
  let area = document.getElementById('notif-area');
  if (!area) {
    area = document.createElement('div');
    area.id = 'notif-area';
    area.style.cssText = 'position:fixed;top:62px;right:16px;display:flex;flex-direction:column;gap:7px;z-index:9999;pointer-events:none;';
    document.body.appendChild(area);
  }
  const n = document.createElement('div');
  n.style.cssText = `background:rgba(6,16,30,.98);border:1px solid #2e6aaa;border-radius:3px;
    padding:10px 14px;width:275px;display:flex;gap:9px;align-items:flex-start;
    animation:slideIn .35s ease;box-shadow:0 4px 20px rgba(0,0,0,.7);
    font-family:'Exo 2',sans-serif;pointer-events:all;`;
  n.innerHTML = `
    <span style="font-size:16px;flex-shrink:0;margin-top:1px">${icon}</span>
    <div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#33ddff;margin-bottom:2px">${title}</div>
      <div style="font-size:11px;color:#7aaad0;line-height:1.5">${body}</div>
    </div>`;
  area.appendChild(n);
  if (!document.getElementById('notif-style')) {
    const s = document.createElement('style');
    s.id = 'notif-style';
    s.textContent = '@keyframes slideIn{from{transform:translateX(110%);opacity:0}to{transform:translateX(0);opacity:1}}';
    document.head.appendChild(s);
  }
  setTimeout(() => {
    n.style.transition = 'opacity .35s, transform .35s';
    n.style.opacity = '0'; n.style.transform = 'translateX(80px)';
    setTimeout(() => n.remove(), 370);
  }, duration);
}

// ── Guard de sesión ───────────────────────────
function requireAuth() {
  // Si está en iframe, no redirigir — la sesión llega por postMessage desde el desktop
  if (window.self !== window.top) return true;
  if (!sessionStorage.getItem('dlk_user')) {
    window.location.href = '/login';
    return false;
  }
  return true;
}

// ── Logout ────────────────────────────────────
function doLogout() {
  sessionStorage.removeItem('dlk_user');
  window.location.href = '/login';
}

// ── Init ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setActiveNav();
  startClock();
});
