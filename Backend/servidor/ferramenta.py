from PIL import Image
from pyzbar.pyzbar import decode as lerqrcode
from io import BytesIO


def extrair_codigo_de_barras(imagem):
    imagem = Image.open(BytesIO(imagem.read()))
    codigo_de_barras = lerqrcode(imagem)

    if len(codigo_de_barras) == 0:
        return None

    return codigo_de_barras[0].data.decode("utf-8")
