from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.BigAutoField(db_column="id",primary_key=True) 
    email = models.CharField(db_column='email', blank=True, null=True, max_length=255)
    full_name = models.CharField(db_column='full_name', blank=True, null=True, max_length=255)
    subject = models.CharField(db_column='subject', blank=True, null=True, max_length=255)
    messgae = models.CharField(db_column='messgae', blank=True, null=True, max_length=500)
    
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True, blank=True, null=True)
    hide_flag = models.IntegerField(db_column='hide_flag', blank=True, null=True, default=0)
    deleted_flag = models.IntegerField(db_column='deleted_flag', blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)