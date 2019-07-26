from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from celery.result import AsyncResult


from celery.task.control import inspect

from .serializers import ImageSerializer, TaskSerializer
from .models import Task, File
from .tasks import app, resize_image
from celery import current_app
# import time
# from rq import Queue
# from redis import Redis
#
# redis_conn = Redis()
# queue = Queue(connection=redis_conn)

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CELERY_TRACK_STARTED = True

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        print(request.data)
        context = {}
        file_serializer = ImageSerializer(data=request.data)

        logger.debug('{}, {}, {}'.format(request.method, request.user, request.content_type))

        image = File.objects.all()
        height_im = request.data.get('height_im')
        width_im = request.data.get('width_im')

        print(image, height_im, width_im)
        print(request.FILES.get('file'))
        data = request.FILES.get('file')
        with open('file', 'wb+') as f:
            for chunk in data.chunks():
                f.write(chunk)
        res = resize_image.delay('file', height_im, width_im)
        task_id = res.id
        task_status = res.status
        print(task_status)
        print(task_id)
        ready_res = res.ready()
        print(ready_res)
        if file_serializer.is_valid():
            file_serializer.save()
            #context['task_id'] = task.id
            #context['task_status'] = task.status
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return render(request, context)
        # return res

class TaskView(APIView):
    def get(self, request):
        task_id = request.GET.get('res')
        task_status = app.AsyncResult(task_id).state
        # task_status = task.state
        # print('{}, {}'.format(task_id, task_status))
        if task_status == 'PENDING':
            return Response(task_status, task_id, status=status.HTTP_404_NOT_FOUND)
        elif task_status == 'STARTED':
            return Response(task_status, task_id, status=status.HTTP_201_CREATED)
        elif task_status == 'SUCCESS':
            return Response(task_status, task_id, status=status.HTTP_200_OK)
        elif task_status == 'FAILURE':
            return Response(task_status, task_id, status=status.HTTP_409_CONFLICT)
        elif task_status == 'RETRY':
            return Response(task_status, task_id, status=status.HTTP_100_CONTINUE)
        else
            return Response(task_status, task_id, status=status.HTTP_205_RESET_CONTENT)

        # tasks = Task.objects.filter(id=pk)
        # print(tasks)
        # serializer = TaskSerializer(tasks, many=True)
        # return Response({"task": serializer.data})

    # def post(self, request):
    #     task = request.data.get('task')
    #     serializer = TaskSerializer(data=task)
    #     if serializer.is_valid(raise_exception=True):
    #         task_saved = serializer.save()
    #     return Response({"success": "Task '{}' created successfully".format(task_saved.status)})
    #
    # def put(self, request, pk):
    #     saved_task = get_object_or_404(Task.objects.all(), pk=pk)
    #     data = request.data.get('task')
    #
    #     serializer = TaskSerializer(instance=saved_task, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         task_saved = serializer.save()
    #     return Response({"success": "Task '{}' updated successfully".format(task_saved.status)})
    #
    # def delete(self, request, pk):
    #     task = get_object_or_404(Task.objects.all(), pk=pk)
    #     task.delete()
    #     return Response({"message": "Task with id '{}' has been deleted".format(pk)}, status=204)



