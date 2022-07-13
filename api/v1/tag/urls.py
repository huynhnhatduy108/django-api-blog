from django.urls import path
from . import views

urlpatterns = [
    path('list', views.TagView.as_view({'get': 'get_list_tag'}), name="get_list_tag"),
    path('info/<int:pk>', views.TagView.as_view({'get': 'get_info'}), name="get_info"),
    path('create', views.TagView.as_view({'post': 'create_tag'}),name="create_car" ),
    path('update/<int:pk>', views.TagAuthenticationView.as_view({'put': 'update_tag'}),name="update_tag"),
    path('delete/<int:pk>', views.TagAuthenticationView.as_view({'delete': 'delete_tag'}),name="delete_tag"),
]