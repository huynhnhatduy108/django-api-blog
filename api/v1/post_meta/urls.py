from django.urls import path

from . import views

urlpatterns = [
    path('list', views.PostMetaView.as_view({'get': 'get_list_postmeta'}), name="get_list_postmeta"),
    path('info/<int:pk>', views.PostMetaView.as_view({'get': 'get_info'}), name="get_info"),
    path('create', views.PostMetaView.as_view({'post': 'create_postmeta'}),name="create_car" ),
    path('update/<int:pk>', views.PostMetaView.as_view({'put': 'update_postmeta'}),name="update_postmeta"),
    path('delete/<int:pk>', views.PostMetaView.as_view({'delete': 'delete_postmeta'}),name="delete_postmeta"),
]