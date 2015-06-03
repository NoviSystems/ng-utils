import random

from django.forms import widgets
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from itng.common.utils import ModelChoiceIterator


class TransferSelect(widgets.MultiWidget):
    """ Take two on the select multiple widget.
        This should work with a normal ModelMultipleChoiceField.
    """
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', ())
        self.template_name = kwargs.pop('template_name', 'forms/widgets/transferselect.html')
        self.iterator = kwargs.pop('iterator', ModelChoiceIterator)

        self.ts_id = "%x" % random.randint(0, 16**6)

        kwargs.update({
            'widgets': (
                widgets.SelectMultiple(
                    choices=self.choices,
                    attrs={
                        'data-transfer-bucket': 'available',
                        'data-transfer-id': self.ts_id,
                    },
                ),
                widgets.SelectMultiple(
                    choices=(),
                    attrs={
                        'data-transfer-bucket': 'selected',
                        'data-transfer-id': self.ts_id,
                    },
                ),
            )
        })
        super(TransferSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        # MultiWidget assumes values that are lists are already decompressed.
        # This assumption is incorrect for `MultipleChoiceField`s and bypasses
        # the decompress function.
        value = self.decompress(value)
        return super(TransferSelect, self).render(name, value, attrs)

    def decompress(self, value):
        if value:
            # if we're a queryset iterator
            if hasattr(self.choices, 'queryset'):
                available_queryset = self.choices.queryset.exclude(pk__in=value)
                selected_queryset = self.choices.queryset.filter(pk__in=value)

                self.widgets[0].choices = self.iterator(available_queryset)
                self.widgets[1].choices = self.iterator(selected_queryset)
                return [None, value]

            # else we're a plain list of choice pairs
            else:
                available_choices = list(c for c in self.choices if c[0] not in value)
                selected_choices = list(c for c in self.choices if c[0] in value)

                self.widgets[0].choices = available_choices
                self.widgets[1].choices = selected_choices
                return [None, value]

        self.widgets[0].choices = self.choices
        self.widgets[1].choices = ()
        return [None, None]

    def __get_name(self):
        """ This method uses stack inspection to get the name parameter of
        """
        import inspect

        # current > format_output > render
        render_locals = inspect.currentframe().f_back.f_back.f_locals
        return render_locals['name']

    def format_output(self, rendered_widgets):
        if not self.template_name:
            output = super(TransferSelect, self).format_output(rendered_widgets)
            output += "<br>"
            output += "<button type='button' data-transfer-action='deselect'>&laquo; Deselect</button>"
            output += "<button type='button' data-transfer-action='select'>Select &raquo;</button>"
            return output

        name = self.__get_name()
        params = {
            'available': rendered_widgets[0],
            'selected': rendered_widgets[1],
            'available_id': "id_%s_0" % name,
            'selected_id': "id_%s_1" % name,
            'select_attrs': mark_safe(flatatt({
                'data-transfer-action': 'select',
                'data-transfer-id': self.ts_id,
            })),
            'deselect_attrs': mark_safe(flatatt({
                'data-transfer-action': 'deselect',
                'data-transfer-id': self.ts_id,
            })),
        }
        return render_to_string(self.template_name, params)

    def value_from_datadict(self, data, files, name):
        values = super(TransferSelect, self).value_from_datadict(data, files, name)
        return values[1]

    class Media:
        css = {
            'all': ('common/css/transferselect.css', )
        }
        js = ('common/js/transferselect.js', )
