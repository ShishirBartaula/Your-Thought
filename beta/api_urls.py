from django.urls import path, include
from rest_framework.routers import DefaultRouter
#Instead of manually writing paths for "get list", "get one", "create", "update", etc., the router does it all.
from .views import TweetViewSet


router = DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='tweet')
# take the TweetViewSet and create all necessary URLs for it starting with tweets 
urlpatterns=[
    path('', include(router.urls)),
]