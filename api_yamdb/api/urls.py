from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet

router = SimpleRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename= 'reviews_list')
urlpatterns = [
    path('', include(router.urls)),
]