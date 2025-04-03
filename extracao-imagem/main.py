from PIL import Image
import pytesseract
from os import listdir
from pytesseract import Output

# Precisa apontar para onde a ferramenta do tesseract foi instalada em sua máquina
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\natal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def extrair_dados_da_imagem(imagem: str):
    config = r"--psm 6"
    return pytesseract.image_to_data(
        Image.open(imagem),
        lang="por+eng",
        config=config,
        output_type=Output.DICT,
    )


def extrair_texto_legivel(textos: list[str]):
    texto_do_livro = ""
    for texto in textos:
        if texto != "":
            texto_do_livro = texto_do_livro + " " + texto

    return texto_do_livro.strip()


pasta_imagens = "./imagens"

for imagem in listdir(pasta_imagens):
    dados_imagem = extrair_dados_da_imagem("{0}/{1}".format(pasta_imagens, imagem))

    print(extrair_texto_legivel(dados_imagem["text"]))
