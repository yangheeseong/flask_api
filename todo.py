from flask import request
from flask_restx import Resource, Api, Namespace, fields
import pymssql

todos = {}
count = 1

Todo = Namespace(name="Todos", description="Todo 리스트 작성 API")

# Model 객체 생성
todo_fields = Todo.model("Todo", {
    "data": fields.String(description="a Todo",
                          required=True,
                          example="what to do")
})

# todo_fields 상속
todo_fields_with_id = Todo.inherit("Todo With ID", todo_fields, {
    "doto_id": fields.Integer(description="a Todo ID")
})

conn = pymssql.connect(host="118.129.153.90:9190",
                       user="ppknwebsvcacc",
                       password="b^9(uZEA}Y6Yhe7=",
                       database="B_ACCOUNT",
                       charset="utf8")


@Todo.route("")
class TodoPost(Resource):
    @Todo.expect(todo_fields)
    @Todo.response(201, 'Success', todo_fields_with_id)
    def post(self):
        """Todo 리스트에 할 일을 등록합니다."""
        global count
        global todos

        idx = count
        count += 1
        todos[idx] = request.json.get("data")

        return {
            "todo_id": idx,
            "data": todos[idx]
        }, 201


@Todo.route("/<int:todo_id>")
@Todo.doc(params={"todo_id": "An ID"})
class TodoSimple(Resource):
    @Todo.response(200, 'Success', todo_fields_with_id)
    @Todo.response(500, 'Failed')
    def get(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 가져옵니다."""
        cursor = conn.cursor()

        cursor.execute("SELECT TOP 10 * FROM [galaxiaTicket] WITH(NOLOCK)")

        row = cursor.fetchone()

        conn.close()

        return {
            "todo_id": todo_id,
            "data": row[0]
        }

    @Todo.response(202, 'Success', todo_fields_with_id)
    @Todo.response(500, 'Failed')
    def put(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 수정합니다."""
        todos[todo_id] = request.json.get("data")

        return {
            "todo_id": todo_id,
            "data": todos[todo_id]
        }, 202

    @Todo.response(202, "Success")
    @Todo.response(500, "Failed")
    def delete(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 삭제합니다."""
        del todos[todo_id]

        return {
            "delete": "success"
        }, 202

