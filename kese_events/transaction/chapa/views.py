from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.conf import settings
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.apps import apps
import json
from django.views import View
from django.http import HttpResponseBadRequest
from transaction.chapa.api import ChapaAPI
from transaction.chapa.models import ChapaTransaction


@csrf_exempt
class ChapaWebhookView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {
                    'error': "Invalid Json Body"
                },
                status=400
            )

        model_class = apps.get_model(settings.CHAPA_TRANSACTION_MODEL)
        try:
            transaction_instance = model_class.objects.get(id=data.get('trx_ref'))
            transaction_instance.status = data.get('status')
            transaction_instance.response_dump = data
            transaction_instance.save()
            return JsonResponse(data)
        except model_class.DoesNotExist:
            return JsonResponse(
                {
                    'error': "Invalid Transaction"
                },
                status=400
            )

# @csrf_exempt
class InitiatePaymentView(View):
    
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
            # print(data)
            # Save the transaction details to your database
            transaction = ChapaTransaction(
                amount=data['amount'],
                currency=data['currency'],
                email=data['email'],
                phone_number=data['phone_number'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                tax_ref=data['tax_ref']   
            )
            try:
                transaction.save()
            except Exception as e:
                print(f"Error saving transaction: {str(e)}")
            
                
            # Initiate the payment through Chapa API
            try:
                chapa_response = ChapaAPI.send_request(transaction)
                print(chapa_response)
            except Exception as e:
                print({str(e)})

            data = JsonResponse(chapa_response)
            return data

        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': "Invalid Json Body"}, status=400)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
        
    


# @csrf_exempt
class VerifyPaymentView(View):
    
    @csrf_exempt
    def get(self, transaction_id):
        print("............................")
        print(transaction_id)
        try:
            # Get the ChapaTransaction instance by transaction_id
            transaction = ChapaTransaction.objects.get(id=transaction_id)
            
            # Send a verification request to Chapa API
            # verification_response = ChapaAPI.verify_payment(transaction)
            verification_response = ChapaAPI.verify_payment(transaction.tax_ref)

            # Return the verification response as JSON
            return JsonResponse({'verification_response': verification_response})

        except ChapaTransaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')