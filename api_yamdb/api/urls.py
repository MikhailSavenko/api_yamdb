from django.urls import include, path
from .views import CustomObtainJWTView, UserViewSet, UserMeView, user_signup_view
from rest_framework.routers import DefaultRouter
from api.views import CategorieViewSet, GenreViewset, TitleViewSet
from .views import CommentViewSet, ReviewViewSet


app_name = 'api'
VERSION = 'v1'

router = DefaultRouter()
router.register('categories', CategorieViewSet, basename='categories')
router.register('genres', GenreViewset, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comment')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='titles')

urlpatterns = [
    path(f'{VERSION}/', include(router.urls)),
    path('users/me/', UserMeView.as_view(), name='users-me'),
    path('auth/token/', CustomObtainJWTView.as_view(), name='token'),
    path('auth/signup/', user_signup_view, name='signup'),
]


