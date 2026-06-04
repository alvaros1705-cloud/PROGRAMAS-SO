# OVA: Características y Optimización de la Planificación de Procesos

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

Objeto Virtual de Aprendizaje (OVA) profesional, académico e interactivo enfocado en enseñar los fundamentos, algoritmos y métricas de la Planificación de Procesos de CPU en Sistemas Operativos.

## 🎯 Objetivos

- **Comprender** la necesidad y la función del planificador de procesos (Scheduler).
- **Analizar** las métricas críticas: tiempo de espera, de retorno y throughput.
- **Simular** empíricamente 5 algoritmos clásicos de planificación.
- **Evaluar** la comprensión mediante cuestionarios interactivos.

## ✨ Características

- **Sin Frameworks**: Desarrollado 100% en HTML5, CSS3 y Vanilla JavaScript, garantizando una carga instantánea y cero dependencias pesadas.
- **Dashboard Analítico**: Integración con *Chart.js* para visualizar comparativas de rendimiento en tiempo real.
- **Simulador Interactivo**: Ejecución de FCFS, SJF, Round Robin, Prioridades y Colas Multinivel sobre 4 escenarios de carga diferentes (hasta 500 procesos simultáneos).
- **Diagrama de Gantt Animado**: Visualización gráfica del uso de la CPU.
- **Evaluación**: Quiz dinámico de 20 preguntas con retroalimentación automática.
- **Dark Mode Moderno**: UI/UX diseñada bajo estándares actuales, enfocada en accesibilidad y confort visual.

## 🛠 Tecnologías Utilizadas

- **HTML5** (Semántico)
- **CSS3** (Variables Globales, Flexbox, CSS Grid, Animaciones keyframes)
- **Vanilla JavaScript** (ES6+, DOM Manipulation, Event Listeners)
- **Chart.js** (vía CDN para gráficas analíticas)

## 🚀 Instalación y Uso

Dado que el proyecto no usa frameworks de Node.js ni bases de datos complejas, la instalación es inmediata:

1. **Clona este repositorio:**
   \`\`\`bash
   git clone https://github.com/tu-usuario/ova-planificacion-procesos.git
   \`\`\`
2. **Navega al directorio:**
   \`\`\`bash
   cd ova-planificacion-procesos
   \`\`\`
3. **Ejecuta el proyecto:**
   Simplemente abre el archivo \`index.html\` en cualquier navegador moderno (Chrome, Firefox, Edge, Safari).
   Para una experiencia óptima, puedes usar la extensión "Live Server" de VS Code.

## 📁 Estructura del Proyecto

\`\`\`text
/
├── index.html              # Estructura principal y maquetación de los 9 módulos
├── README.md               # Documentación principal
├── LICENSE                 # Licencia MIT
├── assets/                 # Recursos gráficos (iconos, diagramas)
├── css/
│   ├── style.css           # Estilos base, variables de color y tipografía
│   ├── responsive.css      # Reglas Media Queries
│   └── animations.css      # Efectos y animaciones
├── js/
│   ├── app.js              # Navegación del menú y UX base
│   ├── data-content.js     # Inyección de contenido académico extenso
│   ├── algorithms.js       # Lógica matemática de los 5 planificadores
│   ├── simulator.js        # Integración DOM, Diagrama de Gantt y cola
│   ├── charts.js           # Lógica del Dashboard con Chart.js
│   └── quiz.js             # Módulo de evaluación de 20 preguntas
├── data/
│   └── scenarios.json      # Definición estática de escenarios (A y B)
└── docs/
    ├── experiment-report.md # Informe de diseño del experimento
    └── user-manual.md       # Manual de usuario detallado
\`\`\`

## 👥 Integrantes (Autores Oficiales)

- **Emely Yanieth Lozano Baez**
- **Elkin Alonso Torres Sandoval**

*Nota de la Versión 2.0: Este proyecto ha sido refactorizado para utilizar una nueva identidad visual institucional, contenido interactivo, un simulador libre de dependencias de servidor (CORS resuelto) y un módulo de evaluación de 10 preguntas con retroalimentación inmediata.*

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Siéntete libre de usarlo, modificarlo y distribuirlo con fines académicos o comerciales. Revisa el archivo \`LICENSE\` para más detalles.
