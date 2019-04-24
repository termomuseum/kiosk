from django.db import models


class ConfigModel(models.Model):
  conf_name = models.CharField(max_length=30, unique=True)
  conf_text = models.TextField()

  def __str__(self):
    return self.conf_name
