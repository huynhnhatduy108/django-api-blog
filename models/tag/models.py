from django.db import models

# Create your models here.
class Tag(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    title = models.CharField(db_column='title', blank=True, null=True, max_length=255)
    slug = models.CharField(db_column='slug', blank=True, null=True, max_length=255)
    meta_title = models.CharField(db_column='meta_title', blank=True, null=True, max_length=255)
    description = models.TextField(db_column='description', blank=True, null=True)

    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)