from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom UserManger
class UserManager(BaseUserManager):
    def create_user(self, email, title, first_name, last_name, gender, password=None):
        """
        Creates and saves a User with the given email, title, first_name, last_name gender.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not title:
          raise ValueError('Users must have an title')

        if not first_name:
          raise ValueError('Users must have an first_name')

        if not last_name:
          raise ValueError('Users must have an last_name')
        
        
        user = self.model(
            email=self.normalize_email(email),
            title= title,
            first_name = first_name,
            last_name = last_name,
            gender = gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, title, first_name, last_name, gender, password=None):
        """
        Creates and saves a superuser with the given email, title, first_name, last_name, gender.
        """
        user = self.create_user(
            email,
            password=password,
            title= title,
            first_name = first_name,
            last_name = last_name,
            gender = gender
        )
        user.is_admin = True
        user.save(using=self._db)

        return user

# Custom UserModel
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    title = models.CharField(max_length=5)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title', 'first_name', 'last_name', 'gender']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin