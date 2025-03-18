from rest_framework import generics
from barter.models import Barter
from barter.serializers import BarterSerializer, BarterCreateSerializer
from barter.services import barter_service
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated


class BarterCreateView(generics.ListCreateAPIView):
    queryset = Barter.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BarterCreateSerializer
        return BarterSerializer

    def create(self, request: Request, *args, **kwargs):
        service = barter_service
        status, context = service(request, self.get_serializer_class())
        return Response(status=status, data=context)
