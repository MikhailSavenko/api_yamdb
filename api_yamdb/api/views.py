from api.filters import TitleFilter
from api.permissions import AdminOnlyPermission, IsAdminOrReadOnly
from api.serializers import (CategorieSerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleGetSerializer, TitleSerializer,
                             UserMeSerializer, UserSerializer,
                             UserSignUpSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categorie, Genre, Review, Title
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        title = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, title_id=title, id=review_id)
        serializer.save(review=review, author=self.request.user)


class CategorieViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """Получаем/создаем/удаляем категорию."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewset(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Получаем/создаем/удаляем жанр."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем произведение."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (Title.objects.prefetch_related('reviews').all().
                        annotate(rating=Avg('reviews__score')).
                        order_by('name'))
            return queryset
        return Title.objects.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup_view(request):
    """Регистрация пользователя"""
    username = request.data.get('username')
    email = request.data.get('email')

    user = User.objects.filter(email=email, username=username).first()
    if user is not None:
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(email=email, confirmation_code=confirmation_code)
        return Response({'Оповещение': 'Письмо с кодом отправлено на маил'}, status=status.HTTP_200_OK)
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
        
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
        
    user = User.objects.create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_confirmation_code(email=email, confirmation_code=confirmation_code)
        
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """User GRUD"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [AdminOnlyPermission]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'post', 'patch', 'delete']


class UserMeView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """Получаем и изменяем данные своей учетки на me/"""
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user

    def get(self, request):
        user = self.get_object()
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainJWTView(APIView):
    """Отправляет JWT токен в ответ на ПОСТ запрос с кодом"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response({'error': 'Заполните все обязательные строки'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=username)
        confirmation_code_chek = default_token_generator.check_token(user, token=confirmation_code)
        if confirmation_code_chek == False:
            return Response({'error': 'Неправильный логин или код доступа'})
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


def send_confirmation_code(email, confirmation_code):
    """Отправляем email сообщение пользователю с его кодом"""
    subject = 'Код подтверждения'
    message = f'Код подтверждения для регистрации: {confirmation_code}'
    from_email = 'sredawork26@gmail.com'
    recipient_list = [email]
    fail_silently = True

    send_mail(subject, message, from_email, recipient_list, fail_silently)


