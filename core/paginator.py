from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'limit'
    max_page_size = 100000

class NakedPagination(DefaultResultsSetPagination):
    page_size = 15

    def get_paginated_response(self, data):
        return Response(data)
