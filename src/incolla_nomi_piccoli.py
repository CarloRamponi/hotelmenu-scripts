#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import json
import time
from textwrap import wrap
import platform
import packprint

def createImages(img, nomi, color):

    W, H = 1060, 1335
    QRSIZE = 330
    QRPAD = 60

    font = ImageFont.truetype("grafiche/poppins.ttf", 34)
    font_big = ImageFont.truetype("grafiche/poppins.ttf", 50)
    font_bigger = ImageFont.truetype("grafiche/poppins.ttf", 80)
    font_not_really_big = ImageFont.truetype("grafiche/poppins.ttf", 100)
    font_really_big = ImageFont.truetype("grafiche/poppins.ttf", 450)

    def centerText(draw, msg, height, font, color, W=W, OFFSET=0):
        w, h = draw.textsize(msg, font=font);
        draw.text((OFFSET+(W-w)/2, height), msg, color, font=font)

    def centerTextV(draw, msg, font, color, H, H_OFFST=0):
        w, h = draw.textsize(msg, font=font);
        draw.text(((W-w)/2, ((H-80)-h)/2 + H_OFFST), msg, color, font=font)

    im = Image.open(img)

    if not os.path.exists("output"):
        os.makedirs("output")

    for nome in nomi:

        imc_t = im.copy()
        drawc_t = ImageDraw.Draw(imc_t)

        w, h = drawc_t.textsize(nome, font=font_bigger);
        im_nome = Image.new("RGBA", (w, h), (255, 255, 255))
        draw_nome = ImageDraw.Draw(im_nome)
        draw_nome.text((0, 0), nome, color, font=font_bigger)

        imc_t.paste(im_nome.rotate(180), ((W-w)//2, (H//2 - 40 - h)))

        imc_t.save('output/'+nome+'.png', 'PNG', dpi=(300, 300))
        print(nome, "--> OK")

    packprint.packprint("output/output.pdf", ["output/"+nome+".png" for nome in nomi])

    print("PDF generated in output/")

def main():
    if(len(sys.argv) < 3):
        print("usage: ./incolla_nomi.py immagine json_file([nome1, nome2, ...]) color(RRGGBB)")
        sys.exit(1)

    img = sys.argv[1]

    with open(sys.argv[2], "r") as f:
        nomi = json.loads(f.read())

    color = tuple(int(a, 16) for a in wrap(sys.argv[3], 2))

    createImages(img, nomi, color)

    print("immagini create in output/")

if __name__ == "__main__":
    main()

# createImages("demo", [{'nome' : "100", 'codice' : 'ABCD'}, {'nome' : "102", 'codice' : 'GH64'}], 'grafiche/logo.png', ['it', 'en', 'de'], (1, 117, 33))
