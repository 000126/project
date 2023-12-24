from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy
from django.contrib.auth.hashers import check_password, make_password
import uuid
from django.core.validators import FileExtensionValidator

ext_validator = FileExtensionValidator(['pptx', 'xlsx', 'docx'])


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,)
    username = None
    email = models.EmailField(('email address'), unique=True)
    password_reset_token = models.CharField(
        max_length=100, blank=True, null=True)
    email_otp = models.CharField(max_length=6, blank=True)
    mobile_no = models.CharField(max_length=6, blank=True)
    mobile_otp = models.CharField(max_length=6, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class file(models.Model):
    name = models.CharField(max_length=100)
    upload_file = models.FileField(
        upload_to="media/", validators=[ext_validator])

    def __str__(self):
        return self.name
