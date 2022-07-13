from api.v1.post import views
from django.urls import path
from config.contanst import ADMIN_ROLE, POST, USER_ROLE 

urlpatterns = [
    path('list', views.PostView.as_view({'get': 'get_list_post'}), name="get_list_post"),
    path('list_by_author/<int:author_id>', views.PostView.as_view({'get': 'get_list_post_by_author'}), name="get_list_post_by_author"),
    path('list_by_tag/<int:tag_id>', views.PostView.as_view({'get': 'get_list_post_by_tag'}), name="get_list_post_by_tag"),
    path('list_by_category/<int:category_id>', views.PostView.as_view({'get': 'get_list_post_by_category'}), name="get_list_post_by_category"),
    path('search_post_by_keyword/<str:keyword>', views.PostView.as_view({'get': 'search_post_by_keyword'}), name="search_post_by_keyword"),
    # path('search_post', views.PostView.as_view({'get': 'search_post'}), name="search_post"),

    path('info_by_id/<int:pk>', views.PostView.as_view({'get': 'get_info_by_id'}), name="info_by_id"),
    path('info_by_slug/<str:slug>', views.PostView.as_view({'get': 'get_info_by_slug'}), name="info_by_slug"),

    path('create', views.PostAuthenticationView.as_view({'post': 'create_post'}),name="create_post" ),
    path('update/<int:pk>', views.PostAuthenticationView.as_view({'put': 'update_post'}),kwargs={"ROLE": [ADMIN_ROLE, USER_ROLE], "TYPE_API":POST},name="update_post"),
    path('delete/<int:pk>', views.PostAuthenticationView.as_view({'delete': 'delete_post'}),kwargs={"ROLE": [ADMIN_ROLE, USER_ROLE], "TYPE_API":POST},name="delete_post"),

]