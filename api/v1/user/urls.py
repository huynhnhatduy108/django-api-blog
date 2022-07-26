from django.urls import path

from . import views

urlpatterns = [
    path('list', views.UserAuthenticationView.as_view({'get': 'get_list_user'}), name="get_list_user"),
    path('info/<int:pk>', views.UserAuthenticationView.as_view({'get': 'get_info'}), name="get_info"),
    path('create', views.UserAuthenticationView.as_view({'post': 'create_user'}),name="create_car" ),
    path('update/<int:pk>', views.UserAuthenticationView.as_view({'put': 'update_user'}),name="update_user"),
    path('delete/<int:pk>', views.UserAuthenticationView.as_view({'delete': 'delete_user'}),name="delete_user"),
    path('update_avatar/<int:pk>', views.UserAuthenticationView.as_view({'put': 'update_avatar_user'}),name="update_avatar_user"),

]