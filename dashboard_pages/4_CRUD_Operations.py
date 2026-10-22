
import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(
    page_title="CRUD Operations | Cricbuzz LiveStats",
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
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #FF7A00;
        color: #FFFFFF;
        border: 1px solid #FF7A00;
        border-radius: 8px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background-color: #E66D00;
        border-color: #E66D00;
        color: #FFFFFF;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #343A46;
        border-radius: 8px;
        overflow: hidden;
    }

    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"]:focus-within {
        border-color: #FF7A00;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #FF8C1A;
        border-bottom-color: #FF7A00;
    }

    div[data-testid="stForm"] {
        border: 1px solid #343A46;
        border-radius: 10px;
        padding: 18px;
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
        🏏 Player CRUD Operations
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption("Create, view, update, and delete player records in MySQL.")


# ---------------- SUCCESS MESSAGE ----------------

if "crud_success" in st.session_state:
    st.success(st.session_state["crud_success"])
    del st.session_state["crud_success"]


# ---------------- DATABASE HELPERS ----------------

def fetch_players():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Could not connect to MySQL.")

    try:
        query = """
            SELECT player_id, player_name, team_name, role,
                   batting_style, bowling_style, country
            FROM players
            ORDER BY player_name
        """
        return pd.read_sql(query, connection)
    finally:
        connection.close()


def run_write_query(query, values):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Could not connect to MySQL.")

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# ---------------- LOAD PLAYER DATA ----------------

try:
    players_df = fetch_players()
except Exception as error:
    st.error(f"Unable to load players: {error}")
    st.stop()


st.metric("Players in Database", len(players_df))

st.divider()


# ---------------- CRUD TABS ----------------

tab_view, tab_add, tab_edit, tab_delete = st.tabs(
    [
        "📋 View Players",
        "➕ Add Player",
        "✏️ Edit Player",
        "🗑️ Delete Player",
    ]
)


# ---------------- VIEW PLAYERS ----------------

with tab_view:
    st.subheader("All Player Records")

    search = st.text_input(
        "Search players",
        placeholder="Enter a player name or team",
        key="player_search",
    )

    displayed = players_df.copy()

    if search.strip():
        mask = (
            displayed["player_name"].fillna("").str.contains(
                search, case=False, regex=False
            )
            | displayed["team_name"].fillna("").str.contains(
                search, case=False, regex=False
            )
        )
        displayed = displayed[mask]

    st.write(f"Showing {len(displayed)} player records.")

    st.dataframe(
        displayed,
        use_container_width=True,
        hide_index=True,
    )


# ---------------- ADD PLAYER ----------------

with tab_add:
    st.subheader("Add a New Player")

    with st.form("add_player_form", clear_on_submit=True):
        player_name = st.text_input("Player Name *")
        team_name = st.text_input("Team Name")

        role = st.selectbox(
            "Role",
            ["Unknown", "Batter", "Bowler", "All-rounder", "Wicketkeeper"],
        )

        batting_style = st.text_input("Batting Style")
        bowling_style = st.text_input("Bowling Style")
        country = st.text_input("Country")

        add_submitted = st.form_submit_button(
            "Add Player",
            type="primary",
        )

    if add_submitted:
        if not player_name.strip():
            st.warning("Player name is required.")
        else:
            connection = get_connection()

            if connection is None:
                st.error("Could not connect to MySQL.")
            else:
                cursor = None

                try:
                    cursor = connection.cursor()

                    # Generate an ID for a manually added player.
                    cursor.execute(
                        """
                        SELECT COALESCE(MAX(player_id), 0) + 1
                        FROM players
                        """
                    )
                    new_player_id = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO players
                        (
                            player_id, player_name, team_name, role,
                            batting_style, bowling_style, country
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            new_player_id,
                            player_name.strip(),
                            team_name.strip() or None,
                            None if role == "Unknown" else role,
                            batting_style.strip() or None,
                            bowling_style.strip() or None,
                            country.strip() or None,
                        ),
                    )

                    connection.commit()

                    st.session_state["crud_success"] = (
                        f"Player '{player_name.strip()}' added successfully!"
                    )
                    st.rerun()

                except Exception as error:
                    connection.rollback()
                    st.error(f"Could not add player: {error}")

                finally:
                    if cursor is not None:
                        cursor.close()
                    connection.close()


