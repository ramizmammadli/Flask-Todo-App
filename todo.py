from flask import Flask, render_template,redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

# in this gui app, we'll create a Todo App by the help of ORM notion in SQLite3


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/vscode/python/ToDoApp/todo.db' # path of database must be given.
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all() # in todos, there is all data of the table now.
    return render_template("index.html", todos = todos)

@app.route("/add", methods = ["POST"]) # the data can only be put to the database.
def addTodo():
    
    title = request.form.get("title") # title is the name of input area.
    newTodo = Todo(title = title, complete = False) # newTodo object is created from Todo class. 2 parameters are sent. the entered input and complete boolean as a false.
    
    db.session.add(newTodo) # added to database by using the logic of ORM. ORM is kind of shortcut of manipulatiing db. Instead of writing long requests for db, we can simply use methods of ORM.
    db.session.commit() # applied to db.
    
    return redirect(url_for("index")) 

@app.route("/complete/<string:id>") #dynamic url is used.
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() # here, id (sent by dynamic url) will be matched by id (the one which is clicked). and it will be put to todo variable.

    todo.complete = not todo.complete # it changes complete from true to false or vice versa.

    db.session.commit() # applied to db.
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo) # directly deletes from db.
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # a table created with the columns of id, title, complete.
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    db.create_all() #applies to db.
    app.run(debug=True)