from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from PIL import Image
import logging

from .celery_im import app


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)

# app = Celery('images.tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

@app.task()
def resize_image(file_image, height_im, width_im):
    original_image = Image.open(file_image)
    new_size = (int(width_im), int(height_im))
    original_image.thumbnail(new_size, Image.ANTIALIAS)

    original_image.save('output_image.jpg', 'JPEG')

    original_image.close()





# @app.task
# def error_handler(uuid):
#     result = AsyncResult(uuid)
#     exc = result.get(propagate=False)
#     print('Task {0} raised exception: {1!r}\n{2!r}'.format(
#           uuid, exc, result.traceback))
# #     #logger.error('ERROR')
#  def on_raw_message(body):
#      print(body)

# res = resize_image.apply_async(('buff', 100, 100), countdown=3)
# print(res.get(on_message=on_raw_message, propagate=False))
# print(res.ready())



# def get_celery_queue_items(queue_name):
#     import base64
#     import json
#
#     # Get a configured instance of a celery app:
#     from images.celery_im import app as celery_app
#
#     with celery_app.pool.acquire(block=True) as conn:
#         tasks = conn.default_channel.client.lrange(queue_name, 0, -1)
#         decoded_tasks = []
#
#     for task in tasks:
#         j = json.loads(task)
#         body = json.loads(base64.b64decode(j['body']))
#         decoded_tasks.append(body)
#
#     return decoded_tasks
#     print(decoded_tasks)
