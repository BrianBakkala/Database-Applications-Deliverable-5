from resources.py.db_helper import DBHelper
from resources.py import util, query_maps
import json

db = DBHelper(host="localhost", user="root", password="", database="cs727_baseball")


def create(obj):
    return db.create(table=obj["table"], data=obj["data"])


def delete(obj):
    return db.delete(table=obj["table"], record_id=obj["record_id"])


def update(obj):
    return db.update(table=obj["table"], record_id=obj["record_id"], data=obj["data"])


def dynamic_query(obj):
    query = query_maps.QUERY_MAPPINGS[obj["mapping_key"]]["query"].replace("?", "%s")
    input = obj["input"]
    result = db.run_query(
        query,
        {"input": obj["input"]},
    )
    html = util.render_template_string_with_components_context(
        """
        
        {{ readOnlyTable(display_data) }}
        """,
        display_data=db.prep_query_for_display(
            query=query, query_params={"input": obj["input"]}
        ),
    )["html"]

    return {"result": result, "input": input, "html": html}
