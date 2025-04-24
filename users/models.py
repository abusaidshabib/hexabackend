from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from users.managers import UserManager
from users.validators import validate_phone_number


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(
        max_length=15, blank=True, validators=[validate_phone_number])
    store_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_shopkeeper = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        upload_to='profile_photos/%Y/%m/%d/', blank=True, null=True)

    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female')], default='Male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'







