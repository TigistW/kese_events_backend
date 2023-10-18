from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class UserProfileManager(BaseUserManager):
    """
    Defines user creation fields and manages to save user
    """
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_organizeruser(self, email, password=None):
        user = self.create_user(email,
                password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        
        return user
    
    
class UserProfile(AbstractBaseUser):
    
    """
    Creates a customized database table for user using customized user manager
    """
    email = models.EmailField(
             max_length=255,unique=True,
             )
    first_name = models.CharField(
              max_length=150,
    )
    last_name = models.CharField(
              max_length=150,    
    )
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
     
    USERNAME_FIELD = 'email'
     
    objects = UserProfileManager()
     
    def get_full_name(self):
        return self.first_name +  self.last_name
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    
class UserAddress(models.Model):
    user = models.OneToOneField('UserProfile', on_delete=models.DO_NOTHING, related_name='address')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}"
    
class OTP(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)