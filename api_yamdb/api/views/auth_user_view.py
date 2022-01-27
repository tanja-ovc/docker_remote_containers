import random
import string

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminPermissions, SelfOrAdmin
from api.serializers import (CompareConfirmationCodesSerializer,
                             CustomUserSerializer,
                             SendConfirmationCodeSerializer)
from api_yamdb.settings import PROJECT_SETTINGS
from users.models import CustomUser


def generate_confirmation_code():
    chars = string.digits + string.ascii_letters
    return ''.join(random.sample(chars, 20))


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if username == 'me':
        return Response(
            'Пользователя с таким именем создать нельзя',
            status=status.HTTP_400_BAD_REQUEST
        )
    if (
            CustomUser.objects.filter(
                Q(email=email) | Q(username=username)
            )
    ):
        return Response(
            'Такой email уже зарегистрирован',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = generate_confirmation_code()
    CustomUser.objects.update_or_create(
        defaults={
            'confirmation_code': make_password(
                confirmation_code,
                salt=None,
                hasher='argon2'
            )
        },
        email=email,
        username=username,
    )
    subject = 'Your confirmation code for YaMDb'
    message = f'Код подтверждения {confirmation_code}'
    send_mail(subject, message, PROJECT_SETTINGS['support_email'], [email])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def compare_confirmation_code(request):
    serializer = CompareConfirmationCodesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(CustomUser, username=username)
    if check_password(confirmation_code, user.confirmation_code):
        return Response({'token': f'{AccessToken.for_user(user)}'})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminPermissions,)
    lookup_field = 'username'
    filter_backends = (filters.OrderingFilter,)
    ordering = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(SelfOrAdmin,)
    )
    def me(self, request):
        if request.method == 'GET':
            if request.user.is_authenticated:
                serializer = CustomUserSerializer(request.user)
                return Response(serializer.data)
            return Response(
                'Для просмотра нужно авторизоваться',
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.method == 'PATCH':
            if request.user.is_authenticated:
                serializer = CustomUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.validated_data.pop('role', None)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                'Для изменения необходимо авторизоваться',
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                'Такой тип запроса недопустим',
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
