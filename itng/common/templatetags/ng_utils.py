
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


@register.simple_tag(takes_context=True)
def isactive(context, url, active, inactive=''):
    """
    A ternary tag for whether the URL is 'active'. An active URL is defined as matching
    the start of the current request URL. For example, if `url` is '/some/path' and the
    current request URL is '/some/path/some/subpath', then `active`s contents would be
    rendered.

    Example::

        {% url 'named-url' as named_url %}
        <div class="{% is_active named_url 'active' 'inactive' %}">
        </div>

    """
    if context['request'].path_info.startswith(url):
        return active
    return inactive
