TABLE_NAME_MAPPINGS = {
    "batting_statistics": "Batting Statistics",
    "games": "Games",
    "managers": "Coaches",
    "players": "Players",
    "seasons": "Seasons",
    "stadiums": "Stadiums",
    "teams": "Teams",
}
PLAIN_TO_TABLE_MAPPINGS = {v: k for k, v in TABLE_NAME_MAPPINGS.items()}

CRUD_OPERATIONS_ICONS = {
    "create": "plus-lg",
    "read": "eyeglasses",
    "update": "pencil-square",
    "delete": "trash3",
}

CRUD_OPERATIONS = CRUD_OPERATIONS_ICONS.keys()


SET_OPERATIONS = {
    "union": {
        "name": "Union",
        "icon": "union",
        "query": "SELECT first_name FROM players \nUNION \nSELECT first_name FROM managers\n\nORDER BY first_name;",
        "description": "Performs the set operation UNION on the two queries. This will return all unique first names from both tables.",
    },
}


def get_crud_icon(operation):
    return CRUD_OPERATIONS_ICONS.get(operation, "exclamation-triangle-fill")


def convert_table_to_plaintext(table_name):
    """
    Converts a database table name like 'player_stats' into a readable format like 'Player Stats'.
    Falls back to title-case if not found in dictionary.
    """
    return TABLE_NAME_MAPPINGS.get(
        table_name, convert_snake_case_to_readable(table_name)
    )


def convert_snake_case_to_readable(text):
    return text.replace("_", " ").title()


def convert_to_table_name(plain_text):
    """
    Converts a readable name like 'Player Stats' into a database table name like 'player_stats'.
    Falls back to a generic conversion if not found in the dictionary.
    """
    return PLAIN_TO_TABLE_MAPPINGS.get(plain_text, plain_text.lower().replace(" ", "_"))


def hello_world_test():
    return "HW!"
