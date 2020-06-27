#!/usr/bin/python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image, ImageDraw
import os
import sys

def drawBorders(image):
    thickness = 2
    im = Image.new("RGBA", (image.size[0]+thickness, image.size[1]+thickness), (255, 255, 255))
    im.paste(image, (thickness, thickness))
    dr = ImageDraw.Draw(im)
    dr.rectangle([(0, 0), (im.size[0]-thickness, im.size[1]-thickness)], outline=(189, 189, 189))
    return im

def packprint(outdir, files):

    PAGESIZE = (A4[0]*4, A4[1]*4)
    padding = (30*mm, 60*mm)

    canvas = Canvas(os.path.join(outdir, "output.pdf"), pagesize=PAGESIZE)

    for j, i in enumerate(range(0, len(files), 4)):

        curfiles = [f for f in files[i:i+4]]

        for idx, f in enumerate(curfiles):

            im = Image.open(f)
            im = drawBorders(im)

            if idx == 0:
                canvas.drawInlineImage(im, padding[0], PAGESIZE[1]-padding[1]-im.size[1], width=im.size[0], height=im.size[1])
            elif idx == 1:
                canvas.drawInlineImage(im, padding[0], padding[1], width=im.size[0], height=im.size[1])
            elif idx == 2:
                canvas.drawInlineImage(im, PAGESIZE[0]-padding[0]-im.size[0], PAGESIZE[1]-padding[1]-im.size[1], width=im.size[0], height=im.size[1])
            else:
                canvas.drawInlineImage(im, PAGESIZE[0]-padding[0]-im.size[0], padding[1], width=im.size[0], height=im.size[1])

        canvas.showPage()
    canvas.save()

def main():
    if(len(sys.argv) < 2):
        print("usage: ./hotelmenu.py directory")
        sys.exit(1)

    dir = sys.argv[1]
    files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    packprint(dir, files)

if __name__ == "__main__":
    main()
