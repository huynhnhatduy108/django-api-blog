from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

PARAMETER_SEARCH_POST_BY_CATEGORY = [
    OpenApiParameter(name="limit", type=OpenApiTypes.STR, description="Giới hạn `số dòng`"),
    OpenApiParameter(name="page", type=OpenApiTypes.STR, description="Giới hạn `số trang`")
]