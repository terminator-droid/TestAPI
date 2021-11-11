from django.test import TestCase, Client
from .models import TasksModel
import requests
from django.http import JsonResponse
import json


class TaskTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.task_1 = TasksModel.objects.create(id='c0af7f44-6221-4db8-8fd1-8d4d836fc8e7', header='Тест',
                                                text='Тестовая задача', date='2021-01-01')
        self.task_2 = TasksModel.objects.create(header='Вторая', text='Тестовая задача два', date='2021-01-01')

        self.post = {
            "Заголовок": "Написать API",
            "Текст": "Написать RESTfull API на Django",
            "Дата": "2021-11-10"
        }

    def test_task_get_all(self):
        response = self.client.get('/tasks/get')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_task_get_detail(self):
        response = self.client.get('/tasks/get/c0af7f44-6221-4db8-8fd1-8d4d836fc8e7')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_task_put(self):
        response = self.client.put('/tasks/put/c0af7f44-6221-4db8-8fd1-8d4d836fc8e7')
        print(json.loads(response.content))
        self.assertEqual(response.status_code, 201)

    def test_task_delete(self):
        response = self.client.delete('/tasks/put/c0af7f44-6221-4db8-8fd1-8d4d836fc8e7')
        print(response.content)
        self.assertEqual(response.status_code, 204)

    def test_post_task(self):
        response = self.client.post('/tasks/post', {'Заголовок': 'Постирать вещи',
                                                    'Текст': 'Написать RESTfull API на Django',
                                                    'Дата': '2021-11-10'
                                                    })
        print(response.text)
