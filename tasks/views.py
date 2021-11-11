from django.shortcuts import render
from django.views import View
from .models import TasksModel
from rest_framework import viewsets
from rest_framework import generics
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import manager
from django.core.exceptions import ValidationError


# @method_decorator(csrf_exempt, name='dispatch')
class TasksGet(View):

    def get(self, request):
        tasks = TasksModel.objects.all()

        serialized_tasks = []
        for task in tasks:
            serialized_tasks.append({
                'id': task.id,
                'Заголовок': task.header,
                'Текст': task.text,
                'Дата': task.date,
                'Выполнено': task.done,
            })
        data = {
            'Задачи': serialized_tasks,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class TasksPost(View):

    def post(self, request):
        post_body = json.loads(request.body)

        task_header = post_body.get('Заголовок')
        task_text = post_body.get('Текст')
        task_date = post_body.get('Дата')

        if task_header and task_text and task_date:
            task_data = {
                'header': task_header,
                'text': task_text,
                'date': task_date,
            }
            try:
                task_obj = TasksModel.objects.create(**task_data)
                data = {
                    'message': 'Новая задача была создана с id {}'.format(task_obj.id)
                }
                return JsonResponse(data, status=201, safe=False)
            except ValidationError:
                data = {
                    'message': "Поле 'Дата' введено неверно. Ожидаемый формат ГГГГ-ММ-ДД"
                }
                return JsonResponse(data)
        else:
            data = {
                'message': 'Отсутствует необходимое поле. Введите корректные данные'
            }
            return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class TasksGetId(View):

    def get(self, request, pk):
        # pk = self.kwargs['pk']
        task = TasksModel.objects.get(id=pk)

        data = {
            'Заголовок': task.header,
            'Текст': task.text,
            'Дата': task.date,
            'Выполнена': task.done,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class TasksPut(View):

    def put(self, request, pk):
        task = TasksModel.objects.get(id=pk)
        task.done = 'Да'
        task.save()
        data = {
            'message': 'Задача {} помечена как выполненная.'.format(task.header)
        }
        return JsonResponse(data, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TasksDelete(View):

    def delete(self, request, pk):
        task = TasksModel.objects.get(id=pk)
        del_id = task.id
        task.delete()

        data = {
            'message': 'Задача {} была удалена.'.format(del_id)
        }
        return JsonResponse(data, status=204 )


# @method_decorator(csrf_exempt, name='dispatch')
# class TasksDeleteAll(View):
#
#     def delete(self, request):
#         tasks = TasksModel.objects.all()
#         for task in tasks:
#             task.delete()
#         data = {
#             'message': 'Все задачи удалены.'
#         }
#         return JsonResponse(data)
#
# class TasksPut(View):
#
#     def put(self, request):

# class TaskViewGet(generics.ListAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TaskSerializer
#
# #
# class TaskViewPut(generics.CreateAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TaskSerializer
#

# Create your views here.
