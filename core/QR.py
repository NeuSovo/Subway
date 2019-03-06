# -*- coding: utf-8 -*-

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.utils.six import BytesIO, StringIO

static_root =  settings.STATIC_ROOT
# static_root = 'D:\\Code\\Python\\django\\Subway\\static\\'
static_ttf = os.path.join(static_root, 'FZXBSJW.TTF')
QRcode_f_url = os.getenv('HOSTNAME') or 'http://127.0.0.1:8000'

backMode_2 = {
    "back_url": os.path.join(static_root, "qr.png"),
    "size": (1440, 1440),
    "QR": {
        "frame": (620, 620),
        "position": (700, 450),
    },
    "text": [{
        "size": 60,
        "ttf": static_ttf,
        "color": "#000000",
        "position": [200, 580],
        "frame": (600, 20),
    }, {
        "size": 60,
        "ttf": static_ttf,
        "color": "#000000",
        "position": [200, 820],
        "frame": (600, 20),
    }],
}

backMode_3 = {
    "back_url": os.path.join(static_root, "qr.png"),
    "size": (1440, 1440),
    "QR": {
        "frame": (620, 620),
        "position": (700, 450),
    },
    "text": [{
        "size": 60,
        "ttf": static_ttf,
        "color": "#000000",
        "position": [200, 560],
        "frame": (600, 20),
    }, {
        "size": 60,
        "ttf": static_ttf,
        "color": "#000000",
        "position": [200, 720],
        "frame": (600, 20),
    }, {
        "size": 60,
        "ttf": static_ttf,
        "color": "#000000",
        "position": [200, 870],
        "frame": (600, 20),
    }],
}


def make_QR(content, sizeW=0, sizeH=0):  # 创建二维码
    qr = qrcode.QRCode(version=3, box_size=3, border=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    if sizeW == 0 and sizeH == 0:
        return img
    w, h = img.size
    if sizeW < w or sizeH < h:
        return None
    img = img.resize((sizeW, sizeH), Image.ANTIALIAS)
    return img


def com_pic(topimg, backimg, position):  # 合并图片
    nodeA = position
    w, h = topimg.size
    nodeB = (position[0]+w, position[1]+h)
    backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
    return backimg


def write_line(backimg, text, tmode):  # 给单个文本框填充数据
    myfont = ImageFont.truetype(tmode["ttf"], size=tmode["size"])
    draw = ImageDraw.Draw(backimg)
    tend = len(text)
    while True:
        text_size = draw.textsize(text[:tend], font=myfont)  # 文本图层的尺寸
        if text_size[0] <= tmode["frame"][0]:
            break
        else:
            tend -= 1
    draw.text(((700 - text_size[0]) / 2, tmode["position"][1]),
              text[:tend], font=myfont, fill=tmode['color'])
    if tend != len(text):
        text2_size = draw.textsize(text[tend:], font=myfont)
        draw.text(((700 - text2_size[0]) / 2, tmode["position"][1] + text_size[1]),
                  text[tend:], font=myfont, fill=tmode['color'])
    return backimg, tend


def write_text(img, tlist, tmodeList):  # 写文本
    mnum = 0
    flag = False
    draw = ImageDraw.Draw(img)
    for t in tlist:
        tbegin = 0
        if flag:
            tmodeList[mnum]['position'][1] += 50
        img, tend = write_line(img, t, tmodeList[mnum])
        mnum += 1
        flag = (tend != len(t))
    return img


def make_pic(text, data):
    mode = backMode_2 if len(text) == 2 else backMode_3
    img = Image.open(mode["back_url"])  # 读取背景图片
    QR_res = make_QR(QRcode_f_url + data, mode["QR"]["frame"][0],
                     mode["QR"]["frame"][1])  # 创建二维码
    img = com_pic(QR_res, img, mode["QR"]["position"])  # 合成1
    img = write_text(img, text, mode["text"])  # 写文本
    # img.save('A.PNG', quality=100)
    return img


# make_pic(["技术信息", "变电所预埋件安装作业指导书"], "QRcode data").save('test.png')
