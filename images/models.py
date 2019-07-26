from django.db import models
from .tasks import resize_image

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    height_im = models.CharField(max_length=4)
    width_im = models.CharField(max_length=4)
    request_id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.file.name

class Task(models.Model):
    status = models.CharField(max_length=255)
    id_image = models.CharField(max_length=255)
    def __str__(self):
        return self.status


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        resize_image.delay(instance.pk)

