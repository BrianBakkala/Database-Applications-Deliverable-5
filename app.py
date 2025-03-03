from flask import Flask, render_template, url_for, redirect, request, jsonify
from resources.py.db_helper import DBHelper
from resources.py import util
from resources.py import request_commands

app = Flask(__name__)
db = DBHelper(host="localhost", user="root", password="", database="cs727_baseball")


@app.context_processor
def utility_processor():
    return {"util": util}


# # # # # #
# # # # # #
# MAIN ROUTES
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


@app.route("/crud/<table>")
def render_crud(table):
    return render_template(
        "crud.html",
        table_data=db.read(table),
        table=table,
        columns_data=db.get_columns_data(table),
    )
    pass


@app.route("/set-ops/<set_op>")
def render_set_ops(set_op):

    op_data = util.SET_OPERATIONS.get(set_op)
    return render_template(
        "set_ops.html",
        data={"hello": "world"},
        set_op=set_op,
        set_op_data=op_data,
        display_data=db.prep_query_for_display(query=op_data.get("query")),
    )
    pass


# # # # # #
# REQUEST COMMANDS
# # # # # #


@app.route("/request/<command>", methods=["POST"])
def perform_request(command):

    # grab data
    content = request.get_json(silent=True)

    # ensure command exists in request_commands
    if not hasattr(request_commands, command):
        return jsonify({"error": "Invalid command"}), 400

    function_name = getattr(request_commands, command)

    # ensure function is callable
    if not callable(function_name):
        return jsonify({"error": "Command is not callable"}), 400

    # call the function and enforce JSON response
    try:
        response = function_name(content)

        if isinstance(response, dict):
            return jsonify(response)

        if isinstance(response, str):  #   string responses
            return jsonify({"result": response})

        return response  # assume it's already a valid Flask Response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
