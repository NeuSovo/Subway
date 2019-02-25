from os.path import basename
import qrcode
import base64
import pyDes
import zipfile

from django.contrib.auth.models import AnonymousUser
from django.utils.six import BytesIO, StringIO

k = pyDes.des(b"DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)


def gen_qrcode(data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()

    return image_stream


def en_password(passwd):
    return str(base64.b64encode(k.encrypt(passwd)), 'utf-8')


def de_password(salt):
    return str(k.decrypt(base64.b64decode(salt)), 'utf-8')


def en_base64(txt):
    tmp = base64.b64encode(str(txt).encode('utf-8'))
    return str(tmp, 'utf-8')


def de_base64(txt):
    uid = base64.b64decode(txt.encode('utf-8'))
    uid = str(uid, 'utf-8')

    return uid


def data_to_obj(to_class, data):
    parms = {}
    for i in data:
        if hasattr(to_class, i):
            parms[i] = data.get(i)
    return to_class(**parms)


def permission(request):
    user = request.user
    res = dict()
    if isinstance(user, AnonymousUser):
        return res
    permissions = user.roles.all().values('permissions__code').distinct()
    for item in permissions:
        res[item['permissions__code']] = True
    print(res)
    return res


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1] # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
     raise ValidationError(u'不支持此类型的文件')


def compress_file(files):
    mm = BytesIO()
    with zipfile.ZipFile(mm, 'w') as z:
        for i in files:
            z.write(i, basename(i))
    return mm
