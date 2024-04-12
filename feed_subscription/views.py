from django.shortcuts import render

# Create your views here.
# Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import throttle_classes, api_view, renderer_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import viewsets
from .models import UserSubscription, User
from .serializers import UserSubscriptionSerializer, UserLoginSerializer, UserSignupSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
# from .services import start_binance_websocket

# @login_required
# def home(request):
#     return render(request, 'home.html', {})

# def authView(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/accounts/login")
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

class UserSignupView(APIView):
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({'message': 'Registered Successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class LoginAPI(APIView):

    def post(self, request):
        # serializer = UserLoginSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        username = request.data.get("username")
        password = request.data.get("password")
            # username = serializer.data.get("username")
            # password = serializer.data.get("password")
        user = authenticate(username=username, password=password)
        if username and password:
            # user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                # user.last_login = timezone.now().astimezone(timezone.get_current_timezone())
                user.save()
                token = get_token_for_user(user)
                return Response({ "message": "Logged in successfully!","token": token}, status=status.HTTP_200_OK)
        return Response({"message": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

class SubscribeChannel(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.data.get("username")
        user = User.objects.get(username=username)
        # user = request.user
        try:
            gc_name = request.data.get('gc_name')
            if UserSubscription.objects.filter(gc_name=gc_name,user=user).exists():
                return Response({'msg': f'You have already subscribed to {gc_name} group'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSubscriptionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({'msg': f'You have successfully subscribed to {gc_name} group'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        # Assuming you expect JSON data with subscription information in the request body
        # channel_id = request.data.get('channel_id')
        # user = request.user  # Assuming you have user authentication enabled
        username = request.data.get("username")
        user = User.objects.get(username=username)
        serializer = UserSubscriptionSerializer(data=request.data)
        # Check if the user is authenticated
        if serializer.is_valid():
            if user.role == 1:
                subscription = UserSubscription(user=user)
                subscription.save()
                return redirect('routing.py')
        
            elif user.role == 2:
                subscription = UserSubscription(user=user)
                subscription.save()
                return Response({"message":"subscribed"}, status=status.HTTP_200_OK)
                # return render(request, '../static/index.html', {})
                # return redirect('../ws/chat/')
                # return Response({"message":"subscribed"}, status=status.HTTP_200_OK)
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

class Test(viewsets.ModelViewSet):
    pass