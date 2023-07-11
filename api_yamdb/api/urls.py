from django.urls import include, path
from rest_framework import routers
from users.views import CustomObtainJWTView, UserViewSet, UserMeView, user_signup_view


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('users/me/', UserMeView.as_view(), name='users-me'),
    path('', include(router.urls)),
    path('auth/token/', CustomObtainJWTView.as_view(), name='token'),
    path('auth/signup/', user_signup_view, name='signup')
    
]