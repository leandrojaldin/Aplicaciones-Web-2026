// Efecto de máquina de escribir para el título secundario
const textElement = document.getElementById('typing-text');
const phrases = [
    "Estudiante de Ingeniería de Software.",
    "Apasionado por la tecnología.",
    "Desarrollador Web."
];
let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
        textElement.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;
    } else {
        textElement.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
    }

    // Velocidad de escritura
    let speed = isDeleting ? 50 : 100;

    // Lógica para cambiar de frase
    if (!isDeleting && charIndex === currentPhrase.length) {
        speed = 2000; // Pausa al terminar de escribir
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        speed = 500; // Pausa antes de empezar a escribir la nueva frase
    }

    setTimeout(typeEffect, speed);
}

// Iniciar el efecto cuando la página cargue
document.addEventListener("DOMContentLoaded", () => {
    typeEffect();
});