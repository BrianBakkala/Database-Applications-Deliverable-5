from flask import Flask, render_template, url_for, redirect, request, jsonify
from resources.py.db_helper import DBHelper
from resources.py import util, request_commands, query_maps


app = Flask(__name__)
configuration = util.get_config()


db = DBHelper(
    host=configuration["db"]["host"],
    user=configuration["db"]["user"],
    password=configuration["db"]["password"],
    database=configuration["db"]["database"],
)


@app.context_processor
def utility_processor():
    return {"util": util, "query_maps": query_maps}


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


@app.route("/<category>/<key>")
def render_set_membership(category, key):
    data = query_maps.QUERY_MAPPINGS.get(key)
    return render_mapped_query(data, key)
    pass


# # # # # #
# RENDER MODULAR QUERY
# # # # # #


def render_mapped_query(query_data, mapping_key):
    display_data = (
        db.prep_query_for_display(query=query_data.get("query"))
        if query_data["query_type"] == "static"
        else None
    )

    if query_data["query_type"] == "dynamic" and "column" not in query_data:
        raise ValueError("The 'column' key is required for dynamic queries.")

    if "column" in query_data:
        parts = query_data["column"].split(".")
        column_data = db.get_columns_data(parts[0])[parts[1]]
    else:
        column_data = None

    query_type = query_data["query_type"]

    return render_template(
        f"{query_type}_query.html",
        data=query_data,
        mapping_key=mapping_key,
        column_data=column_data,
        display_data=display_data,
    )


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
