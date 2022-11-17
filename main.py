from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
#import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#all_books = []
#db = sqlite3.connect("books-collection.db")
#cursor = db.cursor()
#cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
#db.commit()

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.author} - {self.rating}/10"


db.create_all()


class LibraryForm(FlaskForm):
    book = StringField('Book name', validators=[DataRequired()])
    author = StringField('Book author', validators=[DataRequired()])
    rating = SelectField(u'Rating', choices=[( '☕'), ('☕☕'), ('☕☕☕'), ('☕☕☕☕'), ('☕☕☕☕☕')],validators=[DataRequired()])
    submit = SubmitField('Ad book')


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("index.html", all_books=all_books)


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    modifyBook = Book.query.get(id)
    if request.method == "POST":
        rating=float(request.form["rating"])
        modifyBook.rating = rating
        db.session.commit()
        all_books = Book.query.all()
        return  render_template("index.html", all_books=all_books)
    return render_template("edit.html", book=modifyBook)


@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    modifyBook = Book.query.get(id)
    db.session.delete(modifyBook)
    db.session.commit()
    all_books = Book.query.all()
    return render_template("index.html", all_books=all_books)


@app.route("/add",methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book=request.form["book"]
        author=request.form["author"]
        rating = request.form["rating"]
        tmp ={}
        tmp["title"]= book
        tmp["author"] = author
        tmp["rating"]= float(rating)
        booktmp = Book(title=book, author=author, rating=rating)
        db.session.add(booktmp)
        db.session.commit()
        all_books = Book.query.all()
        return render_template("index.html", all_books=all_books)
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

