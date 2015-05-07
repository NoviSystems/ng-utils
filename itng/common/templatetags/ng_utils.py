
from django import template
from ordered_set import OrderedSet

register = template.Library()


@register.filter
def required(field):
    """
    Return 'required' as a string if the BoundField's underlying field is required.
    """
    return "required" if field.field.required else ""


@register.filter
def add_class(value, css_classes):
    """
    Add a single or multiple css classes to a form widget. To add multiple classes, pass
    them as a whitespace delimited string. eg, {{ field|add_class:"foo bar" }}
    """
    if not css_classes:
        return value

    widget = value.field.widget
    orig_classes = OrderedSet(widget.attrs.get('class', '').split())
    new_classes = OrderedSet(css_classes.split())

    widget.attrs['class'] = " ".join(orig_classes | new_classes)
    return value
