// ==========================
// ESTADO DEL DISCO
// ==========================

let health = 100;

// ==========================
// REFERENCIAS
// ==========================

const healthBar = document.getElementById("health-bar");
const healthText = document.getElementById("health-text");
const diskStatus = document.getElementById("disk-status");

const diagnosticContent =
document.getElementById("diagnostic-content");

const questionSection =
document.getElementById("question-section");

const answersContainer =
document.getElementById("answers-container");

const resultSection =
document.getElementById("result-section");

const resultTitle =
document.getElementById("result-title");

const resultMessage =
document.getElementById("result-message");

const historyList =
document.getElementById("history-list");

const buttons =
document.querySelectorAll(".error-btn");

// ==========================
// BASE DE DATOS DE ERRORES
// ==========================

const errors = {

badsector:{
title:"Sectores Defectuosos",
damage:25,
description:`
<h3> Sectores Defectuosos</h3>
<p>Se detectaron sectores dañados físicamente dentro del disco.</p>
<b>Síntomas:</b>
<ul>
<li>Archivos corruptos</li>
<li>Lentitud extrema</li>
<li>Errores al copiar archivos</li>
</ul>
`,
answers:[
"Ejecutar herramientas de verificación del disco y realizar una copia de seguridad preventiva de los datos",
"Incrementar la memoria RAM para mejorar el acceso a los archivos",
"Modificar los permisos de usuario del sistema operativo",
"Actualizar los controladores de video del equipo"
],
correct:0
},

full:{
title:"Disco Lleno",
damage:15,
description:`
<h3> Disco Lleno</h3>
<p>El almacenamiento disponible es insuficiente.</p>
<b>Síntomas:</b>
<ul>
<li>Sistema lento</li>
<li>No se pueden guardar archivos</li>
<li>Actualizaciones fallidas</li>
</ul>
`,
answers:[
"Desfragmentar el disco para recuperar espacio disponible",
"Eliminar archivos innecesarios y trasladar información a un medio de almacenamiento externo",
"Actualizar el sistema operativo a una versión más reciente",
"Modificar la configuración de energía del equipo"
],
correct:1
},

smart:{
title:"SMART Failure",
damage:35,
description:`
<h3> Error SMART</h3>
<p>El sistema SMART predice una falla próxima del disco.</p>
<b>Síntomas:</b>
<ul>
<li>Bloqueos frecuentes</li>
<li>Pérdida de datos</li>
<li>Advertencias del sistema</li>
</ul>
`,
answers:[
"Respaldar inmediatamente la información crítica y programar el reemplazo del dispositivo",
"Formatear completamente la unidad para eliminar los errores detectados",
"Desactivar las alertas SMART desde la BIOS",
"Ejecutar una desfragmentación completa del disco"
],
correct:0
},

corruption:{
title:"Corrupción del Sistema de Archivos",
damage:20,
description:`
<h3> Corrupción del Sistema de Archivos</h3>
<p>La estructura lógica de almacenamiento presenta daños.</p>
<b>Síntomas:</b>
<ul>
<li>Archivos ilegibles</li>
<li>Carpetas desaparecidas</li>
<li>Errores de acceso</li>
</ul>
`,
answers:[
"Incrementar el espacio libre de la partición afectada",
"Reparar la estructura lógica del sistema de archivos y verificar la integridad de los datos",
"Actualizar los controladores de red del sistema",
"Modificar la tabla de particiones manualmente sin realizar respaldos"
],
correct:1
},

overheat:{
title:"Sobrecalentamiento",
damage:20,
description:`
<h3> Sobrecalentamiento</h3>
<p>El disco trabaja a temperaturas superiores a las recomendadas.</p>
<b>Síntomas:</b>
<ul>
<li>Reducción de rendimiento</li>
<li>Apagados inesperados</li>
<li>Mayor desgaste</li>
</ul>
`,
answers:[
"Mejorar la ventilación del sistema y monitorear la temperatura mediante herramientas especializadas",
"Incrementar la velocidad de conexión a Internet",
"Reducir la resolución de pantalla para disminuir el consumo energético",
"Actualizar las aplicaciones instaladas en el equipo"
],
correct:0
},

readwrite:{
title:"Error de Lectura y Escritura",
damage:30,
description:`
<h3> Error de Lectura y Escritura</h3>
<p>El sistema tiene dificultades para acceder o guardar información.</p>
<b>Síntomas:</b>
<ul>
<li>Archivos dañados</li>
<li>Congelamientos</li>
<li>Errores frecuentes</li>
</ul>
`,
answers:[
"Verificar la integridad física del disco y realizar un respaldo inmediato de la información importante",
"Actualizar los controladores de audio del sistema",
"Deshabilitar temporalmente el firewall del sistema operativo",
"Modificar la configuración de la impresora predeterminada"
],
correct:0
},

fragmentation:{
title:"Fragmentación Excesiva",
damage:10,
description:`
<h3> Fragmentación Excesiva</h3>
<p>Los archivos están dispersos en múltiples ubicaciones del disco.</p>
<b>Síntomas:</b>
<ul>
<li>Acceso lento a datos</li>
<li>Mayor tiempo de carga</li>
</ul>
`,
answers:[
"Ejecutar un proceso de desfragmentación para optimizar la ubicación física de los archivos",
"Ampliar la memoria RAM disponible",
"Actualizar los controladores gráficos del sistema",
"Reinstalar el navegador principal del equipo"
],
correct:0
},

ssdwear:{
title:"Desgaste SSD",
damage:25,
description:`
<h3> Desgaste SSD</h3>
<p>Las celdas NAND están alcanzando su límite de escritura.</p>
<b>Síntomas:</b>
<ul>
<li>Pérdida de rendimiento</li>
<li>Bloques defectuosos</li>
</ul>
`,
answers:[
"Monitorear los indicadores SMART y planificar el reemplazo de la unidad antes de una falla crítica",
"Ejecutar una desfragmentación periódica para mejorar el rendimiento",
"Reducir la resolución de pantalla del sistema",
"Modificar los permisos de acceso a los archivos"
],
correct:0
},

malware:{
title:"Malware",
damage:20,
description:`
<h3> Infección por Malware</h3>
<p>Software malicioso afecta archivos y recursos del sistema.</p>
<b>Síntomas:</b>
<ul>
<li>Archivos eliminados</li>
<li>Lentitud extrema</li>
<li>Actividad sospechosa</li>
</ul>
`,
answers:[
"Realizar un análisis completo con herramientas antimalware actualizadas y verificar la integridad de los archivos",
"Incrementar la capacidad de almacenamiento de la unidad",
"Actualizar los controladores de la tarjeta gráfica",
"Reducir el número de usuarios registrados en el sistema"
],
correct:0
},

mechanical:{
title:"Fallo Mecánico HDD",
damage:40,
description:`
<h3>⚙️ Fallo Mecánico HDD</h3>
<p>Existe daño físico en platos o cabezales del disco duro.</p>
<b>Síntomas:</b>
<ul>
<li>Ruido extraño</li>
<li>Imposible acceder a datos</li>
<li>Bloqueos constantes</li>
</ul>
`,
answers:[
"Respaldar inmediatamente la información accesible y sustituir la unidad de almacenamiento",
"Formatear la partición principal para corregir el problema",
"Actualizar el sistema operativo a una versión más reciente",
"Modificar la configuración de arranque de la BIOS"
],
correct:0
}

};

