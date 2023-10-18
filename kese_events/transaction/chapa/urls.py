from django.urls import path
from .views import ChapaWebhookView, InitiatePaymentView

# urlpatterns = [
#     path('webhook/', ChapaWebhookView.as_view(), name='chapa_webhook'),
#      path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
# ]