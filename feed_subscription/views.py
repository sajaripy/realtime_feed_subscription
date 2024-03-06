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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSubscription

class SubscribeChannel(APIView):
    def get(self, request):
        # Assuming you expect JSON data with subscription information in the request body
        # channel_id = request.data.get('channel_id')
        user = request.user  # Assuming you have user authentication enabled

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        subscription = UserSubscription(user=user)
        subscription.save()
        return Response({"message": f"Subscribed to channel successfully"}, status=status.HTTP_200_OK)

        # Validate the channel_id and perform subscription logic
        # if channel_id:
        #     # Check if the user is already subscribed to the channel
        #     if UserSubscription.objects.filter(user=user, channel_id=channel_id).exists():
        #         return Response({"error": "User is already subscribed to this channel"}, status=status.HTTP_400_BAD_REQUEST)

        #     # Create a new UserSubscription instance and save it to the database
        #     subscription = UserSubscription(user=user, channel_id=channel_id)
        #     subscription.save()

        #     return Response({"message": f"Subscribed to channel {channel_id} successfully"}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"error": "Invalid channel_id provided"}, status=status.HTTP_400_BAD_REQUEST)



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