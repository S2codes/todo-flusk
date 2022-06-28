from flask import Flask, redirect, render_template,  request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable = False)
    decs = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['note']

        todo = ToDo(title = title, decs = desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = ToDo.query.all()
    return render_template('index.html', allTodo = allTodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_todo(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['note']
        filter_todo = ToDo.query.filter_by(sno=sno).first()
        filter_todo.title = title
        filter_todo.decs = desc
        db.session.add(filter_todo)
        db.session.commit()
        return redirect('/')

    filter_todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', updateTodo = filter_todo)

@app.route("/delete/<int:sno>")
def delete_todo(sno):
    filter_todo = ToDo.query.filter_by(sno=sno).first()
    print(filter_todo)
    db.session.delete(filter_todo)
    db.session.commit()
    return redirect('/')


@app.route("/products")
def products():
    return "<p>This IS product page</p>"



if __name__ == "__main__":
    app.run(debug=True, port=8000)