from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария', max_length=255)