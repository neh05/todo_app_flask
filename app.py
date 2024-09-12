from flask import Flask , render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask("__name__")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    created = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self)-> str:
        f"{self.name}"
class User(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self)-> str:
        f"{self.username}"
@app.route("/", methods =  ["POST","GET"])
def home():
    if request.method == "POST":
        cur_task = request.form['title']
        desc = request.form['desc']
        new_task = Task(name = cur_task , desc = desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")
    
    else:
        todo = Task.query.all()
        return render_template("index.html", todo = todo)
    
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.filter_by(id= id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):
    task = Task.query.filter_by(id = id).first()
    if request.method == "POST":
        task.title = request.form['title']
        task.desc  = request.form['desc']
        db.session.commit()
        return redirect("/")
    
    else:
        return render_template("update.html",task=task)
    


if __name__ == ("__main__"):
    with app.app_context():
        db.create_all()
    app.run(debug = True,port = 8000)