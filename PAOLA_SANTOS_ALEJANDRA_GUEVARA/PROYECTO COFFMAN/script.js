function iniciar(){

    document.getElementById("p1").innerHTML =
    "Usando R1";

    document.getElementById("p2").innerHTML =
    "Usando R2";

    document.getElementById("r1").innerHTML =
    "Ocupado por P1";

    document.getElementById("r2").innerHTML =
    "Ocupado por P2";

    let estado =
    document.getElementById("estado");

    estado.className = "normal";

    estado.innerHTML =
    "Sistema funcionando correctamente";
}

function deadlock(){

    document.getElementById("p1").innerHTML =
    "Esperando R2";

    document.getElementById("p2").innerHTML =
    "Esperando R1";

    let estado =
    document.getElementById("estado");

    estado.className = "bloqueo";

    estado.innerHTML =
    "⚠ DEADLOCK DETECTADO ⚠";
}

function reiniciar(){

    document.getElementById("p1").innerHTML =
    "Esperando...";

    document.getElementById("p2").innerHTML =
    "Esperando...";

    document.getElementById("r1").innerHTML =
    "Libre";

    document.getElementById("r2").innerHTML =
    "Libre";

    let estado =
    document.getElementById("estado");

    estado.className = "";

    estado.innerHTML =
    "Esperando simulación...";
}