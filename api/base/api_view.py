from api.base.response import CustomAPIException
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.core.paginator import Paginator, EmptyPage
from rest_framework import exceptions, status

class CustomAPIView(GenericViewSet):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.is_paging = False
        self.total_page = None
        self.total_record = None
        self.limit = 10
        self.page = 1
        self.order_by = 'id'
        self.paging_list = None

    def initial(self, request, *args, **kwargs):
        limit = self.request.query_params.get('limit', None)
        if limit and limit.isdigit():
            self.limit = int(limit)

        page = self.request.query_params.get('page', None)
        if page and page.isdigit():
            self.page = int(page)

        order_by = self.request.query_params.get('order_by', None)
        if type(order_by) is list:
            order_by = ",".join(map(str, self.order_by))
        if order_by and isinstance(order_by, str):
            self.order_by = order_by

    
    def paginate(self, query_set):
        is_order = getattr(query_set, 'ordered', None)
        if not is_order:
            query_set = query_set.order_by(self.order_by)

        paginator = Paginator(query_set, per_page=self.limit)

        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except EmptyPage:
            self.paging_list = []


    def response_paging(self, data, custom_fields=None):
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        paging_data = {
            "items": data,
            "total_page": self.total_page,
            "total_record": len(data) if not self.is_paging and isinstance(data, list) else self.total_record,
            "limit": self.limit,
            "page": self.page,
        }
        if custom_fields:
            paging_data.update(custom_fields)

        return paging_data

    def http_response(self, data = None, mess ="", status_code=status.HTTP_400_BAD_REQUEST):
        pass

    def http_exception(self, error = None, mess ="", status_code=status.HTTP_400_BAD_REQUEST):
        raise CustomAPIException( error, mess, status_code)