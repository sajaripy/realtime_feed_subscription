from rest_framework.routers import DefaultRouter
from .views import UserSignupView, LoginAPI, SubscribeChannel, Test
from django.urls import path, include

# router = DefaultRouter()
# router.register(r'subscriptions', UserSubscriptionViewSet)

# urlpatterns = router.urls

from django.urls import path
from . import views

app_name = 'feed_subscription'
router = DefaultRouter()
router.register('ws/binance', Test, basename="index")

urlpatterns = router.urls

urlpatterns = [
    path('register/', UserSignupView.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('subscribe/', SubscribeChannel.as_view(), name='subscribe'),

    # path('subscriptions/', UserSubscriptionViewSet.as_view({'get':'list'}), name='subscriptions'),
    # path('', home, name='home'),
    # path("signup/", authView, name='authView'),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path('subscribe', SubscribeChannel.as_view(), name='subscribe'),
]