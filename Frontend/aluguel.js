const enviar = document.getElementById('enviar');
const enviarSalvo = document.getElementById('enviar-salvo');


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
        formData.append('isbn', blob, 'captura.jpg');

        fetch('http://localhost:8080/livro/aluguel', {
            method: 'PATCH',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                alert(data.error ?? data.message);
            })
            .catch(error => {
                console.error('Erro ao enviar a imagem:', error);
            });
    }, 'image/jpeg');
});