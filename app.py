from flask import Flask
from flask_restx import Api, Resource
from todo import Todo

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Demo API Server",
    description="Flask Demo Api Server"
)


# @api.route("/test")
# class Test(Resource):
#     def get(self):
#         return "call get method"
#
#
# @api.route("/hello/<string:name>")
# class Hello(Resource):
#     def get(self, name):
#         return {"messgae": "Welcome, %s!" % name}
api.add_namespace(Todo, "/todos")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
