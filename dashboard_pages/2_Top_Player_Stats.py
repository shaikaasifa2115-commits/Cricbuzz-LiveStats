
import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(
    page_title="Top Player Stats | Cricbuzz LiveStats",
    page_icon="📊",
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

    div[data-testid="stMetric"] {
        background-color: #1C2028;
        border: 1px solid #343A46;
        border-radius: 10px;
        padding: 14px;
    }

    div[data-testid="stAlert"] {
        border-left: 4px solid #FF7A00;
        border-radius: 8px;
    }

    div.stButton > button[kind="primary"],
    div.stDownloadButton > button {
        background-color: #FF7A00;
        color: #FFFFFF;
        border: 1px solid #FF7A00;
        border-radius: 8px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover,
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
        📊 Top Player Statistics
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Explore batting and bowling performance from synchronized matches."
)


# ---------------- LOAD PLAYER STATISTICS ----------------

@st.cache_data(ttl=60)
def load_player_stats():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
            SELECT
                p.player_id,
                p.player_name,
                p.team_name,
                COUNT(DISTINCT s.match_id) AS matches,
                COALESCE(SUM(s.runs), 0) AS total_runs,
                COALESCE(SUM(s.balls_faced), 0) AS balls_faced,
                COALESCE(SUM(s.wickets), 0) AS total_wickets,
                COALESCE(SUM(s.runs_conceded), 0) AS runs_conceded,
                CASE
                    WHEN SUM(s.balls_faced) > 0
                    THEN ROUND(
                        SUM(s.runs) * 100.0 / SUM(s.balls_faced), 2
                    )
                    ELSE 0
                END AS strike_rate
            FROM players p
            LEFT JOIN player_match_stats s
                ON p.player_id = s.player_id
            GROUP BY
                p.player_id,
                p.player_name,
                p.team_name
            ORDER BY total_runs DESC
        """

        return pd.read_sql(query, connection)

    except Exception as error:
        st.error(f"Could not load player statistics: {error}")
        return None

    finally:
        connection.close()


# ---------------- DISPLAY STATISTICS ----------------

stats = load_player_stats()

if stats is None:
    st.error("Unable to load statistics. Check your MySQL connection.")

elif stats.empty:
    st.info("No player statistics are available yet.")

else:
    team_options = sorted(
        stats["team_name"].dropna().unique().tolist()
    )

    selected_team = st.selectbox(
        "Filter by team",
        ["All Teams"] + team_options,
    )

    filtered = stats.copy()

    if selected_team != "All Teams":
        filtered = filtered[
            filtered["team_name"] == selected_team
        ]

    total_players = len(filtered)
    total_runs = int(filtered["total_runs"].sum())
    total_wickets = int(filtered["total_wickets"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Players", total_players)
    col2.metric("Total Runs", f"{total_runs:,}")
    col3.metric("Total Wickets", total_wickets)

    st.divider()

    # ---------------- TOP RUN SCORERS ----------------

    st.subheader("🏏 Top Run Scorers")

    top_runs = filtered.sort_values(
        "total_runs", ascending=False
    ).head(10)

    st.dataframe(
        top_runs[
            [
                "player_name",
                "team_name",
                "matches",
                "total_runs",
                "balls_faced",
                "strike_rate",
            ]
        ].rename(
            columns={
                "player_name": "Player",
                "team_name": "Team",
                "matches": "Matches",
                "total_runs": "Runs",
                "balls_faced": "Balls Faced",
                "strike_rate": "Strike Rate",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ---------------- TOP WICKET-TAKERS ----------------

    st.subheader("🎯 Top Wicket-Takers")

    top_wickets = filtered.sort_values(
        ["total_wickets", "runs_conceded"],
        ascending=[False, True],
    ).head(10)

    st.dataframe(
        top_wickets[
            [
                "player_name",
                "team_name",
                "matches",
                "total_wickets",
                "runs_conceded",
            ]
        ].rename(
            columns={
                "player_name": "Player",
                "team_name": "Team",
                "matches": "Matches",
                "total_wickets": "Wickets",
                "runs_conceded": "Runs Conceded",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ---------------- ALL PLAYER STATISTICS ----------------

    st.subheader("📋 All Player Statistics")

    st.dataframe(
        filtered.sort_values(
            "total_runs", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )

    # ---------------- CSV DOWNLOAD ----------------

    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Player Statistics CSV",
        data=csv_data,
        file_name="player_statistics.csv",
        mime="text/csv",
    )

    # ---------------- REFRESH ----------------

    if st.button("🔄 Refresh Player Statistics"):
        load_player_stats.clear()
        st.rerun()

    st.caption(
        "Statistics cover the matches stored in your database, "
        "not necessarily an entire tournament or season."
    )
