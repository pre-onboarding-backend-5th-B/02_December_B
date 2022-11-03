from django.urls import path, include
from rest_framework import routers

from transfer.views import TransferViewSet

router = routers.DefaultRouter()
router.register('', TransferViewSet)

urlpatterns = [
    path('', include(router.urls), name='transfer')
]
