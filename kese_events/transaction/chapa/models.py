from django.db import models
from uuid import uuid4


class ChapaStatus(models.TextChoices):
    CREATED = 'created', 'CREATED'
    PENDING = 'pending', 'PENDING'
    SUCCESS = 'success', 'SUCCESS'
    FAILED = 'failed', 'FAILED'


class ChapaTransaction(models.Model):
    # transaction = models.OneToOneField('Transaction', on_delete=models.CASCADE, related_name='transaction')

    amount = models.FloatField()
    currency = models.CharField(max_length=25, default='ETB')
    email = models.EmailField()
    phone_number = models.CharField(
              max_length=150,null=True, blank = True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    payment_title = models.CharField(max_length=255, default='Payment')
    description = models.TextField()

    status = models.CharField(max_length=50, choices=ChapaStatus.choices, default=ChapaStatus.CREATED)
    
    response_dump = models.JSONField(default=dict, blank=True)  # incase the response is valuable in the future
    checkout_url = models.URLField(null=True, blank=True)

    tax_ref = models.CharField(max_length=50, default= "AstridFrostIce")
    return_url = models.URLField(null=True, blank=True)
    
