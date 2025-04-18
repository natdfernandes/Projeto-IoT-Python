from PIL import Image
from pyzbar.pyzbar import decode as lerqrcode


def extrair_codigo_de_barras(caminho_imagem: str):
    imagem = Image.open(caminho_imagem)
    codigo_de_barras = lerqrcode(imagem)
    return codigo_de_barras[0].data.decode("utf-8")


print(extrair_codigo_de_barras("./imagens/codigo-de-barras.jpg"))
