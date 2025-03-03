QUERY_MAPPINGS = {
    #
    #
    #
    # set operations
    #
    "union": {
        "category": "set_operations",
        "name": "Union",
        "icon": "bi-union",
        "query_type": "static",
        "query": "SELECT home_team_id AS team_id FROM games\r\nUNION\r\nSELECT away_team_id FROM games;",
        "description": "This query returns a list of all teams that have played at least one game (either home or away).",
    },
    "intersect": {
        "category": "set_operations",
        "name": "Intersect",
        "icon": "bi-intersect",
        "query_type": "static",
        "query": "SELECT player_id FROM batting_statistics WHERE season_id = 3\r\nINTERSECT\r\nSELECT player_id FROM batting_statistics WHERE season_id = 2;",
        "description": "This query finds players who had stats recorded in both 2023 and 2024.",
    },
    "except": {
        "category": "set_operations",
        "name": "Except",
        "icon": "bi-exclude",
        "query_type": "static",
        "query": "SELECT player_id FROM batting_statistics WHERE season_id = 3\r\nEXCEPT\r\nSELECT player_id FROM batting_statistics WHERE season_id = 2;\r\n",
        "description": "This query lists players who played in 2023 but not in 2024.",
    },
    #
    #
    #
    # set  membership
    #
    "home_run_threshold": {
        "category": "set_membership",
        "name": "Home Run Threshold",
        "icon": "fa-baseball-bat-ball",
        "query_type": "dynamic",
        "query": "SELECT player_id, first_name, last_name \r\nFROM players \r\nWHERE player_id IN (SELECT player_id FROM batting_statistics WHERE home_runs > ?);",
        "column": "batting_statistics.home_runs",
        "description": "desv.",
    },
}


UNIQUE_QUERY_MAPPING_CATEGORIES = set(
    query_info["category"] for query_info in QUERY_MAPPINGS.values()
)


def filter_by_category(category):
    filtered = {
        key: value
        for key, value in QUERY_MAPPINGS.items()
        if value["category"] == category
    }
    return filtered
