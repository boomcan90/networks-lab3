from flask import Flask
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
import sys
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
toolbar = DebugToolbarExtension(app)

# dummy test data

todo_items = [
    {
        'id': 1,
        'title': u'Get clara to shut up',
        'description': u'She is too damn irritating',
        'completed': False
    },
    {
        'id': 2,
        'title': u'Please, shut clara up',
        'description': u'She just doesnt know when to shut up',
        'completed': False
    }
]


# url for api: localhost:5000/api/

@app.route("/api/todoitem", methods=['GET'])
def alltasks():
    return jsonify({'todo_items' : todo_items})


@app.route('/api/<int:num>', methods=['GET'])
def todo_item(num):
    todo_item = [todo_item for todo_item in todo_items if todo_item['id'] == num]
    if len(todo_item) == 0:
        abort(404)
    return jsonify({'todo_items': todo_item[0]})

@app.route('/api/<int:num>', methods=['PUT'])
def update(num):
    a = []
    for i in todo_items:
        if i['id'] == num:
            for j in request.json:
                i[j] = request.json[j]

            return jsonify({"i":i})

@app.route('/api/<int:num>', methods=["DELETE"])
def delete(num):
    todo_item = [todo_item for todo_item in todo_items if todo_item['id'] == num]
    if len(todo_item) == 0:
        abort(404)
    todo_items.remove(todo_item[0])
    return jsonify({'todo_items': todo_items})


@app.errorhandler(404)
def error(num):
    return make_response(jsonify({'Error':'Not found'}), 404)

@app.errorhandler(400)
def error(num):
    return make_response(jsonify({'Error':'Not allowed'}), 400)

@app.route('/api/todoitem', methods=['POST'])
def add():
    if not request.json:
        abort(400)
    todo_item = {
        'id' : todo_items[-1]['id'] +1,
        "title" : request.json['title'],
        "description" : request.json['description'],
        "completed" : False
    }
    todo_items.append(todo_item)
    return jsonify({'todo_items': todo_items}), 201


# url for showing: localhost:5000/todolist


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)