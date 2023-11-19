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

    im_nome = Image.new("RGBA", (W, H//2), (255, 255, 255))
    draw_nome = ImageDraw.Draw(im_nome)

    if not os.path.exists("output"):
        os.makedirs("output")

    if not os.path.exists("output/orizzontali"):
        os.makedirs("output/orizzontali")

    if not os.path.exists("output/triangoli"):
        os.makedirs("output/triangoli")


    for nome in nomi:

        imc_o = im.copy()
        imc_t = im.copy()
        drawc_o = ImageDraw.Draw(imc_o)
        drawc_t = ImageDraw.Draw(imc_t)

        im_nomec = im_nome.copy()
        draw_nomec = ImageDraw.Draw(im_nomec)

        # mi aspetto di ricevere camere con nomi del tipo: 100, 200, .. oppure 'Tavolo 1', 'Appartamento 1', ...

        if len(nome.split()) > 1:
            centerTextV(draw_nomec, nome.split()[0], font_not_really_big, color, H//2, -160)
            centerTextV(draw_nomec, nome.split()[1], font_really_big, color, H//2, 70)
        else:
            centerTextV(draw_nomec, nome, font_really_big, color, H//2)

        imc_o.paste(im_nomec)
        imc_t.paste(im_nomec.rotate(180))

        imc_o.save('output/orizzontali/'+nome+'.png', 'PNG', dpi=(300, 300))
        imc_t.save('output/triangoli/'+nome+'.png', 'PNG', dpi=(300, 300))
        print(nome, "--> OK")

    packprint.packprint("output/triangoli.pdf", ["output/triangoli/"+nome+".png" for nome in nomi])
    packprint.packprint("output/orizzontali.pdf", ["output/orizzontali/"+nome+".png" for nome in nomi])

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
