from api.serializers import UserSerializer, UserSignUpSerializer
from users.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.tokens import default_token_generator  
from rest_framework import status
from django.core.mail import send_mail


class UserSignUpViewSet(viewsets.ModelViewSet):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        if User.objects.filter(username=request.POST.get('username')).exists():
            return Response('Пользователь уже существует', status=status.HTTP_200_OK)
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(email=user.email, confirmation_code=confirmation_code)
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(email=email, confirmation_code=confirmation_code)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    """User GRUD"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    # permission_classes = (IsAdminUser,)


class CustomObtainJWTView(APIView):
    """Отправляет JWT токен в ответ на ПОСТ запрос с кодом"""
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response({'error': 'Заполните все обязательные строки'})

        try:
            user = User.objects.get(username=username, confirmation_code=confirmation_code)
        except User.DoesNotExist:
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
