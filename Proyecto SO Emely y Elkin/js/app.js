// app.js - Manejo de la Interfaz de Usuario y Navegación

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
});

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.module-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remover active de todos
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Añadir active al clickeado
            link.classList.add('active');
            
            // Mostrar sección
            const targetId = link.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
            
            // Scroll arriba suave
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}
