from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
  GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
  )
  default_img_path = "media/utility_images/default.png"
  uploaded_img_path = "media/profile_images/"

  # model fields
  profile_img = models.ImageField(upload_to=uploaded_img_path, default=default_img_path)
  gender = models.CharField(max_length=7, choices=GENDER_CHOICES)

  def __str__(self):
    return self.username


