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
        "category": "subqueries_using_W‌I‌T‌H",
        "name": "RBI Leaders",
        "icon": "fa-up-long",
        "query_type": "dynamic",
        "query": "WITH RBIleaders AS (\r\n    SELECT player_id, SUM(rbi) AS total_rbi \r\n    FROM batting_statistics \r\n    WHERE season_id = 2 \r\n    GROUP BY player_id\r\n)\r\nSELECT p.player_id, p.first_name, p.last_name, rbil.total_rbi \r\nFROM players p\r\nJOIN RBIleaders rbil ON p.player_id = rbil.player_id\r\nORDER BY rbil.total_rbi DESC\r\nLIMIT ?;",
        "column": "batting_statistics.rbi",  # not really, just an integer
        "description": "This query finds the top n power hitters in terms of RBIs in a season.",
    },
    "total_season_hrs": {
        "category": "subqueries_using_W‌I‌T‌H",
        "name": "Total HRs per team per season",
        "icon": "bi-123",
        "query_type": "dynamic",
        "query": "WITH TeamHomeRuns AS (\r\n    SELECT team_id, SUM(home_runs) AS total_home_runs \r\n    FROM batting_statistics \r\n    INNER JOIN players\r\n    \tON players.player_id = batting_statistics.player_id\r\n    WHERE season_id = ? \r\n    GROUP BY team_id\r\n)\r\nSELECT t.team_name, thr.total_home_runs \r\nFROM teams t\r\nJOIN TeamHomeRuns thr ON t.team_id = thr.team_id\r\nORDER BY thr.total_home_runs DESC",
        "column": "seasons.season_id",
        "description": "This ranks teams by total home runs in a given season.",
    },
    "highest_scoring_games": {
        "category": "subqueries_using_W‌I‌T‌H",
        "name": "Highest scoring games",
        "icon": "bi-123",
        "query_type": "dynamic",
        "query": "WITH GameScores AS (\r\n    SELECT game_id, home_team_id, away_team_id, \r\n           (home_team_score + away_team_score) AS total_runs\r\n    FROM games\r\n)\r\nSELECT gs.game_id, \r\n       home_team.team_name AS home_team, \r\n       away_team.team_name AS away_team, \r\n       gs.total_runs \r\nFROM GameScores gs\r\nJOIN teams home_team ON gs.home_team_id = home_team.team_id\r\nJOIN teams away_team ON gs.away_team_id = away_team.team_id\r\nHAVING total_runs>?\r\nORDER BY gs.total_runs DESC",
        "column": "games.home_team_score",
        "description": "This finds the highest-scoring games ever played.",
    },
    #
    #
    #
    # advanced aggregate fns
    #
    "avg_margin_victory": {
        "category": "advanced_functions",
        "name": "Average Margin of Victory",
        "icon": "bi-distribute-horizontal",
        "query_type": "static",
        "query": "SELECT \r\n\tt.team_name,\r\n\tAVG(\r\n\t\t\r\n\t\tCASE \r\n\t\t\tWHEN g.home_team_id = t.team_id THEN g.home_team_score - g.away_team_score\r\n\t\t\tWHEN g.away_team_id = t.team_id THEN g.away_team_score - g.home_team_score\r\n\t\t\tELSE 0 \r\n\t\tEND) AS avg_margin_of_victory\r\nFROM games g\r\nJOIN  teams t ON g.home_team_id = t.team_id OR g.away_team_id = t.team_id\r\nGROUP BY \r\n\tt.team_name\r\nORDER BY \r\n\tavg_margin_of_victory DESC;",
        "description": "This query returns the average margin of victory for each team",
    },
    "highest_scoring_stadiums": {
        "category": "advanced_functions",
        "name": "Highest-scoring stadiums",
        "icon": "bi-123",
        "query_type": "static",
        "query": "SELECT s.stadium_name, \r\n\tSUM(g.home_team_score + g.away_team_score) AS total_score\r\nFROM games g\r\nJOIN \r\n\tstadiums s ON g.stadium_id = s.stadium_id\r\nGROUP BY \r\n\ts.stadium_name\r\nORDER BY \r\n\ttotal_score DESC ",
        "description": 'This query returns the "best" stadiums, i.e. the ones that produces the most total runs',
    },
    "best_obp_rank": {
        "category": "advanced_functions",
        "name": "Best season OBP rank",
        "icon": "bi-123",
        "query_type": "dynamic",
        "query": "SELECT\r\n\tb.player_id, players.first_name, players.last_name, MIN(obp_rank) as best_obp_rank\r\nFROM \r\n\tbatting_statistics b \r\nINNER JOIN \r\n(\r\n\tSELECT player_id,\r\n\t\tRANK() OVER (PARTITION BY season_id ORDER BY on_base_percentage DESC) \r\n\t\tAS obp_rank\r\n\tFROM batting_statistics \r\n\tORDER BY player_id\r\n) as obp_ranks\r\nON\r\n\t(obp_ranks.player_id = b.player_id) \r\nINNER JOIN \r\n\tplayers ON\r\n    \tplayers.player_id = b.player_id\r\nWHERE \r\n\tb.player_id=?\r\nGROUP BY \r\n\tplayer_id",
        "column": "batting_statistics.player_id",
        "description": "This query gets the best rankings of players in on base percentage across multiple seasons. For example, if a player was ranked 1st, 3rd, and 5th across three seasons, return the best rank, rank 1",
    },
    "season_hr_rank": {
        "category": "advanced_functions",
        "name": "Season HR rank",
        "icon": "fa-baseball-bat-ball",
        "query_type": "dynamic",
        "query": "SELECT  p.first_name, p.last_name, home_runs,\r\nRANK() OVER (ORDER BY home_runs DESC) AS home_run_rank\r\nFROM batting_statistics b\r\nJOIN players p ON b.player_id = p.player_id\r\nWHERE season_id = ?;",
        "column": "batting_statistics.season_id",
        "description": "This query ranks players based on the number of home runs they hit during a given season using the RANK() window function. ",
    },
    #
    #
    #
    # olap
    #
    "sub_grand_hrs": {
        "category": "O‌L‌A‌P",
        "name": "Subtotals and Grand Totals of HRs",
        "icon": "fa-list-check",
        "query_type": "static",
        "query": "SELECT \r\n\tb.player_id, \r\n\ts.year, \r\n\tSUM(b.home_runs) AS total_home_runs\r\nFROM \r\n\tbatting_statistics b  \r\nJOIN \r\n\tseasons s ON b.season_id = s.season_id\r\nGROUP BY \r\nb.player_id, s.year\r\nWITH ROLLUP;",
        "description": "This query gets the subtotals and grand totals of homeruns per player per season",
    },
    "sub_grand_stats": {
        "category": "O‌L‌A‌P",
        "name": "Subtotals and Grand Totals of Stats",
        "icon": "fa-list-check",
        "query_type": "static",
        "query": "SELECT first_name, last_name, total_home_runs, total_rbi,  avg_batting_avg,  avg_batting_obp FROM\r\n\t(\r\n\t\tSELECT player_id, season_id ,\r\n\t\t\tSUM(home_runs) AS total_home_runs,\r\n\t\t\tSUM(rbi) AS total_rbi,\r\n\t\t\tAVG(batting_avg) AS avg_batting_avg,\r\n\t\t\tAVG(on_base_percentage) AS avg_batting_obp\r\n\t\tFROM batting_statistics\r\n\t\tGROUP BY player_id, season_id WITH ROLLUP \r\n\r\n\t)  as sub\r\n\r\nLEFT JOIN players p ON sub.player_id = p.player_id AND season_id IS NOT NULL;",
        "description": "This query gets the subtotals and grand totals for all stats for players across multiple seasonsm, using rollup to show subtotals of player's stats across multiple seasons. The subquery does the heavy lifting, and the outer query adds the player's names",
    },
}


UNIQUE_QUERY_MAPPING_CATEGORIES = sorted(
    set(query_info["category"] for query_info in QUERY_MAPPINGS.values()), key=str.lower
)


def filter_by_category(category):
    filtered = {
        key: value
        for key, value in QUERY_MAPPINGS.items()
        if value["category"] == category
    }
    return filtered
