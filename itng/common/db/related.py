
import django
from django.db.models.fields import related
from django.utils.functional import cached_property
from ..utils import override_attr


def create_many_related_manager(superclass, rel):
    opts = rel.through._meta

    class ManyRelatedManager(superclass):
        def add(self, *objs):
            with override_attr(opts, 'auto_created', True):
                super(ManyRelatedManager, self).add(*objs)
        add.alters_data = True

        def remove(self, *objs):
            with override_attr(opts, 'auto_created', True):
                super(ManyRelatedManager, self).remove(*objs)
        remove.alters_data = True

        def create(self, **kwargs):
            with override_attr(opts, 'auto_created', True):
                super(ManyRelatedManager, self).create(**kwargs)
        create.alters_data = True

    return ManyRelatedManager


# Overrides the auto_created of to-many related object descriptors, enabling
# the add, remove, etc... methods for use with custom 'through' models. This
# is ONLY valid when through instances can be created automatically. This
# is related to ticket #9475, and should be deprecated when it is resolved.
#
# For reference:
# - https://code.djangoproject.com/ticket/9475
# - https://groups.google.com/forum/#!topic/django-developers/uWe31AjzZX0
class ManyRelatedObjectsDescriptor(related.ManyRelatedObjectsDescriptor):

    @cached_property
    def related_manager_cls(self):
        return create_many_related_manager(
            super(ManyRelatedObjectsDescriptor, self).related_manager_cls,
            self.related.field.rel,
        )

    def __set__(self, instance, value):
        opts = self.related.field.rel.through._meta

        with override_attr(opts, 'auto_created', True):
            super(ManyRelatedObjectsDescriptor, self).__set__(instance, value)


class ReverseManyRelatedObjectsDescriptor(related.ReverseManyRelatedObjectsDescriptor):

    @cached_property
    def related_manager_cls(self):
        return create_many_related_manager(
            super(ReverseManyRelatedObjectsDescriptor, self).related_manager_cls,
            self.field.rel,
        )

    def __set__(self, instance, value):
        opts = self.field.rel.through._meta

        with override_attr(opts, 'auto_created', True):
            super(ReverseManyRelatedObjectsDescriptor, self).__set__(instance, value)


class ManyThroughManyField(related.ManyToManyField):

    def __init__(self, *args, **kwargs):
        if django.VERSION >= (1, 9):
            raise Exception("Nooop. Ensure compatibility w/ Django 1.9 before proceeding.")

        super(ManyThroughManyField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super(ManyThroughManyField, self).contribute_to_class(cls, name, **kwargs)

        setattr(cls, self.name, ReverseManyRelatedObjectsDescriptor(self))

    def contribute_to_related_class(self, cls, related):
        super(ManyThroughManyField, self).contribute_to_related_class(cls, related)

        if not self.rel.is_hidden() and not related.related_model._meta.swapped:
            setattr(cls, related.get_accessor_name(), ManyRelatedObjectsDescriptor(related))
