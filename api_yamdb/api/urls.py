from django.urls import include, path
from rest_framework import routers
from users.views import CustomObtainJWTView, UserSignUpViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'auth/signup', UserSignUpViewSet, basename='signup')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomObtainJWTView.as_view(), name='token')
]