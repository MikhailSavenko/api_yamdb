from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Avg

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


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем/создаем/удаляем/редактируем произведение."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (Title.objects.prefetch_related('reviews').all().
                        annotate(rating=Avg('reviews__score')).
                        order_by('name'))
            return queryset
        return Title.objects.all()
