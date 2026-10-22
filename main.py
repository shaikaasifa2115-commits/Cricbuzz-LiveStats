
import streamlit as st
import pandas as pd

from database import get_connection
from scorecard_service import get_scorecard


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
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

    div[data-testid="stMetric"] {
        background-color: #1C2028;
        border: 1px solid #343A46;
        border-radius: 10px;
        padding: 14px;
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

    div[data-testid="stDataFrame"] {
        border: 1px solid #343A46;
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #343A46;
        border-radius: 10px;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"]:focus-within {
        border-color: #FF7A00;
    }

    a {
        color: #FF9A3D !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- LOAD MATCHES ----------------

@st.cache_data(ttl=30)
def load_matches():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
            SELECT match_id, series_name, match_type,
                   match_description, team1, team2,
                   venue, city, match_status
            FROM matches
            ORDER BY match_id DESC
        """
        return pd.read_sql(query, connection)

    except Exception as error:
        print(f"Could not load matches: {error}")
        return None

    finally:
        connection.close()


# ---------------- SCORECARD DISPLAY ----------------

def show_scorecard(data):
    if not data:
        st.error("Could not retrieve the scorecard.")
        return

    st.subheader("Match Status")
    st.info(data.get("status", "Status unavailable"))

    innings_list = data.get("scorecard", [])

    if not isinstance(innings_list, list) or not innings_list:
        st.warning("No innings scorecard is available.")
        return

    for index, innings in enumerate(innings_list, start=1):
        if not isinstance(innings, dict):
            continue

        team = innings.get("batteamname", f"Innings {index}")
        runs = innings.get("score", 0)
        wickets = innings.get("wickets", 0)
        overs = innings.get("overs", 0)
        run_rate = innings.get("runrate", 0)

        with st.expander(
            f"{team} — {runs}/{wickets} ({overs} overs)",
            expanded=(index == 1),
        ):
            c1, c2, c3 = st.columns(3)
            c1.metric("Runs / Wickets", f"{runs}/{wickets}")
            c2.metric("Overs", overs)
            c3.metric("Run Rate", run_rate)

            st.markdown("#### Batting")
            batsmen = innings.get("batsman", [])

            if batsmen:
                batting_rows = [
                    {
                        "Batter": p.get("name", ""),
                        "Runs": p.get("runs", 0),
                        "Balls": p.get("balls", 0),
                        "Fours": p.get("fours", 0),
                        "Sixes": p.get("sixes", 0),
                        "Strike Rate": p.get("strkrate", 0),
                        "Dismissal": p.get("outdec", ""),
                    }
                    for p in batsmen
                ]

                st.dataframe(
                    pd.DataFrame(batting_rows),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.write("Batting details unavailable.")

            st.markdown("#### Bowling")
            bowlers = innings.get("bowler", [])

            if bowlers:
                bowling_rows = [
                    {
                        "Bowler": p.get("name", ""),
                        "Overs": p.get("overs", 0),
                        "Maidens": p.get("maidens", 0),
                        "Runs": p.get("runs", 0),
                        "Wickets": p.get("wickets", 0),
                        "Economy": p.get("economy", 0),
                    }
                    for p in bowlers
                ]

                st.dataframe(
                    pd.DataFrame(bowling_rows),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.write("Bowling details unavailable.")

            extras = innings.get("extras", {})

            if isinstance(extras, dict):
                st.markdown("#### Extras")
                st.write(
                    f"Total: {extras.get('total', 0)} "
                    f"| Wides: {extras.get('wides', 0)} "
                    f"| No-balls: {extras.get('noballs', 0)} "
                    f"| Byes: {extras.get('byes', 0)} "
                    f"| Leg-byes: {extras.get('legbyes', 0)}"
                )


# ---------------- HOME PAGE ----------------

def show_home_page():
    st.markdown(
        """
        <h1 style="
            color: #FF8C1A;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        ">
            🏏 Cricbuzz LiveStats
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Cricket analytics powered by Cricbuzz API, Python, "
        "Streamlit, and MySQL."
    )

    st.markdown(
        """
        Welcome to **Cricbuzz LiveStats**!

        Explore cricket matches, inspect scorecards, analyze player
        performance, execute SQL queries, and manage player records
        through one interactive dashboard.
        """
    )

    matches = load_matches()

    if matches is None:
        st.error("Could not connect to MySQL. Check your database settings.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Matches in Database", len(matches))
        c2.metric("Match Categories", matches["match_type"].nunique())
        c3.metric("Series", matches["series_name"].nunique())

    st.divider()
    st.subheader("🎯 Project Objectives")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            - Retrieve cricket match information from an API.
            - Display scorecards and player performances.
            - Store cricket data in MySQL.
            """
        )

    with c2:
        st.markdown(
            """
            - Analyze batting and bowling statistics.
            - Execute SQL analytics queries.
            - Manage player records through CRUD operations.
            """
        )

    st.divider()
    st.subheader("🧰 Technologies Used")

    c1, c2, c3, c4 = st.columns(4)
    c1.info("**Python**\n\nApplication logic")
    c2.info("**Streamlit**\n\nDashboard")
    c3.info("**MySQL**\n\nDatabase")
    c4.info("**Cricbuzz API**\n\nCricket data")

    st.divider()
    st.subheader("📌 Project Features")

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            st.markdown("### 🏏 Live Match")
            st.write("Search matches and view available scorecards.")

        with st.container(border=True):
            st.markdown("### 🗄️ SQL Analytics")
            st.write("Run SQL queries and download their results.")

    with c2:
        with st.container(border=True):
            st.markdown("### 📊 Top Player Stats")
            st.write("Explore run scorers and wicket-takers.")

        with st.container(border=True):
            st.markdown("### ✏️ CRUD Operations")
            st.write("Create, view, update, and delete player records.")

    st.divider()
    st.subheader("🗂️ Project Structure")

    st.code(
        """
Cricbuzz-LiveStats/
├── main.py
├── database.py
├── api_service.py
├── scorecard_service.py
├── player_stats_service.py
├── sync_matches.py
├── sync_all_player_stats.py
├── requirements.txt
├── README.md
├── SQL_Queries_Documentation.md
├── schema.sql
├── cricbuzz_livestats.sql
└── dashboard_pages/
    ├── 2_Top_Player_Stats.py
    ├── 3_SQL_Analytics.py
    └── 4_CRUD_Operations.py
        """,
        language="text",
    )

    st.info(
        "Keep your .env file private. Never publish API keys or passwords."
    )

    st.subheader("🚀 How to Run")

    st.code(
        "pip install -r requirements.txt\n"
        "python sync_matches.py\n"
        "python sync_all_player_stats.py\n"
        "streamlit run main.py",
        language="powershell",
    )

    st.caption(
        "Statistics cover matches synchronized into your database."
    )


# ---------------- LIVE MATCH PAGE ----------------

def show_match_dashboard():
    st.markdown(
        """
        <h1 style="
            color: #FF8C1A;
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        ">
            🏏 Live Match Explorer
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Browse matches and view their available scorecards.")

    matches = load_matches()

    if matches is None:
        st.error("Could not connect to MySQL. Check your database settings.")
        return

    if matches.empty:
        st.warning("No matches found. Run python sync_matches.py first.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Matches in Database", len(matches))
    c2.metric("Match Categories", matches["match_type"].nunique())
    c3.metric("Series", matches["series_name"].nunique())

    st.divider()

    f1, f2, f3 = st.columns(3)

    with f1:
        search = st.text_input(
            "Search matches",
            placeholder="Search team, series, or status...",
        )

    with f2:
        categories = sorted(
            matches["match_type"].dropna().unique().tolist()
        )
        category = st.selectbox("Match category", ["All"] + categories)

    with f3:
        teams = sorted(
            set(matches["team1"].dropna().tolist())
            | set(matches["team2"].dropna().tolist())
        )
        team = st.selectbox("Team", ["All"] + teams)

    filtered = matches.copy()

    if search:
        mask = filtered.astype(str).apply(
            lambda column: column.str.contains(
                search, case=False, na=False, regex=False
            )
        ).any(axis=1)
        filtered = filtered[mask]

    if category != "All":
        filtered = filtered[filtered["match_type"] == category]

    if team != "All":
        filtered = filtered[
            (filtered["team1"] == team) | (filtered["team2"] == team)
        ]

    st.caption(f"Showing {len(filtered)} of {len(matches)} matches")

    st.dataframe(
        filtered[
            [
                "match_id",
                "series_name",
                "match_type",
                "match_description",
                "team1",
                "team2",
                "venue",
                "city",
                "match_status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("🏏 Match Scorecard")

    options = {}

    for _, row in matches.iterrows():
        label = (
            f"{row['team1']} vs {row['team2']} | "
            f"{row['match_description']} | ID: {row['match_id']}"
        )
        options[label] = row["match_id"]

    selected = st.selectbox("Choose a match", list(options.keys()))

    if st.button("View Scorecard", type="primary"):
        with st.spinner("Fetching scorecard from Cricbuzz..."):
            data = get_scorecard(options[selected])

        if data is None:
            st.error("Unable to fetch this match's scorecard.")
        else:
            show_scorecard(data)

    if st.button("🔄 Refresh Database Data"):
        load_matches.clear()
        st.rerun()


# ---------------- REGISTER PAGES ----------------

home = st.Page(
    show_home_page,
    title="Home",
    icon="🏠",
    default=True,
)

live = st.Page(
    show_match_dashboard,
    title="Live Match",
    icon="🏏",
)

top_stats = st.Page(
    "dashboard_pages/2_Top_Player_Stats.py",
    title="Top Player Stats",
    icon="📊",
)

sql_analytics = st.Page(
    "dashboard_pages/3_SQL_Analytics.py",
    title="SQL Analytics",
    icon="🗄️",
)

crud = st.Page(
    "dashboard_pages/4_CRUD_Operations.py",
    title="CRUD Operations",
    icon="✏️",
)

navigation = st.navigation(
    {
        "Cricbuzz LiveStats": [
            home,
            live,
            top_stats,
            sql_analytics,
            crud,
        ]
    }
)

navigation.run()
