document.addEventListener('DOMContentLoaded', function () {
 
    // ========================================
    // MOBILE MENU TOGGLE
    // ========================================
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
 
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function () {
            mobileMenu.classList.toggle('active');
            const isOpen = mobileMenu.classList.contains('active');
            menuToggle.innerHTML = isOpen
                ? '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>'
                : '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>';
        });
 
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                menuToggle.innerHTML = '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>';
            });
        });
    }
 
    // ========================================
    // NAVBAR SCROLL EFFECT
    // ========================================
    const mainNav = document.getElementById('mainNav');
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 80) {
            mainNav.style.top = '0';
        } else {
            mainNav.style.top = '36px';
        }
    });
 
    // ========================================
    // ACTIVE NAV LINK ON SCROLL
    // ========================================
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a, .mobile-menu a');
 
    function updateActiveLink() {
        const scrollY = window.pageYOffset + 120;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollY >= top && scrollY < top + height) {
                navLinks.forEach(a => {
                    a.classList.remove('active');
                    if (a.getAttribute('href') === '#' + id) {
                        a.classList.add('active');
                    }
                });
            }
        });
    }
    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink();
 
    // ========================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
 
    // ========================================
    // SCROLL REVEAL ANIMATIONS
    // ========================================
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
 
    function addRevealClasses() {
        document.querySelectorAll('.section-header').forEach(el => {
            el.classList.add('reveal');
        });
        document.querySelectorAll('.algo-card').forEach((el, i) => {
            el.classList.add('reveal', `reveal-delay-${Math.min(i + 1, 4)}`);
        });
        document.querySelectorAll('.condition-card').forEach((el, i) => {
            el.classList.add('reveal', `reveal-delay-${Math.min(i + 1, 4)}`);
        });
        document.querySelectorAll('.comp-item').forEach((el, i) => {
            el.classList.add('reveal', 'reveal-left', `reveal-delay-${Math.min(i + 1, 4)}`);
        });
        document.querySelectorAll('.step-card').forEach((el, i) => {
            el.classList.add('reveal', `reveal-delay-${Math.min(i + 1, 4)}`);
        });
        document.querySelectorAll('.pros-box, .cons-box').forEach((el, i) => {
            el.classList.add('reveal', i === 0 ? 'reveal-left' : 'reveal-right');
        });
        document.querySelectorAll('.conclusion-box, .safe-state-box, .formula-box, .info-card').forEach(el => {
            el.classList.add('reveal');
        });
 
        document.querySelectorAll('.reveal').forEach(el => {
            revealObserver.observe(el);
        });
    }
 
    addRevealClasses();
 
    // ========================================
    // BOTÓN IMAGEN EXPLICATIVA — FUNCIONAMIENTO
    // ========================================
    const howImgBtn     = document.getElementById('howImgBtn');
    const howImgOverlay = document.getElementById('howImgOverlay');
    const howImgClose   = document.getElementById('howImgClose');

    if (howImgBtn && howImgOverlay) {
        howImgBtn.addEventListener('click', () => {
            howImgOverlay.classList.toggle('open');
        });
        howImgClose.addEventListener('click', () => {
            howImgOverlay.classList.remove('open');
        });
        howImgOverlay.addEventListener('click', (e) => {
            if (e.target === howImgOverlay) howImgOverlay.classList.remove('open');
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') howImgOverlay.classList.remove('open');
        });
    }

    console.log('⚙️ Algoritmo del Banquero cargado correctamente!');
});