from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage with dummy data
tasks = [
    {
        'id': 1,
        'title': 'Task 1',
        'description': 'Description for Task 1',
        'due_date': '2023-06-30',
        'status': 'Incomplete'
    },
    {
        'id': 2,
        'title': 'Task 2',
        'description': 'Description for Task 2',
        'due_date': '2023-07-15',
        'status': 'In Progress'
    },
    {
        'id': 3,
        'title': 'Task 3',
        'description': 'Description for Task 3',
        'due_date': '2023-08-10',
        'status': 'Completed'
    }
]

# Endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.form['title'],
        'description': request.form['description'],
        'due_date': request.form['due_date'],
        'status': request.form['status']
    }
    # print("new_task", new_task)
    # adding task to tasks list
    tasks.append(new_task)
    return jsonify({'message': 'Task created'}, new_task), 201

# Endpoint to retrieve a single task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    
    return jsonify({'message': 'Task not found'}), 404

# Endpoint to update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = request.form.get('title', task['title'])
            task['description'] = request.form.get('description', task['description'])
            task['due_date'] = request.form.get('due_date', task['due_date'])
            task['status'] = request.form.get('status', task['status'])
            return jsonify(task)
        
    return jsonify({'message': 'Task not found'}), 404

# Endpoint to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({'message': 'Task with ID deleted'})
    
    return jsonify({'message': 'Task not found'}), 404

# Endpoint to list all tasks
@app.route('/tasks', methods=['GET'])
def task_list():
    # page represents the page number
    # page_size represents the no. of tasks to be displayed on each page
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)

    # start_index & end_index is used to slice the tasks, and return the desired set of tasks to be displayed on each page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_tasks = tasks[start_index:end_index]
    # /tasks?page=1&page_size=4
    return jsonify(paginated_tasks)

if __name__ == '__main__':
    app.run()
