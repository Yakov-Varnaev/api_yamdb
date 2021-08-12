import uuid
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserModelSerializer, SignUpSerializer, CodeSerializer
from .permissions import IsSelf

User = get_user_model()


class UserModelViewset(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=('get', 'patch'),detail=True, url_name='me', permission_classes=[permissions.IsAdminUser, IsSelf])
    def user_own_profile(self, request):
        user = request.user
        serializer = UserModelSerializer(user).data
        return Response(data=serializer)


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
                'Account verification',
                f'Your activation key {confirmation_code}',
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
    """
    Code validation class. Checks valid code and email address.
    Will give you a token if the form is valid.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = CodeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.data['email'],
                confirmation_code=serializer.data['confirmation_code']
            )
        except exceptions.ValidationError:
            return Response(
                data={'detail': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh_token.access_token)
            })