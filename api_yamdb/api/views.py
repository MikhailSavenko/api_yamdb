from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title, Review
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment."""
    serializer_class = CommentSerializer
    permission_classes = IsAuthenticatedOrReadOnly

    def perform_create(self, serializer):
        title = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, title_id=title, id=review_id)
        serializer.save(review=review, author=self.request.user)