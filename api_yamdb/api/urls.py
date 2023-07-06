from django.urls import include, path
from rest_framework import routers
from users.views import CustomObtainJWTView, UsersSignUpViewSet, UsersViewSet


router = routers.DefaultRouter()
router.register(r'auth/signup', UsersSignUpViewSet, basename='signup')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomObtainJWTView.as_view(), name='token')
]