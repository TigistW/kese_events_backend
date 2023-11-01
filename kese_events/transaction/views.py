from io import StringIO
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests
import json
import secrets
import string
from django.shortcuts import get_object_or_404
from authentication.models import UserProfile

from events.models import Event

class TransactionInitiationView(View):
    
    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(characters) for _ in range(length))
        return random_string

    def post(self, request):
        print(request.body)
        # Your TicketTransaction logic here
        data = json.loads(request.body)
        event_id = data.get('event_id')
        user_profile_id = data.get('user_profile_id')
        # print(event_id)
        # print(user_profile_id)
        # Retrieve related model instances based on their IDs
        event = Event.objects.get(pk=event_id)
        print(event.ticket_price)
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        
        tax_ref = self.generate_random_string(8)
        print(tax_ref)
        amount = int(event.ticket_price) * data['quantity']
        
        # Prepare data for the ChapaTransaction request
        chapa_transaction_data = {
            "amount": amount,  # Modify with your data
            "email": user_profile.email,  # Modify with your data
            "phone_number": user_profile.phone_number, 
            "first_name": user_profile.first_name, 
            "last_name": user_profile.last_name, 
            "tax_ref": tax_ref,
            "currency":data['currency'],
            
            # Include other ChapaTransaction fields
        }
        
        print(chapa_transaction_data    )

        # Send a POST request to the ChapaTransaction view
        chapa_transaction_url = "http://192.168.43.250:8000/transaction/initiate-payment/"  # Modify with your domain
        response = requests.post(chapa_transaction_url, data=json.dumps(chapa_transaction_data), headers={"Content-Type": "application/json"})
        print("response", response)
        if response.status_code == 200:
            # Handle a successful response
            chapa_transaction_response = response.json()
            # Process the ChapaTransaction response as needed
            # ...
            print(chapa_transaction_response)
            chapa_initiation_response = {
                "data":chapa_transaction_response,
                "statusCode":201
            }
            return JsonResponse(chapa_initiation_response)
        else:
            # Handle an error response
            # You may want to return an error response to the front-end
            error_response = {"error": "ChapaTransaction failed"}
            return JsonResponse(error_response, status=400)

class TransactionConfirmationView(View):
    pass
    
    
