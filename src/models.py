from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL
from django.db.models.fields import BooleanField, CharField, DateTimeCheckMixin
from core.settings import STATIC_ROOT
from django.core.files.storage import default_storage
import os 
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    def create_user(self, Username, password, Name):
        if not Username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        
        user = self.model(
            Username=Username,
            Name=Name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, password, Name):
        user = self.create_user(
            Username=Username,
            password=password,
            Name=Name
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    Key = models.CharField(max_length=100, blank=True, null=True)
    DateCreated = models.DateTimeField(auto_now_add=True, null=True)
    AccType = models.CharField(max_length=50, blank=True, null=True)
    Username = models.CharField(max_length=100, unique=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    ProfilePic = models.ImageField(default='add-image.gif', null=True, blank=True)
    
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    is_active = models.BooleanField(default=False)
    RawPassword = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = ['Name',]

    objects = MyAccountManager()

    def parameter(self):
        return ["Name","Username","Password","DateCreated","Active Status"]
    
    def list(self):
        return [self.Name,self.Username,self.RawPassword,self.DateCreated,self.is_active]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Admin(Account):
    pass

class Client(Account):
    Email = models.EmailField(unique=True, null=True, blank=True)
    DateRegister = models.DateTimeField(default=timezone.now)
    Address = models.CharField(max_length=200, null=True, blank=True)
    PhoneNum = models.CharField(max_length=13, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    
class TaskFile(models.Model):
    Created = models.DateTimeField(auto_now_add=True)
    Taskfile = models.FileField(null=True, blank=True, upload_to='documents/')
    
class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    duedate = models.DateTimeField(null=True, blank=True)
    lastchange = models.DateTimeField(auto_now=True)
    photo = models.ManyToManyField(TaskFile, related_name="photo", blank=True)
    document = models.ManyToManyField(TaskFile, related_name="document", blank=True)
    complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['complete', 'duedate', '-created']
        
    def __str__(self):
        return self.title

# NO FKING TOUCH =====================================================================================

class UploadedFile(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(Account, on_delete=models.CASCADE)
    FileName = models.CharField(max_length=255)
    SavedFileName = models.CharField(max_length=255)
    File = models.FileField(upload_to='temp/')

    def __str__(self):
        return self.FileName

class SavedFile(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True)
    File = models.FileField(upload_to='saved_file/')

# This signal is to make sure the UploadedFile delete, the file is deleted as well
@receiver(pre_delete, sender=UploadedFile)
@receiver(pre_delete, sender=SavedFile)
def uploaded_file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.File and default_storage.exists(instance.File.name):
        default_storage.delete(instance.File.name)

class UserActivity(models.Model):
    DateCreated = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(Account, on_delete=models.CASCADE)
    Activity = models.CharField(max_length=500)
    Link = models.CharField(max_length=500, blank=True, null=True) # Store "/<url>/<pk> (if any)/"

