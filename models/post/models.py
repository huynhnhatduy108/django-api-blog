from django.db import models
from models.category.models import Category
from models.tag.models import Tag
# from models.post.category.models import Category
# from models.post.tag.models import Tag
from models.user.models import User

# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    parent = models.ForeignKey("self", db_column='parent_id', on_delete=models.PROTECT, blank=True, null=True)
    slug = models.CharField(db_column='slug', blank=True, null=True, max_length=50)
    title = models.CharField(db_column='title', blank=True, null=True, max_length=100)
    meta_title = models.CharField(db_column='meta_title', blank=True, null=True, max_length=100)
    content = models.TextField(db_column='content', blank=True, null=True)
    summary = models.TextField(db_column='summary', blank=True, null=True)
    author =  models.ForeignKey(User, db_column='user_id', on_delete=models.PROTECT, blank=True, null=True, related_name="author_post")
    published_at = models.DateTimeField(db_column='published_at', blank=True, null=True)
    thumbnail = models.CharField(db_column='thumbnail', blank=True, null=True, max_length=500)

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class PostTag(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    post =  models.ForeignKey(Post, db_column='post_id', on_delete=models.PROTECT, blank=True, null=True, related_name="post_tag")
    tag =  models.ForeignKey(Tag, db_column='tag_id', on_delete=models.PROTECT, blank=True, null=True, related_name="tag_post")

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class PostMeta(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    post =  models.ForeignKey(Post, db_column='post_id', on_delete=models.PROTECT, blank=True, null=True, related_name="post_meta")
    content = models.TextField(db_column='content', blank=True, null=True)
    key = models.CharField(db_column='meta_title', blank=True, null=True, max_length=100)

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class PostComment(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    title = models.CharField(db_column='title', blank=True, null=True, max_length=75)
    parent = models.ForeignKey("self", db_column='parent_id', on_delete=models.PROTECT, blank=True, null=True)
    post =  models.ForeignKey(Post, db_column='post_id', on_delete=models.PROTECT, blank=True, null=True, related_name="post_coment")
    content =   models.TextField(db_column='content', blank=True, null=True)
    author =  models.ForeignKey(User, db_column='user_id', on_delete=models.PROTECT, blank=True, null=True, related_name="author_coment")

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name
    
class PostCategory(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    post =  models.ForeignKey(Post, db_column='post_id', on_delete=models.PROTECT, blank=True, null=True, related_name="post_category")
    category =  models.ForeignKey(Category, db_column='category_id', on_delete=models.PROTECT, blank=True, null=True, related_name="post_category")

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name