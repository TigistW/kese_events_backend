from django.db import models
from django.utils import timezone

NULL = {'null': True, 'blank': True}


class BaseMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime, editable=False)
    updated_at = models.DateTimeField(**NULL)
    
    class Meta:
        abstract = True
