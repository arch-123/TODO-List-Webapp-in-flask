from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tasks = request.form['task']
        new_task = Todo(task = tasks)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Sorry! There is a problem creating your task."
        
    else:
        all_tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks = all_tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Sorry there is a problem deleting this task."


@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "GET":
        return render_template("update.html",task = task_to_update)
    
    if request.method=="POST":
        task_to_update.task = request.form['task']
    
    try:
        db.session.commit()
        return redirect("/")
    except:
        return "Sorry! There is an error updating this task."


if __name__=="__main__":
    app.run(debug=True)