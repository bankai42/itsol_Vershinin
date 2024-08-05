from django.db import models

# Create your models here.

class VideoRequest(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')