from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    username = models.CharField(db_column='username', blank=True, null=True, max_length=50)
    full_name = models.CharField(db_column='full_name', blank=True, null=True, max_length=50)
    email = models.CharField(db_column='email', max_length=200, blank=True, null=True)
    address = models.CharField(db_column='address', blank=True, null=True, max_length=200)
    phone = models.CharField(db_column='phone', blank=True, null=True, max_length=50)
    intro = models.TextField(db_column='intro', blank=True, null=True)
    profile = models.TextField(db_column='profile', blank=True, null=True)
    password = models.CharField(db_column='password', blank=True, null=True, max_length=50)
    role = models.IntegerField(db_column='role', blank=True, null=True, default= 0)  #role users
    avatar_url = models.CharField(db_column='avatar_url', blank=True, null=True, max_length=500)
    avatar_provider = models.CharField(db_column='avatar_provider', blank=True, null=True, max_length=500)
    c_provider = models.CharField(db_column='c_provider', blank=True, null=True, max_length=50)
    refresh_token = models.CharField(db_column='refresh_token', blank=True, null=True, max_length=500)
    access_token = models.CharField(db_column='access_token', blank=True, null=True, max_length=500)

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return self.name
    