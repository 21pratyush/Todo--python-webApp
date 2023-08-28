from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key' 

db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = TodoItem.query.order_by(TodoItem.completed, TodoItem.id).all()
    completed_count = TodoItem.query.filter_by(completed=True).count()
    total_count = TodoItem.query.count()
    return render_template('index.html', tasks=tasks, completed_count=completed_count, total_count=total_count)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content'].strip()

    # Checking if the content is not empty
    if content:
        new_task = TodoItem(content=content)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Please enter a valid task.', 'error')

    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = TodoItem.query.get(task_id)
    task.completed = True
    db.session.commit()
    flash('Task marked as completed.', 'success')
    return redirect('/')

@app.route('/incomplete/<int:task_id>')
def incomplete_task(task_id):
    task = TodoItem.query.get(task_id)
    task.completed = False
    db.session.commit()
    flash('Task marked as incomplete.', 'success')
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = TodoItem.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
