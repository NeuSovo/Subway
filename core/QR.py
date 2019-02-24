from PIL import Image, ImageDraw, ImageFont
import qrcode

backMode = {
    "back_url": "qr.png",
    "size": (1440, 1440),
    "QR": {
        "frame": (620, 620),
        "position": (630, 450),
    },
    "text": [{
        "size": 70,
        "ttf": "FZXBSJW.TTF",
        "color": "#000000",
        "position": (200, 620),
        "frame": (300, 20),
    }, {
        "size": 70,
        "ttf": "FZXBSJW.TTF",
        "color": "#000000",
        "position": (200, 820),
        "frame": (300, 20),
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
        # print(text_size)
        if text_size[0] <= tmode["frame"][0]:
            break
        else:
            tend -= 1
    draw.text((tmode["position"][0], tmode["position"][1]),
              text[:tend], font=myfont, fill=tmode['color'])

    return backimg, tend


def write_text(img, text, tmodeList):  # 写文本
    tlist = text.split("\n")
    mnum = 0
    draw = ImageDraw.Draw(img)
    for t in tlist:
        tbegin = 0
        tend = len(t)
        while True:
            img, tend = write_line(img, t[tbegin:tend], tmodeList[mnum])
            mnum += 1
            if tbegin + tend == len(t) or mnum == len(tmodeList):
                break
            else:
                tbegin = tbegin + tend
                tend = len(t)
        if mnum == len(tmodeList):
            break
    return img


def make_pic(mode, text, data):
    img = Image.open(mode["back_url"])  # 读取背景图片
    QR_res = make_QR(data, mode["QR"]["frame"][0],
                     mode["QR"]["frame"][1])  # 创建二维码
    img = com_pic(QR_res, img, mode["QR"]["position"])  # 合成1
    img = write_text(img, text, mode["text"])  # 写文本
    img.save('A.PNG', quality=100)


make_pic(backMode, "晚风窃\n的月色",
         "http://bd.kuwo.cn/yinyue/41230185")
exit()
