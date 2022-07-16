from django.urls import path

from . import views

urlpatterns = [
    path('list', views.CategoryView.as_view({'get': 'get_list_category'}), name="get_list_category"),
    path('search', views.CategoryView.as_view({'get': 'search_list_category'}),name="search_list_category"),
    path('info/<int:pk>', views.CategoryAuthenticationView.as_view({'get': 'get_info'}), name="get_info"),
    path('create', views.CategoryAuthenticationView.as_view({'post': 'create_category'}),name="create_category" ),
    path('update/<int:pk>', views.CategoryAuthenticationView.as_view({'put': 'update_category'}),name="update_category"),
    path('delete/<int:pk>', views.CategoryAuthenticationView.as_view({'delete': 'delete_category'}),name="delete_category"),
]