from django.contrib import admin
from django.urls import path, include
from django.urls import path
from transaction.views import TransactionView

from transaction.chapa.views import InitiatePaymentView, VerifyPaymentView

app_name = 'transaction'
urlpatterns = [
    # path('webhook/', ChapaWebhookView.as_view(), name='chapa_webhook'),
     path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
     path('verify-payment/<tax_ref>', VerifyPaymentView.as_view(), name='verify-payment'),
     path('payment/', TransactionView.as_view(), name='payment'),
]

