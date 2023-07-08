import random
import string
from api.serializers import UsersSerializer
from users.models import Users
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class UsersSignUpViewSet(viewsets.ModelViewSet):
    """Регистрация пользователя"""
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # permissions_classes = (AllowAny,)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        # генерирую код
        confirmation_code = generate_confirmation_code()
        user = Users.objects.create_user(email=email, username=username, confirmation_code=confirmation_code)
        user.save()
        # отправляем код подтверждения. Нужно настроить нормально сервер
        # почтовый! Для реальной отправки. 
        send_confirmation_code(email, confirmation_code)


class UsersViewSet(viewsets.ModelViewSet):
    """Users GRUD"""
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # pagination_class = UsersCustomPagination
    # permissions_classes = (IsAdminUser, IsAuthentificatedOrReadOnly)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirmation_code = generate_confirmation_code()
        serializer.save(confirmation_code=confirmation_code)
        # отправляем в ответ на POST запрос код в API
        return Response({'confirmation_code': confirmation_code})


class CustomObtainJWTView(APIView):
    """Отправляет JWT токен в ответ на ПОСТ запрос с кодом"""
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response({'error': 'Заполните все обязательные строки'})

        try:
            user = Users.objects.get(username=username, confirmation_code=confirmation_code)
        except Users.DoesNotExist:
            return Response({'error': 'Неправильный логин или код доступа'})

        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)})


def generate_confirmation_code():
    """Генерирует код для отправки пользователю на email"""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return code


def send_confirmation_code(email, confirmation_code):
    """Отправляем email сообщение пользователю с его кодом"""
    subject = 'Код подтверждения'
    message = f'Код подтверждения для регистрации: {confirmation_code}'
    from_email = 'sredawork26@gmail.com'
    recipient_list = [email]
    fail_silently = True

    send_mail(subject, message, from_email, recipient_list, fail_silently)
