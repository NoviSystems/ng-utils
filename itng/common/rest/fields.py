import base64, re, uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        data_type, data = data.split(',', 1)
        ext = re.split('[:;//]', data_type)[2]
        data = ContentFile(base64.b64decode(data), name='{}.{}'.format(str(uuid.uuid4()), ext))
        data = super(Base64ImageField, self).to_internal_value(data)
        self.validate_upload_size(data)
        return data

    def validate_upload_size(self, value):
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError('The file you uploaded is larger than 2MB, the maximum file upload size')
