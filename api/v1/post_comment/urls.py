from django.urls import path
from . import views

urlpatterns = [
    path('list_comment_by_post/<int:post_id>', views.CommentView.as_view({'get': 'list_comment_by_post'}), name="list_comment_by_post"),
    path('comment_to_post/<int:post_id>', views.CommentAuthenticationView.as_view({'post': 'comment_to_post'}), name="comment_to_post"),
    path('delete_comment/<int:comment_id>', views.CommentAuthenticationView.as_view({'delete': 'delete_comment'}), name="delete_comment"),

]