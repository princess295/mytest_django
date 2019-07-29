from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from PIL import Image


app = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@app.task()
def resize_image(file_image, height_im, width_im):
    original_image = Image.open(file_image)
    new_size = (int(width_im), int(height_im))
    original_image.thumbnail(new_size, Image.ANTIALIAS)

    original_image.save('output_image.jpg', 'JPEG')

    original_image.close()
