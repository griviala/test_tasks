from app import app
from unittest import TestLoader, TestCase
import json


TestLoader.sortTestMethodsUsing = None


app.testing = True


class TaskStorageId:

    def __init__(self):
        self.task_bad = -1
        self.task_good = 1


testValue = TaskStorageId()


class TaskTest(TestCase):

    def test_a(self):
        with app.test_client() as client:
            r = client.post('/api/task/', json={"title": "Новая задача", "content": "Какой-то контент"})
            testValue.test_good = json.loads(r.data)['id']
            self.assertEqual(r.status_code, 200)

    def test_b(self):
        with app.test_client() as client:
            r = client.post('/api/task/', json={"content": "Новая задача"})
            self.assertEqual(r.status_code, 400)

    def test_c(self):
        with app.test_client() as client:
            r = client.put('/api/task/{}/'.format(testValue.task_good), json={"title": "Новая задача", "content": "Какой-то контент"})
            self.assertEqual(r.status_code, 200)

    def test_d(self):
        with app.test_client() as client:
            r = client.put('/api/task/{}/'.format(testValue.task_good), json={"title": "Новый апдейт"})
            self.assertEqual(r.status_code, 200)

    def test_e(self):
        with app.test_client() as client:
            r = client.put('/api/task/{}/'.format(testValue.task_bad), json={"title": "Новый апдейт"})
            self.assertEqual(r.status_code, 404)

    def test_f(self):
        with app.test_client() as client:
            r = client.get('/api/task/')
            self.assertEqual(r.status_code, 200)

    def test_g(self):
        with app.test_client() as client:
            r = client.get('/api/task/{}/'.format(testValue.task_good))
            self.assertEqual(r.status_code, 200)

    def test_h(self):
        with app.test_client() as client:
            r = client.get('/api/task/{}/'.format(testValue.task_bad))
            self.assertEqual(r.status_code, 404)

    def test_i(self):
        with app.test_client() as client:
            r = client.delete('/api/task/{}/'.format(testValue.task_good))
            self.assertEqual(r.status_code, 200)

    def test_j(self):
        with app.test_client() as client:
            r = client.delete('{}/api/task/{}/'.format(testValue.task_bad))
            self.assertEqual(r.status_code, 404)

    def test_k(self):
        with app.test_client() as client:
            r = client.get('/api/task/')
            self.assertEqual(r.status_code, 400)
