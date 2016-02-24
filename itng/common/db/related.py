
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
class ManyToManyDescriptor(related.ManyToManyDescriptor):

    @cached_property
    def related_manager_cls(self):
        return create_many_related_manager(
            super(ManyToManyDescriptor, self).related_manager_cls,
            self.rel,
        )

    def __set__(self, instance, value):
        opts = self.through._meta

        with override_attr(opts, 'auto_created', True):
            super(ManyToManyDescriptor, self).__set__(instance, value)


class ManyThroughManyField(related.ManyToManyField):

    def contribute_to_class(self, cls, name, **kwargs):
        super(ManyThroughManyField, self).contribute_to_class(cls, name, **kwargs)

        setattr(cls, self.name, ManyToManyDescriptor(self.remote_field, reverse=False))

    def contribute_to_related_class(self, cls, related):
        super(ManyThroughManyField, self).contribute_to_related_class(cls, related)

        if not self.rel.is_hidden() and not related.related_model._meta.swapped:
            setattr(cls, related.get_accessor_name(), ManyToManyDescriptor(self.remote_field, reverse=True))
