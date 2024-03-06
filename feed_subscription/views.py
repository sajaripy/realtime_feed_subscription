from django.shortcuts import render

# Create your views here.
# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import viewsets
from .models import UserSubscription
from .serializers import UserSubscriptionSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .services import start_binance_websocket

@login_required
def home(request):
    return render(request, 'home.html', {})

def authView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/login")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer


# Define an API view for subscribing to channels
class SubscribeChannel(APIView):
    def post(self, request):
        channel_data = start_binance_websocket()
        # Assuming you expect JSON data with channel information in the request body
        # channel_data = request.data.get('channels', [])

        # Your logic to handle subscription to channels
        # You might save the subscribed channels to the database or perform any other actions
        # For demonstration purposes, let's assume you simply return a success message

        # Check if channel_data is not empty
        if channel_data:
            # Process the channels and perform subscription logic here
            # For example, you could save the subscribed channels to the database
            # Or interact with external APIs to manage subscriptions
            # For demonstration, we'll just print the subscribed channels
            print("Subscribed to channels:", channel_data)

            return Response({"message": "Subscribed to channels successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No channels provided for subscription"}, status=status.HTTP_400_BAD_REQUEST)
        # Handle POST request to subscribe to channels
        # Your subscription logic goes here
        # return Response({"message": "Subscription successful"}, status=status.HTTP_200_OK)

# Define an API view for receiving feed updates
class FeedUpdates(APIView):
    def post(self, request):
        # Assuming you expect JSON data with feed update information in the request body
        feed_data = request.data.get('feed_data')

        # Your logic to handle the received feed updates
        # You might process the updates, save them to the database, or perform any other actions
        # For demonstration purposes, let's assume you simply return a success message

        # Check if feed_data is provided
        if feed_data:
            # Process the feed data and perform update logic here
            # For example, you could save the feed updates to the database
            # Or distribute the updates to subscribed users
            # For demonstration, we'll just print the received feed data
            print("Received feed update:", feed_data)

            return Response({"message": "Feed update received successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No feed data provided"}, status=status.HTTP_400_BAD_REQUEST)
        # Handle POST request to receive feed updates
        # Your feed update logic goes here
        # return Response({"message": "Feed update received"}, status=status.HTTP_200_OK)