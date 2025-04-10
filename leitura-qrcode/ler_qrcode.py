from PIL import Image
from pyzbar.pyzbar import decode as lerqrcode

imagem = Image.open("./imagens/codigo-de-barras.jpg")
conteudo_qrcode = lerqrcode(imagem)

print(conteudo_qrcode)
print("*" * 50)
print(conteudo_qrcode[0].data.decode("utf-8"))
