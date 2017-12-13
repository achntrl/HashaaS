from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from haas.serializers import UserSerializer, GroupSerializer, StatisticsSerializer
from haas.hashers import DummyHasher, Md5Hasher, Sha1Hasher, Sha256Hasher
from haas.models import Statistics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserRegister(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


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


class HashView(APIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def post(self, request, *args, **kw):
        data = request.data.get('data', None)  # TODO: Add validation on input length
        iterations = request.data.get('iterations', None)
        algorithm = request.data.get('algorithm', None)

        if (data is None or iterations is None or algorithm is None):
            return Response(
                'Bad request, POST data should be {"data": "seald is awesome", "algorithm": "md5", "iterations": 1}',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            int(iterations)
        except:
            return Response(
                '"iterations" should be an integer',
                status=status.HTTP_400_BAD_REQUEST
            )

        if algorithm.lower() == 'md5':
            hasher = Md5Hasher(data, int(iterations))
        elif algorithm.lower() == 'sha1':
            hasher = Sha1Hasher(data, int(iterations))
        elif algorithm.lower() == 'sha256':
            hasher = Sha256Hasher(data, int(iterations))
        else:
            return Response(
                '"algorithm" should be md5, sha1 or sha256',
                status=status.HTTP_400_BAD_REQUEST
            )

        statistics = Statistics(user=request.user, algorithm=algorithm, data=data, iterations=iterations)
        statistics.save()

        return Response({'hash': hasher.hash()})


class StatisticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format='json'):
        statistics = request.user.statistics_set.all()
        serializer = StatisticsSerializer(statistics, many=True, context={'request': request})

        return Response(serializer.data)
