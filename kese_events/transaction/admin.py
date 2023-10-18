from django.contrib import admin
from transaction.models import TicketTransaction
from transaction.chapa.models import ChapaTransaction

# Register your models here.
admin.site.register(ChapaTransaction)
admin.site.register(TicketTransaction)