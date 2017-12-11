from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from haas.serializers import UserSerializer, GroupSerializer
from haas.hashers import DummyHasher


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DummyHashView(APIView):
    def get(self, request, *args, **kw):
        dummy_hasher = DummyHasher()

        return Response({'hash': dummy_hasher.hash()})
