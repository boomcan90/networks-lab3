from flask import Flask
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from flask_httpauth import HTTPBasicAuth


app=Flask(__name__)
auth = HTTPBasicAuth()

# dummy user info

@auth.get_password
def get_password(username):
    if username in users.keys():
        return users[username]
    return None

@auth.error_handler
def error():
    return make_response(jsonify({'Error': 'Not authorized'}), 401)

# dummy test data

todo_items = [
    {
        'user': 'abc',
        'title': u'Get Networks lab done',
        'description': u'The deadline is Tuesday',
        'completed': "False"
    },
    {
        'user': 'def',
        'title': u'Film HASS shooting',
        'description': u'Setup at 1:30 pm on friday; shooting thereafter',
        'completed': "False"
    }
]

# dummy user information
users = {
        'abc': '123',
        'def': '456'
        }

# url for api: localhost:5000/api/
@auth.login_required
@app.route("/api/todoitem", methods=['GET'])
def alltasks():
    try:
        request.authorization.username
    except:
        abort(401)
    user_todo = todo_list(request.authorization.username)
    return jsonify({'todo_items' : user_todo})

@auth.login_required
@app.route("/api/todoitem/completed", methods=['GET'])
def completed():
    user_todo = todo_list(request.authorization.username)
    return jsonify({'todo_items':[todoitem for todoitem in user_todo if todoitem['completed']=='True']})

@auth.login_required
@app.route('/api/todoitem/notcompleted', methods=['GET'])
def incomplete():
    user_todo = todo_list(request.authorization.username)
    return jsonify({'todo_items': [todoitem for todoitem in user_todo if todoitem['completed'] != 'True']})

@auth.login_required
@app.route('/api/todoitem/<int:num>', methods=['GET'])
def todo_item(num):
    user_todo = todo_list(request.authorization.username)
    if len(user_todo) < num - 1:
        abort(404)
    return jsonify({'todo_items': user_todo[num-1]})

@app.route('/api/todoitem/<int:num>', methods=['PUT'])
@auth.login_required
def update(num):
    user_todo = todo_list(request.authorization.username)
    if len(user_todo) < num-1:
        abort(404)
    for j in request.json:
        user_todo[num-1][j] = request.json[j]

    return jsonify({'todo_items': user_todo[num-1]})

@app.route('/api/todoitem/<int:num>', methods=["DELETE"])
@auth.login_required
def delete(num):
    user_todo = todo_list(request.authorization.username)
    if len(user_todo) <  num:
        abort(404)
    todo_items.remove(user_todo[num-1])
    user_todo = todo_list(request.authorization.username)
    return jsonify({'todo_items': user_todo})


@app.errorhandler(404)
def error(num):
    return make_response(jsonify({'Error':'Not found'}), 404)

@app.errorhandler(400)
def error(num):
    return make_response(jsonify({'Error':'Not allowed'}), 400)

@app.errorhandler(401)
def error(num):
    return make_response(jsonify({'Error': 'Not authorized'}), 401)

@app.route('/api/todoitem', methods=['POST'])
@auth.login_required
def add():
    if not request.json:
        abort(400)
    todo_item = {
        'user' : request.authorization.username ,
        "title" : request.json['title'],
        "description" : request.json['description'],
        "completed" : "False"
    }
    todo_items.append(todo_item)
    user_items = todo_list(todo_item['uname'])
    return jsonify({'todo_items': user_todo}), 201

@app.route('/api/users', methods=['GET'])
@auth.login_required
def allusers():
    return jsonify({'users': list(users.keys())})

# helper functions

def todo_list(uname):
    user_todo =[]
    for item in todo_items:
        if item['user'] == uname:
            user_todo.append(item)
    if len(user_todo) == 0:
        return None
    return user_todo


# url for showing: localhost:5000/todolist


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
