import time

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .mixins import RetrieveUpdateListViewSet
from .permissions import ReadOnlyPermission
from .serializers import (UserAuthSerializer, UserLoginSerializer,
                          UserSerializer)
from .utils import generate_invite_code


class UserAuthSignupView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            status_code = status.HTTP_200_OK
            if not User.objects.filter(username=username).exists():
                invite_code = generate_invite_code()
                while User.objects.filter(invite_code=invite_code).exists():
                    invite_code = generate_invite_code()
                serializer.save(invite_code=invite_code)
                status_code = status.HTTP_201_CREATED
            user = User.objects.get(username=username)

            # it is necessary to implement code generation
            # and sending it via SMS in the future
            time.sleep(2)
            user.auth_code = '0000'

            user.save()
            return Response(serializer.data, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            user = get_object_or_404(User, username=username)
            access_token = str(AccessToken.for_user(user))
            return Response({'token': access_token}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(RetrieveUpdateListViewSet):
    queryset = User.objects.select_related('referrer')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [ReadOnlyPermission]

    @action(detail=False, methods=['GET', 'PATCH'], url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me_action(self, request):
        if self.request.method == 'GET':
            instance = self.request.user
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
