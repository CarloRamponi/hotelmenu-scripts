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
import threading

def createImages(subdomain, camere, langs, color):

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
    draw_nome = ImageDraw.Draw(im)

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

    def creaCameraImg(camera):
        imc_o = im.copy()
        imc_t = im.copy()
        drawc_o = ImageDraw.Draw(imc_o)
        drawc_t = ImageDraw.Draw(imc_t)

        im_nomec = im_nome.copy()
        draw_nomec = ImageDraw.Draw(im_nomec)

        # mi aspetto di ricevere camere con nomi del tipo: 100, 200, .. oppure 'Tavolo 1', 'Appartamento 1', ...

        if len(camera['nome'].split()) > 1:
            centerTextV(draw_nomec, camera['nome'].split()[0], font_not_really_big, color, H//2, -160)
            centerTextV(draw_nomec, camera['nome'].split()[1], font_really_big, color, H//2, 70)
        else:
            centerTextV(draw_nomec, camera['nome'], font_really_big, color, H//2)

        imc_o.paste(im_nomec)
        imc_t.paste(im_nomec.rotate(180))

        qrimg = qr.createQR(SITE_CODE.format(subdomain, camera['codice']), QRSIZE, color)

        imc_o.paste(qrimg, (W-(QRSIZE+QRPAD), H-(QRSIZE+QRPAD)))
        imc_t.paste(qrimg, (W-(QRSIZE+QRPAD), H-(QRSIZE+QRPAD)))

        centerText(drawc_o, camera['codice'].upper(), height_1, font_bigger, color, W - (QRSIZE + QRPAD), 0)
        centerText(drawc_t, camera['codice'].upper(), height_1, font_bigger, color, W - (QRSIZE + QRPAD), 0)

        imc_o.save('output/orizzontali/'+camera['nome']+'.png', 'PNG', dpi=(300, 300))
        imc_t.save('output/triangoli/'+camera['nome']+'.png', 'PNG', dpi=(300, 300))
        print(camera['nome'], "--> OK")

    for chunk in range(0, len(camere), 15):

        threads = []

        for c in camere[chunk:chunk+15]:
            t = threading.Thread(target=creaCameraImg, args=(c,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    packprint.packprint("output/triangoli.pdf", ["output/triangoli/"+c['nome']+".png" for c in camere])
    packprint.packprint("output/orizzontali.pdf", ["output/orizzontali/"+c['nome']+".png" for c in camere])

    print("PDF generated in output/")

def main():
    if(len(sys.argv) < 2 ):
        print("usage: ./hotelmenu.py json_file [languages (json)]")
        sys.exit(1)

    camere = sys.argv[1]
    if not os.path.exists(camere):
        camere = os.path.join("/app/input/", camere)
        if not os.path.exists(camere):
            print(f"File {sys.argv[1]} not found")
            sys.exit(1)

    with open(camere, "r") as f:
        jj = json.loads(f.read())

    if(len(sys.argv) > 2):
        langs = sys.argv[2]
        if not os.path.exists(langs):
            langs = os.path.join("/app/input/", langs)
            if not os.path.exists(langs):
                print(f"File {sys.argv[2]} not found")
                sys.exit(1)
        langs = json.loads(langs)
    else:
        langs = ["it", "en", "de"]

    color = tuple(int(a, 16) for a in wrap(jj['color'], 2))

    createImages(jj['subdomain'], jj['camere'], langs, color)

    print("immagini create in output/")

if __name__ == "__main__":
    main()

# createImages("demo", [{'nome' : "100", 'codice' : 'ABCD'}, {'nome' : "102", 'codice' : 'GH64'}], ['it', 'en', 'de'], (1, 117, 33))