// ==========================
// EVENTOS BOTONES
// ==========================

buttons.forEach(button=>{

button.addEventListener("click",()=>{

const type = button.dataset.error;

simulateError(type);

});

});

// ==========================
// SIMULAR ERROR
// ==========================

function simulateError(type){

const error = errors[type];

health -= error.damage;

if(health < 0){
health = 0;
}

updateHealth();

diagnosticContent.innerHTML =
error.description;

questionSection.classList.remove("hidden");

resultSection.classList.add("hidden");

answersContainer.innerHTML = "";

error.answers.forEach((answer,index)=>{

const btn =
document.createElement("button");

btn.classList.add("answer-btn");

btn.textContent = answer;

btn.addEventListener("click",()=>{

validateAnswer(
index,
error.correct,
error.title
);

});

answersContainer.appendChild(btn);

});

addHistory(
`Error simulado: ${error.title}`
);

}

// ==========================
// VALIDAR RESPUESTA
// ==========================

function validateAnswer(
selected,
correct,
errorName
){

resultSection.classList.remove("hidden");

if(selected === correct){

health += 15;

if(health > 100){
health = 100;
}

updateHealth();

resultTitle.innerHTML =
"✅ Diagnóstico Correcto";

resultTitle.className =
"success";

resultMessage.innerHTML =
"Excelente. La solución seleccionada es la más adecuada para el problema detectado.";

addHistory(
`Diagnóstico correcto: ${errorName}`
);

}else{

health -= 10;

if(health < 0){
health = 0;
}

updateHealth();

resultTitle.innerHTML =
"❌ Diagnóstico Incorrecto";

resultTitle.className =
"danger";

resultMessage.innerHTML =
"La solución elegida no corrige el problema y aumenta el riesgo de falla.";

addHistory(
`Diagnóstico incorrecto: ${errorName}`
);

}

checkDiskState();

}

// ==========================
// SALUD DEL DISCO
// ==========================

function updateHealth(){

healthBar.style.width =
health + "%";

healthText.textContent =
health + "%";

if(health > 70){

diskStatus.textContent =
"Operativo";

diskStatus.className =
"success";

}else if(health > 40){

diskStatus.textContent =
"Advertencia";

diskStatus.className =
"warning";

}else{

diskStatus.textContent =
"Crítico";

diskStatus.className =
"danger";

}

}

// ==========================
// HISTORIAL
// ==========================

function addHistory(text){

const li =
document.createElement("li");

li.textContent =
new Date().toLocaleTimeString()
+ " - " + text;

historyList.prepend(li);

}

// ==========================
// COMPROBAR ESTADO
// ==========================

function checkDiskState(){

if(health <= 0){

diagnosticContent.innerHTML = `
<h2 style="color:#ef4444">
 DISCO FUERA DE SERVICIO
</h2>

<p>
La salud del disco ha llegado a 0%.
El sistema ya no puede operar correctamente.
</p>
`;

questionSection.classList.add("hidden");

resultSection.classList.add("hidden");

buttons.forEach(btn=>{

btn.disabled = true;
btn.style.opacity = ".5";

});

}

}

// ==========================
// INICIAR
// ==========================

updateHealth();