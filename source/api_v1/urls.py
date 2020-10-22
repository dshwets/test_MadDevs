from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import CommitsHistoryViewSet

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'commits', CommitsHistoryViewSet, basename='commits')

urlpatterns = [
    path('', include(router.urls))
]