from flask import Flask, request
from flask_restplus import Api
from resources.task import tasks_ns, TaskList, TaskSingle
from models.task import Task

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

api = Api(app, prefix='/api', title="To Do app", description="Backend для простого To Do приложения", version="1.0",
          validate=True)

api.add_namespace(tasks_ns)

tasks_ns.add_resource(TaskList, '/')
tasks_ns.add_resource(TaskSingle, '/<int:task_id>/')


@app.before_first_request
def create_tables():
    Task.create_table()


if __name__ == '__main__':
    app.run()
