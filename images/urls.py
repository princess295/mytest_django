from django.urls import path
from .views import TaskView, FileUploadView

app_name = "tasks"

urlpatterns = [
    path(r'tasks/', TaskView.as_view()),
    path('', FileUploadView.as_view())

]
