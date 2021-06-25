from flask import request, jsonify, make_response
from flask_restplus import Resource, Namespace, fields
from playhouse.shortcuts import model_to_dict
from models.task import Task, DoesNotExist

tasks_ns = Namespace("task", description='Операции с задачами')

task_model = tasks_ns.model('Задача', {
    'id': fields.Integer(title='Id задачи'),
    'title': fields.String(title='Название задачи'),
    'created_at': fields.DateTime(title='Дата создания задачи')
})

task_single = tasks_ns.model('Задача (детальная задача)', {
    'title': fields.String(title='Название задачи'),
    'content': fields.String(title='Описание задачи'),
    'created_at': fields.DateTime(title='Дата создания задачи')
})

task_model_in = tasks_ns.model('Задача (получение данных)', {
    'title': fields.String(title='Название задачи'),
    'content': fields.String(title='Описание задачи')
})


task_response_message = tasks_ns.model('Ответ', {
    'message': fields.String('Текст ответа')
})

task_list = tasks_ns.model('Список задач', {
    'tasks': fields.List(fields.Nested(task_model))
})


class TaskList(Resource):
    @tasks_ns.doc("Создание новой задачи")
    @tasks_ns.response(200, "Добавляемая задача", task_model)
    @tasks_ns.response(400, "Некорректный набор полей", task_response_message)
    @tasks_ns.response(500, "Внутренняя ошибка сервера", task_response_message)
    @tasks_ns.expect(task_model_in)
    def post(self):
        json_data = request.json
        try:
            task = Task(title=json_data["title"], content=json_data["content"])
            task.save()
            return make_response(jsonify(model_to_dict(task)), 200)
        except KeyError as e:
            return make_response({"message": "Некорректный набор полей"}, 400)
        except Exception as e:
            return make_response({"message": format(e)}, 500)

    @tasks_ns.doc("Получение списка задач")
    # @tasks_ns.marshal_with(task_model, as_list=True, code=200, description="Список всех задач")
    @tasks_ns.response(400, "Список задач пуст", task_response_message)
    @tasks_ns.response(200, "Список задач", task_list)
    @tasks_ns.response(500, "Внутренняя ошибка сервера", task_response_message)
    def get(self):
        try:
            tasks = list(Task.select(Task.id, Task.title, Task.created_at).dicts())
            return make_response(jsonify({"tasks": tasks}), 200) if len(tasks) > 0 else make_response(
                {"message": "Список задач пуст"}, 400)
        except Exception as e:
            return make_response({"message": format(e)}, 500)


@tasks_ns.doc(params={'task_id': 'Id задачи'})
class TaskSingle(Resource):
    @tasks_ns.doc("Получение детальной задачи")
    @tasks_ns.response(404, "Такой задачи не существует", task_response_message)
    @tasks_ns.response(200, "Возвращаемая задача", task_single)
    @tasks_ns.response(500, "Внутренняя ошибка сервера", task_response_message)
    def get(self, task_id):
        try:
            task = Task.select(Task.title, Task.content, Task.created_at).where(Task.id == task_id).dicts().get()
            return make_response(jsonify(task), 200)
        except DoesNotExist:
            return make_response({"message": "Такой задачи не существует"}, 404)
        except Exception as e:
            return make_response({"message": format(e)}, 500)

    @tasks_ns.doc("Изменение задачи")
    @tasks_ns.response(404, "Такой задачи не существует", task_response_message)
    @tasks_ns.response(200, "Возвращаемая задача", task_model)
    @tasks_ns.response(500, "Внутренняя ошибка сервера", task_response_message)
    @tasks_ns.expect(task_model_in, validate=False)
    def put(self, task_id):
        try:
            task = Task.select().where(Task.id == task_id).get()
            if "content" in request.json:
                task.content = request.json["content"]
            if "title" in request.json:
                task.title = request.json["title"]
            task.save()
            return make_response(jsonify(model_to_dict(task)), 200)
        except DoesNotExist:
            return make_response({"message": "Такой задачи не существует"}, 404)
        except Exception as e:
            return make_response({"message": format(e)}, 500)

    @tasks_ns.response(404, "Такой задачи не существует", task_response_message)
    @tasks_ns.response(200, "Задача успешно удалена", task_response_message)
    @tasks_ns.response(500, "Внутренняя ошибка сервера", task_response_message)
    def delete(self, task_id):
        try:
            task = Task.select().where(Task.id == task_id).get()
            task.delete_instance()
            return make_response({"message": "Задача успешно удалена"}, 200)
        except DoesNotExist:
            return make_response({"message": "Такой задачи не существует"}, 404)
        except Exception as e:
            return make_response({"message": format(e)}, 500)
