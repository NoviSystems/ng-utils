
from django.test import TestCase

from tests.models import A, B


class ManyThroughManyFieldTestCase(TestCase):

    def test_forward_auto_cretaed_method_access(self):
        """
        Only `auto_created` through models have access to the related manager's
        `set()`, `add()`, and `remove()` methods. Ensure that we circumvent
        those checks.
        """
        a1 = A.objects.create()
        a2 = A.objects.create()
        b = B.objects.create()

        b.a_set.add(a1, a2)

        self.assertQuerysetEqual(b.a_set.order_by('pk'), [a1.pk, a2.pk], lambda p: p.pk)

    def test_reverse_auto_cretaed_method_access(self):
        """
        Only `auto_created` through models have access to the related manager's
        `set()`, `add()`, and `remove()` methods. Ensure that we circumvent
        those checks.
        """
        a = A.objects.create()
        b1 = B.objects.create()
        b2 = B.objects.create()

        a.b_set.add(b1, b2)

        self.assertQuerysetEqual(a.b_set.order_by('pk'), [b1.pk, b2.pk], lambda p: p.pk)
