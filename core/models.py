from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if extra.get("is_staff") is not True or extra.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")
        return self.create_user(email, password, **extra)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True, 
        null=True, 
        db_index=True
        )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
