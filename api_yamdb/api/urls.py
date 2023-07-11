from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategorieViewSet, GenreViewset, TitleViewSet

app_name = 'api'
VERSION = 'v1'

router_1 = DefaultRouter()
router_1.register('categories', CategorieViewSet, basename='categories')
router_1.register('genres', GenreViewset, basename='genres')
router_1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path(f'{VERSION}/', include((router_1.urls))),
]
