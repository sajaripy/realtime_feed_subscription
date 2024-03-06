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
        # Handle POST request to subscribe to channels
        # Your subscription logic goes here
        return Response({"message": "Subscription successful"}, status=status.HTTP_200_OK)

# Define an API view for receiving feed updates
class FeedUpdates(APIView):
    def post(self, request):
        # Handle POST request to receive feed updates
        # Your feed update logic goes here
        return Response({"message": "Feed update received"}, status=status.HTTP_200_OK)