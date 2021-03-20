from django.urls import path, include
from rest_framework import routers
from .views import CourierViewSet

router = routers.DefaultRouter()
router.register('couriers', CourierViewSet)

urlpatterns = router.urls
