from django.db import models

# Create your models here.
class DbFile(models.Model):
	filename = models.CharField(max_length=256)
	data = models.TextField()
	size = models.IntegerField()