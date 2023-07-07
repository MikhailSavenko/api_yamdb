from rest_framework.pagination import PageNumberPagination


class ReviewsPagination(PageNumberPagination):
    """Разбивает список элементов на страницы с заданным размером."""

    page_size = 10
