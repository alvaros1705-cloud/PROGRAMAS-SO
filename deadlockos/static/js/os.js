/* ══════════════════════════════════════════════
   DeadlockOS — os.js
══════════════════════════════════════════════ */

/* ── Toast ─────────────────────────────────── */
function toast(icon, title, msg, dur = 3500) {
  let area = document.getElementById('toast-area');
  if (!area) {
    area = document.createElement('div');
    area.id = 'toast-area';
    document.body.appendChild(area);
  }
  const t = document.createElement('div');
  t.className = 'toast'; t.style.position = 'relative';
  t.innerHTML = `
    <div class="toast-icon">${icon}</div>
    <div class="toast-body">
      <div class="toast-title">${title}</div>
      <div class="toast-msg">${msg}</div>
    </div>
    <div class="toast-close" onclick="this.closest('.toast').remove()">✕</div>
    <div class="toast-bar"><div class="toast-bar-fill" style="--dur:${dur}ms"></div></div>`;
  area.appendChild(t);
  setTimeout(() => {
    t.style.transition = 'opacity .3s,transform .3s';
    t.style.opacity = '0'; t.style.transform = 'translateX(80px)';
    setTimeout(() => t.remove(), 320);
  }, dur);
}

/* ── initOS — llamado desde desktop.html ─── */
function initOS() {

  /* ── Power menu ─────────────────────────── */
  window.togglePowerMenu = function() {
    document.getElementById('power-menu').classList.toggle('show');
  };
  window.closePowerMenu = function() {
    document.getElementById('power-menu').classList.remove('show');
  };

  /* ── Alt+Tab ────────────────────────────── */
  let atShowing = false, atIdx = 0;

  window.altTabSelect = function(id) {
    closeAltTab();
    if (windows[id]) {
      windows[id].el.classList.remove('minimized');
      windows[id].minimized = false;
      focusWindow(id); updateTaskbar();
    }
  };

  function openAltTab() {
    const ids = Object.keys(windows); if (!ids.length) return;
    const el = document.getElementById('alt-tab');
    el.innerHTML = ids.map((id, i) => {
      const app = APPS[id];
      return `<div class="at-item ${i===0?'sel':''}" onclick="altTabSelect('${id}')">
        <div class="at-icon">${app.icon}</div>
        <div class="at-label">${app.title}</div>
      </div>`;
    }).join('');
    el.classList.add('show'); atShowing = true; atIdx = 0;
  }

  function closeAltTab() {
    document.getElementById('alt-tab').classList.remove('show'); atShowing = false;
  }

  function altTabCycle() {
    const ids = Object.keys(windows); if (!ids.length) return;
    if (!atShowing) { openAltTab(); return; }
    atIdx = (atIdx+1) % ids.length;
    document.querySelectorAll('.at-item').forEach((el,i) => el.classList.toggle('sel', i===atIdx));
  }

  /* ── Teclado ────────────────────────────── */
  document.addEventListener('keydown', e => {
    if (e.altKey && e.key === 'Tab') { e.preventDefault(); altTabCycle(); return; }
    if ((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==='w') {
      e.preventDefault();
      const f = Object.keys(windows).find(k => windows[k].el.classList.contains('focused'));
      if (f) closeApp(f);
    }
    if (e.key === 'Escape') {
      closeAltTab();
      document.getElementById('wallpaper-menu')?.classList.remove('show');
      closePowerMenu();
    }
  });

  document.addEventListener('keyup', e => {
    if (e.key === 'Alt' && atShowing) {
      const ids = Object.keys(windows);
      if (ids[atIdx]) altTabSelect(ids[atIdx]);
    }
  });

  /* ── Click fuera cierra menús ───────────── */
  document.addEventListener('click', e => {
    if (e.target.closest('.tb-logo')) return; // el botón DLK maneja su propio toggle
    if (!e.target.closest('#power-menu')) closePowerMenu();
    if (!e.target.closest('#wallpaper-menu') &&
        !e.target.closest('[title="Cambiar fondo"]')) {
      document.getElementById('wallpaper-menu')?.classList.remove('show');
    }
  });

  /* ── Reloj ──────────────────────────────── */
  const timeEl = document.getElementById('tb-time');
  const dateEl = document.getElementById('tb-date');
  const tick = () => {
    const now = new Date();
    if (timeEl) timeEl.textContent = now.toLocaleTimeString('es-CO', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
    if (dateEl) dateEl.textContent = now.toLocaleDateString('es-CO', {weekday:'short',day:'2-digit',month:'short'});
  };
  tick(); setInterval(tick, 1000);

  /* ── Toasts bienvenida ──────────────────── */
  setTimeout(() => toast('💡','BIENVENIDO','Doble clic en un ícono para abrir cada módulo.'), 800);
  setTimeout(() => toast('⌨️','ATAJOS','Alt+Tab: cambiar ventana  ·  Ctrl+W: cerrar', 5000), 3500);

} // fin initOS
