from django.db import models

# Create your models here.

import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('username is required')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.user_type = 'AD'
        user.save(using=self._db)
        return user


USER_TYPES = [
    ('AD', 'Admin User'),
    # ('NU', 'Nurse User'),
    ('PU', 'Partner User'),
    ('MAU', 'Marketing Admin User'),
    ('MU', 'Marketer User'),
    # ('AU', 'Account User'),
]


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True,unique=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, blank=True, null=True)
    reset_password = models.BooleanField(blank=True, null=True)
    is_loggedin = models.BooleanField(blank=True, null=True)
    login_at = models.DateTimeField(blank=True, null=True)
    branch_code = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey('Role', related_name="user_role", on_delete=models.DO_NOTHING, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'user'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()}"

    def has_role_perm(self, perm):

        if self.is_active and self.is_superuser:
            return True

        if not self.role:
            return False

        if perm:
            try:
                self.role.permissions.get(codename=perm)
                
                return True
            except Permission.DoesNotExist:         
                return False
        else: return False



class Role(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name="role_permissions",
        verbose_name=_('role permissions'),
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="roles", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'role'
        managed = True
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return str(self.description)

    def has_perm(self, perm):
        
        if perm:
            try:
                self.permissions.get(codename=perm)
                
                return True
            except Permission.DoesNotExist:         
                return False
        else: return False
        


REGIONS = [
    ('Ahafo', 'Ahafo'),
    ('Ashanti', 'Ashanti'),
    ('Bono East', 'Bono East'),
    ('Brong Ahafo', 'Brong Ahafo'),
    ('Central', 'Central'),
    ('Eastern', 'Eastern'),
    ('Greater Accra', 'Greater Accra'),
    ('North East', 'North East'),
    ('Northern', 'Northern'),
    ('Oti', 'Oti'),
    ('Savannah', 'Savannah'),
    ('Upper East', 'Upper East'),
    ('Western', 'Western'),
    ('Western North', 'Western North'),
    ('Volta', 'Volta')
]


class Branch(models.Model):
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True, choices=REGIONS)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="branches", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'branch'
        managed = True
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.code
    
