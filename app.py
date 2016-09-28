from flask import Flask
from flask import jsonify

app=Flask(__name__)

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


@app.route('/api/todoitem/<int:num>', methods=['GET'])
def task(num):
    task = [task for task in todo_items if task['id'] == num]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# url for showing: localhost:5000/todolist


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)