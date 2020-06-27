import requests
import json
import shutil
import uuid
import os
import tempfile

proxies = {
  "http": "socks5://127.0.0.1:9050",
  "https": "socks5://127.0.0.1:9050",
}

def uploadimage(image):
    with open(image, 'rb') as f:
        r = requests.post('https://qr-generator.qrcode.studio/qr/uploadimage', files = { 'file' : f }, proxies=proxies)
    file = r.json()['file']
    del r
    return file

def createQR(url, size, image, color):

    c_str = "#"
    for c in color:
        c_str += hex(c)[2:]

    r = requests.post('https://qr-generator.qrcode.studio/qr/custom', json = {
        "data" : url,
        "config" : {
            "body" : "square",
            "eye" : "frame0",
            "eyeBall" : "ball0",
            "erf1" : [],
            "erf2" : [],
            "erf3" : [],
            "brf1" : [],
            "brf2" : [],
            "brf3" : [],
            "bodyColor" : c_str,
            "bgColor" : "#FFFFFF",
            "eye1Color" : c_str,
            "eye2Color" : c_str,
            "eye3Color" : c_str,
            "eyeBall1Color" : c_str,
            "eyeBall2Color" : c_str,
            "eyeBall3Color" : c_str,
            "gradientColor1" : "",
            "gradientColor2" : "",
            "gradientType" : "linear",
            "gradientOnEyes" : "true",
            "logo" : image,
            "logoMode" : "clean"
        },
        "size" : size,
        "download" : "imageUrl",
        "file" : "png"
    }, proxies=proxies)

    img = "https:" + r.json()['imageUrl']
    del r

    file = tempfile.NamedTemporaryFile(suffix='.png', prefix='qr_', delete=False)

    r = requests.get(img, stream=True)
    shutil.copyfileobj(r.raw, file)
    del r

    return file.name
