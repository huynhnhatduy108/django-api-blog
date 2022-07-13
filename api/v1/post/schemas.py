from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PARAMETER_SEARCH_POST = [
    OpenApiParameter(name="detail", type=OpenApiTypes.STR, description="Detail tags and categories of post"),
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