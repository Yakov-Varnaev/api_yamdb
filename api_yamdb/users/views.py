import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .serializers import UserModelSerializer, SignUpSerializer, CodeSerializer, FullUserSerializer
from .permissions import IsSelf, IsAdmin

User = get_user_model()


class UserModelViewset(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAdminUser | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


    def get_serializer_class(self):
        if (self.action == ('user_profile', 'user_own_profile')
            or 'search' in self.request.query_params):
            return FullUserSerializer
        return self.serializer_class


    @action(methods=('get', 'patch', 'delete'), url_path=r'^(?P<username>\w+)$',detail=True)
    def user_profile(self, request, username=None):
        user = get_object_or_404(self.queryset, username=username)
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data)


    @action(
        methods=('get', 'patch'),
        detail=True, url_path='me',
        permission_classes=[IsAdmin | IsSelf]
    )
    def user_own_profile(self, request):
        instance = request.user
        serializer = self.get_serializer(instance=instance)
        self.check_object_permissions(request, instance)
        print(request)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=instance.email, role=instance.role)
        return Response(serializer.data)


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
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')

            user = get_object_or_404(User, username=username)

            if user.confirmation_code != confirmation_code:
                return Response('Wrong confirmation code!', status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)

            return Response({'token': token.access_token}, status.HTTP_200_OK)
        return Response(data={'response': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)