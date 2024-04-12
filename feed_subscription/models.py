from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):
    USER = 1
    MICROSERVICEUSER = 2
    TYPE_CHOICES = (
        (USER, 'User'),
        (MICROSERVICEUSER, 'Microserviceuser')
    )
    id = models.PositiveIntegerField(choices=TYPE_CHOICES, primary_key=True)
    
    def __str__(self):
        return self.get_id_display()

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("username is required")
        # email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.Model):
        NUSER = 1
        MICROUSER = 2
        TYPE_CHOICES = (
            (NUSER, 'Nuser'),
            (MICROUSER, 'Microuser')
        )
        id = models.PositiveIntegerField(choices=TYPE_CHOICES, primary_key=True)
    
        def __str__(self):
            return self.get_id_display()
        # ADMIN = "ADMIN", 'Admin'
        # NUSER = "NUSER", 'Nuser'
        # MICROUSER = "MICROUSER", 'Microuser'
    
    # base_role = Role.NUSER
    role = models.PositiveIntegerField(Role, choices=Role.TYPE_CHOICES)
    
    # role = models.CharField(max_length=50, choices=Role.choices)
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #         return super().save(*args, **kwargs)



class NuserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.NUSER)

class Nuser(User):
    base_role = User.Role.NUSER
    
    nuser = NuserManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "Only for Normal Users"

@receiver(post_save, sender=Nuser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "NUSER":
        NuserProfile.objects.create(user=instance)

class NuserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuser_id = models.IntegerField(null=True, blank=True)

class MicrouserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.MICROUSER)

class Microuser(User):
    base_role = User.Role.MICROUSER
    
    microuser = MicrouserManager()
    
    class Meta:
        proxy = True
    
    def welcome(self):
        return "Only for Microservice Users"

class MicrouserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    microuser_id = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=Microuser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "MICROUSER":
        MicrouserProfile.objects.create(user=instance)

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    gc_name = models.CharField(max_length=200)