from PIL import Image
import pytesseract
from pytesseract import Output

# Precisa apontar para onde a ferramenta do tesseract foi instalada em sua máquina
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\natal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
config = r"--psm 11"

for i in range(7):
    posicao = i + 1
    print("Lendo imagem de número {0}".format(posicao))

    dados_imagem = pytesseract.image_to_data(
        Image.open("./imagens/IMG-20250330-WA000{0}.jpg".format(posicao)),
        lang="por",
        config=config,
        output_type=Output.DICT,
    )

    texto_do_livro = ""
    for texto in dados_imagem["text"]:
        if texto != "":
            texto_do_livro = texto_do_livro + " " + texto

    print(texto_do_livro.strip())
