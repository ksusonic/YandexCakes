from rest_framework import viewsets
from .models import Courier
from .serializers import CourierSerializer


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
