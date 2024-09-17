from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='FrontEnd')

tasks = []

@app.route('/')
def home():

    # return "Hello, Flask!"
    return render_template('home.html')


@app.route('/create-task')
def create_task():
    if request.method == 'POST':
        # Get the task name from the form submission
        task_name = request.form['task_name']
        # Add the task to the tasks list (in a real app, you would use a database)
        tasks.append({'name': task_name})
        # Redirect to the page that shows all tasks
        return redirect(url_for('all_tasks'))
    return render_template('create_task.html')

@app.route('/all-tasks')
def all_tasks():
    # Render the template and pass the list of tasks
    return render_template('all_tasks.html', tasks=tasks)

def say_hello():
    print ("Hello")
    
if __name__ == '__main__':
    app.run(debug=True)


