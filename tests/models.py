
from django.db import models
from itng.common.db import ManyThroughManyField


class Through(models.Model):
    a = models.ForeignKey('A')
    b = models.ForeignKey('B')


class A(models.Model):
    pass


class B(models.Model):
    a_set = ManyThroughManyField(A, through=Through)
