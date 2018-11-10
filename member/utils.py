import qrcode
import base64
from django.utils.six import BytesIO


def gen_qrcode(data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()

    return image_stream


def en_base64(txt):
    tmp = base64.b64encode(str(txt).encode('utf-8'))
    return str(tmp, 'utf-8')


def de_base64(txt):
    uid = base64.b64decode(txt.encode('utf-8'))
    uid = str(uid, 'utf-8')

    return uid