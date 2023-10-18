from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests
import json
from django.shortcuts import get_object_or_404
from authentication.models import UserProfile

from events.models import Event

class TransactionView(View):

    def post(self, request):
        # print(request.body)
        # Your TicketTransaction logic here
        data = json.loads(request.body)
        event_id = data.get('event_id')
        user_profile_id = data.get('user_profile_id')
        # print(event_id)
        # print(user_profile_id)
        # Retrieve related model instances based on their IDs
        event = Event.objects.get(pk=event_id)
        # print(event.location)
        user_profile = UserProfile.objects.get(pk=user_profile_id)
        
        # print(data)
        
        # Prepare data for the ChapaTransaction request
        chapa_transaction_data = {
            "amount": data['amount'],  # Modify with your data
            "email": user_profile.email,  # Modify with your data
            "phone_number": data['phone_number'], 
            "first_name": user_profile.first_name, 
            "last_name": user_profile.last_name, 
            "payment_title": data['payment_title'], 
            "description": data['description'], 
            "tax_ref": data['tax_ref'],
            "currency":data['currency'],
            # Include other ChapaTransaction fields
        }

        # Send a POST request to the ChapaTransaction view
        chapa_transaction_url = "http://192.168.43.250:8000/transaction/initiate-payment/"  # Modify with your domain
        response = requests.post(chapa_transaction_url, data=json.dumps(chapa_transaction_data), headers={"Content-Type": "application/json"})
        print("response", response.content)
        if response.status_code == 200:
            # Handle a successful response
            chapa_transaction_response = response.json()
            # Process the ChapaTransaction response as needed
            # ...
            return chapa_transaction_response
        else:
            # Handle an error response
            # You may want to return an error response to the front-end
            error_response = {"error": "ChapaTransaction failed"}
            return JsonResponse(error_response, status=400)

        # Continue with your TicketTransaction logic
