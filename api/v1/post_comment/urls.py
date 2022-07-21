from django.urls import path
from . import views

urlpatterns = [
    path('list_comment_by_post/<int:post_id>', views.CommentView.as_view({'get': 'list_comment_by_post'}), name="list_comment_by_post"),
    path('user_comment_to_post/<int:post_id>', views.CommentView.as_view({'post': 'user_comment_to_post'}), name="user_comment_to_post"),

    path('admin_comment_reply/<int:post_id>', views.CommentAuthenticationView.as_view({'post': 'admin_comment_reply'}), name="admin_comment_reply"),
    path('delete_comment/<int:post_id>', views.CommentAuthenticationView.as_view({'delete': 'delete_comment'}), name="delete_comment"),

]