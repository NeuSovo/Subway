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
    return str(base64.urlsafe_b64encode(k.encrypt(passwd)), 'utf-8')


def de_password(salt):
    return str(k.decrypt(base64.urlsafe_b64decode(salt)), 'utf-8')


def en_base64(txt):
    tmp = base64.urlsafe_b64encode(str(txt).encode('utf-8'))
    return str(tmp, 'utf-8')


def de_base64(txt):
    uid = base64.urlsafe_b64decode(txt.encode('utf-8'))
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



try:
    from django.db.models.fields.related import SingleRelatedObjectDescriptor
except ImportError:
    from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor as SingleRelatedObjectDescriptor
from django.db.models import OneToOneField
from django.db.transaction import atomic


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    """
    The descriptor that handles the object creation for an AutoOneToOneField.
    """

    @atomic
    def __get__(self, instance, instance_type=None):
        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return (
                super(AutoSingleRelatedObjectDescriptor, self)
                .__get__(instance, instance_type)
            )
        except model.DoesNotExist:
            # Using get_or_create instead() of save() or create() as it better handles race conditions
            model.objects.get_or_create(**{self.related.field.name: instance})

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return (
                super(AutoSingleRelatedObjectDescriptor, self)
                .__get__(instance, instance_type)
            )


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField creates related object on first call if it doesnt exist yet.
    Use it instead of original OneToOne field.

    example:

        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255, blank=True)
            icq = models.IntegerField(max_length=255, null=True)
    '''

    def contribute_to_related_class(self, cls, related):
        setattr(
            cls,
            related.get_accessor_name(),
            AutoSingleRelatedObjectDescriptor(related)
        )
