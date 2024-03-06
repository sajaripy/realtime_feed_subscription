from django.shortcuts import render

# Create your views here.
# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import throttle_classes, api_view, renderer_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import viewsets
from .models import UserSubscription
from .serializers import UserSubscriptionSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# from .services import start_binance_websocket

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

class SubscribeChannel(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request):
        # Assuming you expect JSON data with subscription information in the request body
        # channel_id = request.data.get('channel_id')
        user = request.user  # Assuming you have user authentication enabled

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        subscription = UserSubscription(user=user)
        subscription.save()
        return render(request, 'subscribe.html', {})
