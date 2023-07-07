from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

app_name = 'api'
VERSION = 'v1'

router_1 = DefaultRouter()
router_1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='titles'
)

urlpatterns = [
    path(f'{VERSION}/', include((router_1.urls))),
]
