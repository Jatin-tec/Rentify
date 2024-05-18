from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_user(self, first_name, phone_number, password, **other_fields):
        if not phone_number:
            raise ValueError(_("You must provide a phone number"))

        if not password:
            raise ValueError(_("You must provide a password"))

        user = self.model(
            first_name=first_name,
            phone_number=phone_number,
            **other_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, phone_number, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_admin", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        superuser = self.create_user(
            first_name=first_name,
            phone_number=phone_number,
            password=password,
            **other_fields,
        )

        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser

class Profile(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100, blank=True, null=True)
    phone_number = models.CharField(_("phone number"), max_length=20, unique=True, null=True)
    email = models.EmailField(_("email address"), max_length=254, primary_key=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    phone_number_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_timestamp = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='profile_users',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='profile_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='profile_users',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='profile_user',
    )
    
    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "phone_number"]

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "User Profiles"
