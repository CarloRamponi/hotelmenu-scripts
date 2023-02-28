import os
import tempfile
import qrcode
from PIL import Image

def createQR(url, size, color):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")
    img = img.resize((size, size), Image.ANTIALIAS)

    return img
