from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PARAMETER_LIST_POST = [
    OpenApiParameter(name="detail", type=OpenApiTypes.STR, description="Detail tags and categories of post"),
    OpenApiParameter(name="is_pagination", type=OpenApiTypes.STR, description="pagination of post"),
    OpenApiParameter(name="keyword", type=OpenApiTypes.STR, description="keyword search of post"),
    OpenApiParameter(name="tags", type={'type': 'array', 'items': {'type': 'number'}}, description="tags search of post"),
    OpenApiParameter(name="categories", type={'type': 'array', 'items': {'type': 'number'}}, description="categories search of post"),
    OpenApiParameter(name="author", type=OpenApiTypes.STR, description="author of post"),

    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]

PARAMETER_SEARCH_POST_BY_AUTHOR = [
    OpenApiParameter(name="detail", type=OpenApiTypes.STR, description="Detail tags and categories of post"),
    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]

PARAMETER_SEARCH_POST_BY_TAG = [
    OpenApiParameter(name="detail", type=OpenApiTypes.STR, description="Detail tags and categories of post"),
    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]

PARAMETER_SEARCH_POST_BY_CATEGORY = [
    OpenApiParameter(name="detail", type=OpenApiTypes.STR, description="Detail tags and categories of post"),
    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]