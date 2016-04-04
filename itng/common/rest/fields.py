import base64, re, uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        data_type, data = data.split(',', 1)
        ext = re.split('[:;//]', data_type)[2]
        data = ContentFile(base64.b64decode(data), name='{}.{}'.format(str(uuid.uuid4()), ext))
        return super(Base64ImageField, self).to_internal_value(data)
