from rest_framework.routers import DefaultRouter
from .views import UserSubscriptionViewSet, authView, home
from django.urls import path, include

# router = DefaultRouter()
# router.register(r'subscriptions', UserSubscriptionViewSet)

# urlpatterns = router.urls

from django.urls import path
from . import views

app_name = 'feed_subscription'

urlpatterns = [
    path('subscriptions/', UserSubscriptionViewSet.as_view({'get':'list'}), name='subscriptions'),
    path('', home, name='home'),
    path("signup/", authView, name='authView'),
    path("accounts/", include("django.contrib.auth.urls")),
]