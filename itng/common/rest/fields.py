
import base64
import re
import shortuuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import ImageField, ValidationError
from rest_framework.renderers import HTMLFormRenderer


DATATYPE_REGEX = re.compile('[:;//]')


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        # base64 image urls looks something like: data:image/png;base64,R0lGODlhPQBEAPe....
        # We can split on the first comma to separate type information from the image data.
        data_type, data = data.split(',', 1)
        ext = DATATYPE_REGEX.split(data_type)[2]
        data = ContentFile(base64.b64decode(data), name='{}.{}'.format(str(shortuuid.uuid()), ext))
        data = super(Base64ImageField, self).to_internal_value(data)
        self.validate_upload_size(data)
        return data

    def validate_upload_size(self, value):
        # It's recommended that nginx have a client_max_body_size greater than
        # the combined size of image uploads in a single request. eg, a request
        # could potentially upload multiple images at the same time.
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 2)
        max_size_bytes = max_size * 1000**2

        if value.size > max_size_bytes:
            raise ValidationError(_("The file you uploaded is larger than {max_size}MB, "
                                    "the maximum file upload size")
                                    .format(max_size=max_size))


HTMLFormRenderer.default_style[Base64ImageField] = {
    'base_template': 'input.html',
    'input_type': 'text'
}
