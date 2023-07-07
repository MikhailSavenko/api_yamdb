from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import ReviewSerializer
from reviews.models import Title
from .pagination import ReviewsPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""
    serializer_class = ReviewSerializer
    permission_classes = IsAuthenticatedOrReadOnly
    pagination_class= ReviewsPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)