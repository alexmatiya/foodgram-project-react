from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """
    Пагинатор с определением атрибута
    `page_size_query_param`, для вывода запрошенного количества страниц.
    """
    page_size_query_param = "limit"
    page_size = 10
    # max_page_size = 50
