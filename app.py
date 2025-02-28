from flask import Flask, render_template, url_for, redirect
from resources.py.db_helper import DBHelper
from resources.py import util

app = Flask(__name__)
db = DBHelper(host="localhost", user="root", password="", database="cs727_baseball")


@app.context_processor
def utility_processor():
    return {"util": util}


# # # # # #
# # # # # #
# ROUTES
# # # # # #
# # # # # #


@app.route("/")
def index():
    return redirect(url_for("home"))
    pass


@app.route("/home/")
def home():
    return render_template("index.html", index_data=db.read("players"))
    pass


# # # # # #
# CRUD
# # # # # #


@app.route("/read/<table>")
def read(table):
    return render_template(
        "crud_read.html", table_data=db.read(table), crud_op="read", table=table
    )
    pass


@app.route("/create/<table>")
def create(table):
    return render_template(
        "crud_create.html", table_data=db.read(table), crud_op="create", table=table
    )
    pass


if __name__ == "__main__":
    app.run(debug=True)
