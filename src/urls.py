from django.urls import path
from django.conf.urls import include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from config.root_local import REDOC_SUB_ENDPOINT, SWAGGER_SUB_ENDPOINT

urlpatterns = [
    path('api/post/', include('api.v1.post.urls')),
    path('api/tag/', include('api.v1.tag.urls')),
    path('api/category/', include('api.v1.category.urls')),
    path('api/comment/', include('api.v1.post_comment.urls')),
    path('api/user/', include('api.v1.user.urls')),
    path('api/post_meta/', include('api.v1.post_meta.urls')),
    path('api/common/', include('api.v1.common.urls')),

]

api_url_v1_patterns = [
    path('api/post/', include('api.v1.post.urls')),
    path('api/tag/', include('api.v1.tag.urls')),
    path('api/category/', include('api.v1.category.urls')),
    path('api/comment/', include('api.v1.post_comment.urls')),
    path('api/user/', include('api.v1.user.urls')),
    path('api/post_meta/', include('api.v1.post_meta.urls')),
    path('api/common/', include('api.v1.common.urls')),

]

urlpatterns += [

    path('v1/schema/', SpectacularAPIView.as_view(urlconf=api_url_v1_patterns, api_version='v1'), name="schema_v1"),
    path('v1/' + SWAGGER_SUB_ENDPOINT, SpectacularSwaggerView.as_view(url_name="schema_v1"), name='swagger_v1'),
    path('v1/' + REDOC_SUB_ENDPOINT, SpectacularRedocView.as_view(url_name="schema_v1"), name='redoc_v1')
]
