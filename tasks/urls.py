from django.urls import path
from . import views

urlpatterns = [
    # path('tasks/all', views.TaskViewGet.as_view()),
    path('tasks/get', views.TasksGet.as_view()),
    path('tasks/post', views.TasksPost.as_view()),
    path('tasks/get/<uuid:pk>', views.TasksGetId.as_view()),
    path('tasks/put/<uuid:pk>', views.TasksPut.as_view()),
    path('tasks/del/<uuid:pk>', views.TasksDelete.as_view())
]
