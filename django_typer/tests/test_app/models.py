from django.db import models
from uuid import uuid1


class ShellCompleteTester(models.Model):

    char_field = models.CharField(max_length=15, db_index=True, default='')
    text_field = models.TextField(default='')
    float_field = models.FloatField(db_index=True, default=None, null=True)
    decimal_field = models.DecimalField(db_index=True, default=None, null=True, max_digits=10, decimal_places=2)
    uuid_field = models.UUIDField(default=uuid1, unique=True)
