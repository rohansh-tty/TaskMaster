from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from os import environ
import logging 
import traceback

#logging.basicConfig(filename='app.log',encoding='utf-8',level=logging.WARNING, filemode = 'w', format='%(process)d-%(levelname)s-%(message)s')


app = Flask(__name__)
app.config["ENV"] = 'development'
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# TODO List App 
class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
with app.app_context():
    db.create_all()

@app.route("/")
def main():
    #return "TaskMaster it is!"
    todo_list = Todo.query.all()
    return render_template('base.html',todo_list = todo_list)

@app.route("/add", methods=["POST"])
def add():
    try:
        title = request.form.get('title')
        if len(title)>0: 
            new_todo = Todo(title=title, complete=False)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for("main"))
        
    except Exception as e:
        print(f"Failed to add new todo, {traceback.format_exc(e)}")

@app.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
        return redirect(url_for("main"))
    except Exception as e:
       print(f"Failed to update status todo {todo_id}, {traceback.format_exc(e)}")

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    #db.create_all()
    app.run()

