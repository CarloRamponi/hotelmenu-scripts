#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import qr
import sys
import os
import json
import time
from textwrap import wrap
import platform
import packprint

def createImages(subdomain, codice, nomi, logo, langs, color):

    W, H = 1060, 1335
    QRSIZE = 330
    QRPAD = 60

    SITE_CODE = "https://{}.hotelmenu.it/?c={}"
    SITE_VISUAL = "{}.hotelmenu.it"

    STRINGS = {
        "it" : [
            "Appoggia il tuo smartphone,",
            "oppure scansiona il codice, oppure visita:"
        ],
        "en" : [
            "Tap with your smartphone, or scan the code, or visit:",
        ],
        "de" : [
            "Tippen Sie mit Ihrem Smartphone auf,",
            "scannen Sie den Code oder besuchen Sie:"
        ],
        "po" : [
            "Stuknij w smartfonie lub zeskanuj kod lub odwiedź:"
        ],
        "fr" : [
            "Appuyez avec votre smartphone, ou scannez le code, ou visitez:"
        ]
    }

    STRINGS_BOTTOM = {
        "it" : "e inserisci:",
        "en" : "and enter:",
        "de" : "und geben Sie ein:",
        "po" : "i wprowadź:",
        "fr" : "et entrez:"
    }

    font = ImageFont.truetype("grafiche/poppins.ttf", 34)
    font_big = ImageFont.truetype("grafiche/poppins.ttf", 50)
    font_bigger = ImageFont.truetype("grafiche/poppins.ttf", 80)
    font_not_really_big = ImageFont.truetype("grafiche/poppins.ttf", 100)
    font_really_big = ImageFont.truetype("grafiche/poppins.ttf", 450)

    INTRA_PADDING = 38
    INTER_PADDING = 12
    START_HEIGTH = H//2 + 30

    def centerText(draw, msg, height, font, color, W=W, OFFSET=0):
        w, h = draw.textsize(msg, font=font);
        draw.text((OFFSET+(W-w)/2, height), msg, color, font=font)

    def centerTextV(draw, msg, font, color, H, H_OFFST=0):
        w, h = draw.textsize(msg, font=font);
        draw.text(((W-w)/2, ((H-80)-h)/2 + H_OFFST), msg, color, font=font)

    im = Image.new("RGBA", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    im_nome = Image.new("RGBA", (W, H//2), (255, 255, 255))
    draw_nome = ImageDraw.Draw(im_nome)

    height = START_HEIGTH;

    for l in langs:
        for s in STRINGS[l]:
            centerText(draw, s, height, font, color)
            height += INTRA_PADDING
        height += INTER_PADDING

    height_1 = height + 35

    centerText(draw, SITE_VISUAL.format(subdomain), height_1, font_big, color, W - (QRSIZE + QRPAD))

    height_1 += 70

    for l in langs:
        centerText(draw, STRINGS_BOTTOM[l], height_1, font, color, W - (QRSIZE + QRPAD), 0)
        height_1 += 50

    if not os.path.exists("output"):
        os.makedirs("output")

    if not os.path.exists("output/orizzontali"):
        os.makedirs("output/orizzontali")

    if not os.path.exists("output/triangoli"):
        os.makedirs("output/triangoli")

    height_1 += 20

    logo = qr.uploadimage(logo);
    print("Logo uploaded...")

    qrfile = qr.createQR(SITE_CODE.format(subdomain, codice), QRSIZE, logo, color)
    qrimg = Image.open(qrfile)

    im.paste(qrimg, (W-(QRSIZE+QRPAD), H-(QRSIZE+QRPAD)))

    centerText(draw, codice.upper(), height_1, font_bigger, color, W - (QRSIZE + QRPAD), 0)

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

    packprint.packprint("output/triangoli.pdf", ["output/triangoli/"+n+".png" for n in nomi])
    packprint.packprint("output/orizzontali.pdf", ["output/orizzontali/"+n+".png" for n in nomi])

    print("PDF generated in output/")

def main():
    if(len(sys.argv) < 3):
        print("usage: ./fisso_oneqr.py json_file logo nomi(json) [traduzioni(json)]")
        sys.exit(1)

    logo = sys.argv[2]

    with open(sys.argv[1], "r") as f:
        jj = json.loads(f.read())

    with open(sys.argv[3], "r") as f:
        nomi = json.loads(f.read())

    if(len(sys.argv) > 4):
        langs = json.loads(sys.argv[4])
    else:
        langs = ["it", "en", "de"]

    color = tuple(int(a, 16) for a in wrap(jj['color'], 2))

    print("Eseguo 'sudo service tor start', inserisci la password se richiesto")
    if "MANJARO" in platform.release():
        os.system('sudo systemctl start tor')
    else:
        os.system('sudo service tor start')
    time.sleep(2)

    createImages(jj['subdomain'], jj['codice'], nomi, logo, langs, color)

    print("immagini create in output/")

if __name__ == "__main__":
    main()
