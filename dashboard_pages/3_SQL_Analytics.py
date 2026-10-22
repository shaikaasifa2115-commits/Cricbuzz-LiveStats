
import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(
    page_title="SQL Analytics | Cricbuzz LiveStats",
    page_icon="🗄️",
    layout="wide",
)


# ---------------- DARK ORANGE THEME ----------------

st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #FF8C1A;
    }

    hr {
        border-color: #FF7A00;
        opacity: 0.55;
    }

    div[data-testid="stAlert"] {
        border-left: 4px solid #FF7A00;
        border-radius: 8px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #FF7A00;
        color: #FFFFFF;
        border: 1px solid #FF7A00;
        border-radius: 8px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #E66D00;
        border-color: #E66D00;
        color: #FFFFFF;
    }

    div.stDownloadButton > button {
        background-color: #FF7A00;
        color: #FFFFFF;
        border: 1px solid #FF7A00;
        border-radius: 8px;
        font-weight: 600;
    }

    div.stDownloadButton > button:hover {
        background-color: #E66D00;
        border-color: #E66D00;
        color: #FFFFFF;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #343A46;
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #FF7A00;
    }

    div[data-testid="stCode"] {
        border: 1px solid #343A46;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- PAGE HEADER ----------------

st.markdown(
    """
    <h1 style="
        color: #FF8C1A;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    ">
        🗄️ SQL Queries &amp; Analytics
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption("Explore cricket data using 25 predefined MySQL queries.")


# ---------------- SQL QUERIES ----------------

QUERIES = {
    "1. Top 10 run scorers": """
        SELECT p.player_name, p.team_name,
               SUM(s.runs) AS total_runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name, p.team_name
        ORDER BY total_runs DESC
        LIMIT 10
    """,

    "2. Top 10 wicket-takers": """
        SELECT p.player_name, p.team_name,
               SUM(s.wickets) AS total_wickets
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name, p.team_name
        ORDER BY total_wickets DESC
        LIMIT 10
    """,

    "3. Players with the most runs in one match": """
        SELECT p.player_name, s.match_id, s.runs
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        ORDER BY s.runs DESC
        LIMIT 10
    """,

    "4. Players with both runs and wickets": """
        SELECT p.player_name,
               SUM(s.runs) AS total_runs,
               SUM(s.wickets) AS total_wickets
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        HAVING SUM(s.runs) > 0 AND SUM(s.wickets) > 0
        ORDER BY total_runs DESC
    """,

    "5. Total runs in the database": """
        SELECT SUM(runs) AS total_runs
        FROM player_match_stats
    """,

    "6. Total wickets in the database": """
        SELECT SUM(wickets) AS total_wickets
        FROM player_match_stats
    """,

    "7. Number of stored matches": """
        SELECT COUNT(*) AS match_count FROM matches
    """,

    "8. Number of players": """
        SELECT COUNT(*) AS player_count FROM players
    """,

    "9. Matches by category": """
        SELECT match_type, COUNT(*) AS match_count
        FROM matches
        GROUP BY match_type
        ORDER BY match_count DESC
    """,

    "10. Matches by series": """
        SELECT series_name, COUNT(*) AS match_count
        FROM matches
        GROUP BY series_name
        ORDER BY match_count DESC
    """,

    "11. Matches by venue": """
        SELECT venue, COUNT(*) AS match_count
        FROM matches
        GROUP BY venue
        ORDER BY match_count DESC
    """,

    "12. Matches by status": """
        SELECT match_status, COUNT(*) AS match_count
        FROM matches
        GROUP BY match_status
        ORDER BY match_count DESC
    """,

    "13. Players by team": """
        SELECT team_name, COUNT(*) AS player_count
        FROM players
        WHERE team_name IS NOT NULL AND team_name <> ''
        GROUP BY team_name
        ORDER BY player_count DESC
    """,

    "14. Highest strike rates (minimum 50 balls)": """
        SELECT p.player_name,
               SUM(s.runs) AS runs,
               SUM(s.balls_faced) AS balls,
               ROUND(SUM(s.runs) * 100.0 /
                     NULLIF(SUM(s.balls_faced), 0), 2) AS strike_rate
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        HAVING SUM(s.balls_faced) >= 50
        ORDER BY strike_rate DESC
        LIMIT 10
    """,

    "15. Players with most balls faced": """
        SELECT p.player_name, SUM(s.balls_faced) AS balls_faced
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY balls_faced DESC
        LIMIT 10
    """,

    "16. Players with most fours and sixes unavailable": """
        SELECT p.player_name, SUM(s.runs) AS total_runs,
               SUM(s.balls_faced) AS balls_faced
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC
        LIMIT 10
    """,

    "17. Bowling runs conceded": """
        SELECT p.player_name,
               SUM(s.runs_conceded) AS runs_conceded
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY runs_conceded DESC
        LIMIT 10
    """,

    "18. Players with the most matches recorded": """
        SELECT p.player_name,
               COUNT(DISTINCT s.match_id) AS matches_recorded
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY matches_recorded DESC
        LIMIT 10
    """,

    "19. Average runs per player record": """
        SELECT ROUND(AVG(runs), 2) AS average_runs
        FROM player_match_stats
    """,

    "20. Average wickets per player record": """
        SELECT ROUND(AVG(wickets), 2) AS average_wickets
        FROM player_match_stats
    """,

    "21. Matches involving a selected team (all teams)": """
        SELECT match_id, series_name, team1, team2, match_status
        FROM matches
        ORDER BY match_id DESC
    """,

    "22. Players with zero recorded runs": """
        SELECT p.player_name, p.team_name
        FROM players p
        LEFT JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name, p.team_name
        HAVING COALESCE(SUM(s.runs), 0) = 0
        ORDER BY p.player_name
    """,

    "23. Players with zero recorded wickets": """
        SELECT p.player_name, p.team_name
        FROM players p
        LEFT JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name, p.team_name
        HAVING COALESCE(SUM(s.wickets), 0) = 0
        ORDER BY p.player_name
    """,

    "24. Match statistics by match ID": """
        SELECT match_id,
               COUNT(*) AS player_records,
               SUM(runs) AS total_player_runs,
               SUM(wickets) AS recorded_wickets
        FROM player_match_stats
        GROUP BY match_id
        ORDER BY total_player_runs DESC
    """,

    "25. Player performance summary": """
        SELECT p.player_name,
               COUNT(DISTINCT s.match_id) AS matches_recorded,
               SUM(s.runs) AS total_runs,
               SUM(s.wickets) AS total_wickets,
               SUM(s.balls_faced) AS balls_faced
        FROM players p
        JOIN player_match_stats s ON p.player_id = s.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC
        LIMIT 25
    """,
}


# ---------------- QUERY SELECTOR ----------------

st.info(
    f"Available queries: {len(QUERIES)}. "
    "Results depend on the data stored in your database."
)

selected_query = st.selectbox(
    "Choose an SQL query",
    list(QUERIES.keys()),
)

sql = QUERIES[selected_query].strip()

st.subheader("SQL Query")
st.code(sql, language="sql")


# ---------------- EXECUTE QUERY ----------------

if st.button("▶️ Run SQL Query", type="primary"):
    connection = get_connection()

    if connection is None:
        st.error("Could not connect to MySQL.")
    else:
        try:
            with st.spinner("Executing SQL query..."):
                result = pd.read_sql(sql, connection)

            st.session_state["sql_result"] = result
            st.session_state["sql_query_name"] = selected_query

            st.success(
                f"Query completed: {len(result)} rows returned."
            )

        except Exception as error:
            st.error(f"SQL query failed: {error}")

        finally:
            connection.close()


# ---------------- QUERY RESULTS ----------------

if "sql_result" in st.session_state:
    result = st.session_state["sql_result"]

    st.subheader("📊 Query Results")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Results as CSV",
        data=csv_data,
        file_name="cricbuzz_sql_results.csv",
        mime="text/csv",
    )


# ---------------- FOOTER ----------------

st.caption(
    "Note: Some detailed batting fields, such as fours and sixes, "
    "are not stored in the current player_match_stats table."
)
