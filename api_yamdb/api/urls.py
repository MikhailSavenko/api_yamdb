from django.urls import include, path
from users.views import CustomObtainJWTView, UserViewSet, UserMeView, user_signup_view
from rest_framework.routers import DefaultRouter
from api.views import CategorieViewSet, GenreViewset, TitleViewSet


app_name = 'api'
VERSION = 'v1'

router = DefaultRouter()
router.register('categories', CategorieViewSet, basename='categories')
router.register('genres', GenreViewset, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(f'{VERSION}/', include((router.urls))),
    path('users/me/', UserMeView.as_view(), name='users-me'),
    path('auth/token/', CustomObtainJWTView.as_view(), name='token'),
    path('auth/signup/', user_signup_view, name='signup'),
]

