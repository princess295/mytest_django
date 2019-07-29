from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from celery.result import AsyncResult

from .serializers import ImageSerializer, TaskSerializer
from .models import Task, File
from .tasks import app, resize_image
from celery import current_app

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CELERY_TRACK_STARTED = True
TASKS = {}
class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)

        logger.debug('{}, {}, {}'.format(request.method, request.user, request.content_type))

        image = File.objects.all()
        height_im = request.data.get('height_im')
        width_im = request.data.get('width_im')
        data = request.FILES.get('file')
        with open('file', 'wb+') as f:
            for chunk in data.chunks():
                f.write(chunk)
        res = resize_image.delay('file', height_im, width_im)
        task_id = res.id

        if file_serializer.is_valid():
            file_serializer.save()
            TASKS[file_serializer.data['request_id']] = task_id
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    def get(self, request):
        task_id = request.GET.get('res')
        task_id = TASKS.get(int(task_id), None)
        print(TASKS)
        task_status = app.AsyncResult(task_id).state

        if task_status == 'PENDING':
            return Response({'task_status' : task_status,
                             'task_id' : task_id}, status=status.HTTP_404_NOT_FOUND)
        elif task_status == 'STARTED':
            return Response({'task_status': task_status,
                             'task_id': task_id}, status=status.HTTP_201_CREATED)
        elif task_status == 'SUCCESS':
            return Response({'task_status': task_status,
                             'task_id': task_id}, status=status.HTTP_200_OK)
        elif task_status == 'FAILURE':
            return Response({'task_status': task_status,
                             'task_id': task_id}, status=status.HTTP_409_CONFLICT)
        elif task_status == 'RETRY':
            return Response(task_status, task_id, status=status.HTTP_100_CONTINUE)
        else:
            return Response(task_status, task_id, status=status.HTTP_205_RESET_CONTENT)




