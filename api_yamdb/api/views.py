import random
import string

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import viewsets, filters, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from reviews.models import Categories, Genres, Title
from .filters import TitleFilters
from .permissions import IsAdminOrReadOnly
from .serializers import (
    SendTokenSerializer,
    GetGWTSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    TitleCRUDSerializer
)


EMAIL_SENDER = 'admin <admin@yamdb.ru>'
RANDOM_STRING_LENGTH = 20


@api_view(['POST'])
def send_token(request):
    """
    Sends a confirmation code to the specified email address.

    If the email address is not associated, a new user is created.
    The confirmation code is stored in the user's confirmation_token field.

    :param request: The HTTP request containing the email address.
    :return: A HTTP response indicating whether the code was sent successfully.
    """
    serializer = SendTokenSerializer(data=request.data)
    email = request.data.get('email', False)
    username = request.data.get('username', False)

    if serializer.is_valid():
        random_string = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits, k=RANDOM_STRING_LENGTH
            )
        )
        user = User.objects.filter(email=email).first()
        if not user:
            User.objects.create_user(
                email=email,
                username=username)
        User.objects.filter(email=email).update(
            confirmation_token=random_string
        )
        mail_subject = 'Код подтверждения на YAMDB'
        message = f'Ваш код подтверждения: {random_string}'
        send_mail(mail_subject, message, EMAIL_SENDER, [email])
        return Response(
            f'Код отправлен на адрес {email}', status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt(request):
    serializer = GetGWTSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_token = serializer.validated_data['confirmation_token']
        user = get_object_or_404(User, username=username)
        if user.confirmation_token != confirmation_token:
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()  # сюда можно добавить аннотейт для рейтинга
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCRUDSerializer
        return TitleSerializer
