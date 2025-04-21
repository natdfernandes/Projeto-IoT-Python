const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const capture = document.getElementById('capture');
const enviar = document.getElementById('enviar');
const novaCaptura = document.getElementById('nova-captura');
const enviarSalvo = document.getElementById('enviar-salvo');

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

enviarSalvo.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const img = new Image();

            img.onload = function () {
                // Ajusta o canvas para o tamanho da imagem
                canvas.width = img.width;
                canvas.height = img.height;

                // Desenha a imagem no canvas
                context.drawImage(img, 0, 0);
            };

            img.src = e.target.result;
            capture.style.display = 'none';
            video.style.display = 'none';
            enviar.style.display = 'block';
            canvas.style.display = 'block';
            novaCaptura.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        alert('Por favor, selecione uma imagem válida.');
    }
});

// Envia a imagem capturada para uma API
enviar.addEventListener('click', () => {
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('imagem', blob, 'captura.jpg');

        fetch('https://sua-api.com/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log('Sucesso:', data);
                alert('Imagem enviada com sucesso!');
            })
            .catch(error => {
                console.error('Erro ao enviar a imagem:', error);
            });
    }, 'image/jpeg');
});