# ---------------- EDIT PLAYER ----------------

with tab_edit:
    st.subheader("Edit an Existing Player")

    if players_df.empty:
        st.info("There are no player records to edit.")
    else:
        player_options = {
            f"{row.player_name} (ID: {row.player_id})": int(row.player_id)
            for row in players_df.itertuples(index=False)
        }

        selected_label = st.selectbox(
            "Select a player",
            list(player_options.keys()),
            key="edit_player_selection",
        )

        selected_id = player_options[selected_label]

        selected_row = players_df[
            players_df["player_id"] == selected_id
        ].iloc[0]

        with st.form("edit_player_form"):
            edit_name = st.text_input(
                "Player Name *",
                value=str(selected_row["player_name"] or ""),
            )
            edit_team = st.text_input(
                "Team Name",
                value=str(selected_row["team_name"] or ""),
            )
            edit_role = st.text_input(
                "Role",
                value=str(selected_row["role"] or ""),
            )
            edit_batting = st.text_input(
                "Batting Style",
                value=str(selected_row["batting_style"] or ""),
            )
            edit_bowling = st.text_input(
                "Bowling Style",
                value=str(selected_row["bowling_style"] or ""),
            )
            edit_country = st.text_input(
                "Country",
                value=str(selected_row["country"] or ""),
            )

            edit_submitted = st.form_submit_button(
                "Save Changes",
                type="primary",
            )

        if edit_submitted:
            if not edit_name.strip():
                st.warning("Player name cannot be empty.")
            else:
                try:
                    changed = run_write_query(
                        """
                        UPDATE players
                        SET player_name = %s,
                            team_name = %s,
                            role = %s,
                            batting_style = %s,
                            bowling_style = %s,
                            country = %s
                        WHERE player_id = %s
                        """,
                        (
                            edit_name.strip(),
                            edit_team.strip() or None,
                            edit_role.strip() or None,
                            edit_batting.strip() or None,
                            edit_bowling.strip() or None,
                            edit_country.strip() or None,
                            selected_id,
                        ),
                    )

                    if changed:
                        st.session_state["crud_success"] = (
                            f"Player '{edit_name.strip()}' updated successfully!"
                        )
                    else:
                        st.session_state["crud_success"] = (
                            "No changes were made to the player record."
                        )

                    st.rerun()

                except Exception as error:
                    st.error(f"Could not update player: {error}")


# ---------------- DELETE PLAYER ----------------

with tab_delete:
    st.subheader("Delete a Player")

    st.warning(
        "A player cannot be deleted if related match statistics prevent "
        "the deletion. Existing match statistics will not be deleted."
    )

    if players_df.empty:
        st.info("There are no player records to delete.")
    else:
        delete_options = {
            f"{row.player_name} (ID: {row.player_id})": int(row.player_id)
            for row in players_df.itertuples(index=False)
        }

        delete_label = st.selectbox(
            "Select a player to delete",
            list(delete_options.keys()),
            key="delete_player_selection",
        )

        delete_id = delete_options[delete_label]

        confirm_delete = st.checkbox(
            "I understand this will permanently delete the player record.",
            key="confirm_delete_player",
        )

        if st.button("Delete Player", type="primary"):
            if not confirm_delete:
                st.warning("Please confirm before deleting.")
            else:
                try:
                    deleted = run_write_query(
                        "DELETE FROM players WHERE player_id = %s",
                        (delete_id,),
                    )

                    if deleted:
                        st.session_state["crud_success"] = (
                            "Player deleted successfully!"
                        )
                        st.rerun()
                    else:
                        st.warning("No player record was deleted.")

                except Exception as error:
                    st.error(
                        "Could not delete this player. They may have "
                        "related match-stat records. No change was committed. "
                        f"Details: {error}"
                    )
