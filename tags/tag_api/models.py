from django.db import models
from django import forms
from django.core.exceptions import ValidationError
import uuid
from django.http import JsonResponse


class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    # is_admin = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'user'
        verbose_name = 'user'


class TagsModel(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    tag_name  = models.CharField('tag_name',max_length=255, blank=True, null=True)
    scope  = models.CharField('scope',max_length=255, blank=True, null=True)
    user_id = models.ForeignKey(UserProfile, to_field='user_id', on_delete=models.CASCADE, db_column='user_id')
    
    class Meta:
        managed = True
        unique_together = (('tag_name', 'scope'),)
        db_table = 'tags'
        verbose_name = 'tags'

    def save(self, *args, **kwargs):

        # Set tag_name to None if it is an empty string
        self.tag_name = None if self.tag_name == '' else self.tag_name
        
        # Set scope to None if it is an empty string
        self.scope = None if self.scope == '' else self.scope

        # If scope is null, remove it from uniqueness check
        if TagsModel.objects.filter(tag_name=self.tag_name, scope=self.scope).exists():
            raise ValidationError("This tag already exists.")
        
        super().save(*args, **kwargs)

class VM(models.Model):
    vm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    vm_name = models.CharField('vm_name', max_length=255, unique=True)
    creation_date = models.DateTimeField('creation_date', auto_now_add=True)
    tags = models.ManyToManyField('TagsModel', related_name='vms')

    class Meta:
        managed = True
        db_table = 'vms'
        verbose_name = 'vms'

