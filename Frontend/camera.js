const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const capture = document.getElementById('capture');
const novaCaptura = document.getElementById('nova-captura');

// Pede permissão para usar a câmera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('Erro ao acessar a câmera:', err);
    });

// Captura a imagem da câmera
capture.addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    capture.style.display = 'none';
    video.style.display = 'none';
    enviar.style.display = 'block';
    canvas.style.display = 'block';
    novaCaptura.style.display = 'block';
});

novaCaptura.addEventListener('click', () => {
    capture.style.display = 'block';
    video.style.display = 'block';
    enviar.style.display = 'none';
    canvas.style.display = 'none';
    novaCaptura.style.display = 'none';
    enviarSalvo.value = '';
})

