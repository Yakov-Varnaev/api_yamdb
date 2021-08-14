import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserModelSerializer, SignUpSerializer, CodeSerializer
from .permissions import IsAdmin, OnlyAdminCanChangeRole

User = get_user_model()


class UserModelViewset(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAdminUser | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False, url_path='me', url_name='me',
        permission_classes=[
            permissions.IsAuthenticated,
            OnlyAdminCanChangeRole
        ]
    )
    def user_own_profile(self, request):
        instance = request.user
        serializer = self.get_serializer(instance=instance)
        if self.request.method == 'PATCH':
            print(request.user.role)
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(
                instance=instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            confirmation_code = uuid.uuid4()

            User.objects.create(
                email=email,
                username=username,
                confirmation_code=confirmation_code,
                is_active=False,
            )
            send_mail(
                'Email confirmation',
                f'Your confirmation code: {confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BADREQUEST)


class CodeConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = CodeSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')

            user = get_object_or_404(User, username=username)

            if f'{user.confirmation_code}' != confirmation_code:
                return Response(
                    'Wrong confirmation code!', status.HTTP_400_BAD_REQUEST
                )

            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status.HTTP_200_OK)
        return Response(
            data={'response': 'Something went wrong.'},
            status=status.HTTP_400_BAD_REQUEST
        )
