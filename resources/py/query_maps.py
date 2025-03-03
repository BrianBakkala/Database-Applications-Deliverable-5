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
        "description": "This query finds power hitters who have hit more home runs than the given threshold in a season.",
    },
    "no_games_played": {
        "category": "set_membership",
        "name": "No Games Played",
        "icon": "bi-x-lg",
        "query_type": "static",
        "query": "SELECT player_id, first_name, last_name \r\nFROM players \r\nWHERE player_id NOT IN (SELECT DISTINCT player_id FROM batting_statistics);",
        "description": "This finds players who exist in the players table but never recorded any batting stats.",
    },
    #
    #
    #
    # subqueries using with
    #
    "rbi_leaders": {
        "category": "subqueries_using_'WITH'",
        "name": "RBI Leaders",
        "icon": "fa-up-long",
        "query_type": "dynamic",
        "query": "WITH RBIleaders AS (\r\n    SELECT player_id, SUM(rbi) AS total_rbi \r\n    FROM batting_statistics \r\n    WHERE season_id = 2 \r\n    GROUP BY player_id\r\n)\r\nSELECT p.player_id, p.first_name, p.last_name, rbil.total_rbi \r\nFROM players p\r\nJOIN RBIleaders rbil ON p.player_id = rbil.player_id\r\nORDER BY rbil.total_rbi DESC\r\nLIMIT ?;",
        "column": "batting_statistics.rbi",  # not really, just an integer
        "description": "This query finds the top n power hitters in terms of RBIs in a season.",
    },
    "total_season_hrs": {
        "category": "subqueries_using_'WITH'",
        "name": "Total HRs per team per season",
        "icon": "bi-123",
        "query_type": "dynamic",
        "query": "WITH TeamHomeRuns AS (\r\n    SELECT team_id, SUM(home_runs) AS total_home_runs \r\n    FROM batting_statistics \r\n    INNER JOIN players\r\n    \tON players.player_id = batting_statistics.player_id\r\n    WHERE season_id = ? \r\n    GROUP BY team_id\r\n)\r\nSELECT t.team_name, thr.total_home_runs \r\nFROM teams t\r\nJOIN TeamHomeRuns thr ON t.team_id = thr.team_id\r\nORDER BY thr.total_home_runs DESC",
        "column": "seasons.season_id",
        "description": "This ranks teams by total home runs in a given season.",
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
