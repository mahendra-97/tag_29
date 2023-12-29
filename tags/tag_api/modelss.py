from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.http import JsonResponse

class UserProfile(models.Model):
    """
    Model representing user profiles.

    Attributes:
    - user_id: Primary key for the user.
    - user_name: Name of the user.
    """
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'user'
        verbose_name = 'user'


class TagsModel(models.Model):
    """
    Model representing tags.

    Attributes:
    - tag_id: Primary key for the tag.
    - tag_name: Name of the tag.
    - scope: Scope of the tag.
    - user_id: Foreign key to the UserProfile model.

    Unique Constraint:
    - tag_name and scope combination must be unique.
    """
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    tag_name  = models.CharField('tag_name', max_length=255, blank=True, null=True)
    scope  = models.CharField('scope', max_length=255, blank=True, null=True)
    user_id = models.ForeignKey(UserProfile, to_field='user_id', on_delete=models.CASCADE, db_column='user_id')
    
    class Meta:
        managed = True
        unique_together = (('tag_name', 'scope'),)
        db_table = 'tags'
        verbose_name = 'tags'

    def save(self, *args, **kwargs):
        """
        Custom save method for TagsModel.

        """
        self.tag_name = None if self.tag_name == '' else self.tag_name
        self.scope = None if self.scope == '' else self.scope

        if TagsModel.objects.filter(tag_name=self.tag_name, scope=self.scope).exists():
            raise ValidationError("This tag already exists.")
        
        super().save(*args, **kwargs)

class VM(models.Model):
    """
    Model representing virtual machines (VMs).

    Attributes:
    - vm_id: Primary key for the VM.
    - vm_name: Name of the VM.
    - creation_date: Date and time of VM creation.
    - tags: Many-to-many relationship with TagsModel.

    Unique Constraint:
    - vm_name must be unique.
    """
    vm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    vm_name = models.CharField('vm_name', max_length=255, unique=True)
    creation_date = models.DateTimeField('creation_date', auto_now_add=True)
    tags = models.ManyToManyField('TagsModel', related_name='vms')

    class Meta:
        managed = True
        db_table = 'vms'
        verbose_name = 'vms'
