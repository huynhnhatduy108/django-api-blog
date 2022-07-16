
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PARAMETER_SEARCH_USER = [
    OpenApiParameter(name="keyword", type=OpenApiTypes.STR, description="File by title, Description"),
    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]