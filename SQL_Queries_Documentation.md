# Cricbuzz LiveStats — SQL Queries Documentation

## 1. Project Overview

Cricbuzz LiveStats is a cricket statistics application built using Python, Streamlit, MySQL, Pandas, and the Cricbuzz API.

The SQL Analytics module provides 25 predefined MySQL queries to analyze match information, player performance, runs, wickets, strike rates, and other cricket statistics.

## 2. Database Tables Used

| Table | Purpose |
|---|---|
| `matches` | Stores match details, teams, series, venue, category, and status. |
| `players` | Stores player names, teams, roles, and playing information. |
| `player_match_stats` | Stores player statistics recorded for individual matches. |
| `teams` | Stores team information. |
| `venues` | Stores venue information. |

The 25 queries primarily use the `matches`, `players`, and `player_match_stats` tables.

## 3. SQL Queries

### Query 1: Top 10 Run Scorers

**Purpose:** Displays the top 10 players with the highest total recorded runs.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 2: Top 10 Wicket-Takers

**Purpose:** Displays the top 10 players with the highest total recorded wickets.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 3: Players with the Most Runs in One Match

**Purpose:** Lists the 10 highest individual player-match run records, along with player names and match IDs.

**SQL concepts:** `JOIN`, `ORDER BY`, `LIMIT`.

### Query 4: Players with Both Runs and Wickets

**Purpose:** Finds players whose recorded totals include both runs and wickets, ordered by total runs.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `HAVING`, `AND`, `ORDER BY`.

### Query 5: Total Runs in the Database

**Purpose:** Calculates the sum of runs recorded in `player_match_stats`.

**SQL concepts:** `SUM()`.

### Query 6: Total Wickets in the Database

**Purpose:** Calculates the sum of wickets recorded in `player_match_stats`.

**SQL concepts:** `SUM()`.

### Query 7: Number of Stored Matches

**Purpose:** Counts the records in the `matches` table.

**SQL concepts:** `COUNT()`.

### Query 8: Number of Players

**Purpose:** Counts the records in the `players` table.

**SQL concepts:** `COUNT()`.

### Query 9: Matches by Category

**Purpose:** Counts stored matches for each match type and sorts the categories by match count.

**SQL concepts:** `GROUP BY`, `COUNT()`, `ORDER BY`.

### Query 10: Matches by Series

**Purpose:** Counts the matches recorded for each series.

**SQL concepts:** `GROUP BY`, `COUNT()`, `ORDER BY`.

### Query 11: Matches by Venue

**Purpose:** Counts matches associated with each venue.

**SQL concepts:** `GROUP BY`, `COUNT()`, `ORDER BY`.

### Query 12: Matches by Status

**Purpose:** Counts matches for each recorded match status.

**SQL concepts:** `GROUP BY`, `COUNT()`, `ORDER BY`.

### Query 13: Players by Team

**Purpose:** Counts players assigned to each non-empty team name.

**SQL concepts:** `WHERE`, `IS NOT NULL`, `GROUP BY`, `COUNT()`, `ORDER BY`.

### Query 14: Highest Strike Rates (Minimum 50 Balls)

**Purpose:** Calculates the aggregate strike rate for players with at least 50 recorded balls faced and returns the top 10.

**SQL concepts:** `JOIN`, `SUM()`, `ROUND()`, `NULLIF()`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.

**Formula:**

Strike Rate = (Total Runs / Total Balls Faced) × 100

`NULLIF()` prevents division by zero.

### Query 15: Players with the Most Balls Faced

**Purpose:** Lists the top 10 players by total recorded balls faced.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 16: Players with Most Fours and Sixes Unavailable

**Purpose:** Lists players by total runs and displays their recorded balls faced.

**Important limitation:** The current database does not store separate fours and sixes fields. Therefore, this query does not calculate fours or sixes; it uses runs and balls faced as available statistics.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 17: Bowling Runs Conceded

**Purpose:** Displays the top 10 players by total recorded bowling runs conceded.

**SQL concepts:** `JOIN`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 18: Players with the Most Matches Recorded

**Purpose:** Finds the top 10 players with the highest number of distinct matches represented in the statistics table.

**SQL concepts:** `JOIN`, `COUNT(DISTINCT ...)`, `GROUP BY`, `ORDER BY`, `LIMIT`.

### Query 19: Average Runs per Player Record

**Purpose:** Calculates the average runs value across all rows in `player_match_stats`.

**SQL concepts:** `AVG()`, `ROUND()`.

### Query 20: Average Wickets per Player Record

**Purpose:** Calculates the average wickets value across all rows in `player_match_stats`.

**SQL concepts:** `AVG()`, `ROUND()`.

### Query 21: Matches Involving a Selected Team (All Teams)

**Purpose:** Displays match IDs, series names, both teams, and match statuses, ordered by match ID.

**Important limitation:** Despite the query's label, the current SQL statement does not filter by a selected team. It returns all stored matches.

**SQL concepts:** `SELECT`, `ORDER BY`.

### Query 22: Players with Zero Recorded Runs

**Purpose:** Finds players whose total recorded runs are zero, including players without matching statistics records.

**SQL concepts:** `LEFT JOIN`, `GROUP BY`, `COALESCE()`, `SUM()`, `HAVING`, `ORDER BY`.

### Query 23: Players with Zero Recorded Wickets

**Purpose:** Finds players whose total recorded wickets are zero, including players without matching statistics records.

**SQL concepts:** `LEFT JOIN`, `GROUP BY`, `COALESCE()`, `SUM()`, `HAVING`, `ORDER BY`.

### Query 24: Match Statistics by Match ID

**Purpose:** Groups player statistics by match ID and displays the number of player-stat records, total recorded runs, and recorded wickets for each match.

**SQL concepts:** `GROUP BY`, `COUNT()`, `SUM()`, `ORDER BY`.

### Query 25: Player Performance Summary

**Purpose:** Summarizes each player's distinct recorded matches, total runs, total wickets, and balls faced. It returns the top 25 players ordered by total runs.

**SQL concepts:** `JOIN`, `COUNT(DISTINCT ...)`, `SUM()`, `GROUP BY`, `ORDER BY`, `LIMIT`.

## 4. SQL Concepts Demonstrated

| SQL concept | Explanation |
|---|---|
| `SELECT` | Retrieves data from database tables. |
| `JOIN` | Combines related records from tables. |
| `LEFT JOIN` | Preserves all rows from the left table, including rows without a match. |
| `WHERE` | Filters rows before grouping. |
| `GROUP BY` | Groups rows for aggregate calculations. |
| `HAVING` | Filters grouped results. |
| `ORDER BY` | Sorts results. |
| `LIMIT` | Restricts the number of returned rows. |
| `COUNT()` | Counts rows or values, depending on the expression. |
| `SUM()` | Calculates a total. |
| `AVG()` | Calculates an average. |
| `ROUND()` | Rounds a numeric value. |
| `COALESCE()` | Replaces a `NULL` result with a specified value. |
| `NULLIF()` | Returns `NULL` when two expressions are equal; useful for avoiding division by zero. |
| `COUNT(DISTINCT ...)` | Counts unique values. |

## 5. How SQL Analytics Works

1. The user opens the SQL Analytics page in Streamlit.
2. The application displays the 25 predefined queries in a dropdown.
3. The user selects a query.
4. The corresponding SQL statement is displayed.
5. When the user clicks **Run SQL Query**, Python obtains a MySQL connection.
6. Pandas executes the query and stores the result in a DataFrame.
7. Streamlit displays the result in a table.
8. The user can download the result as a CSV file.

## 6. Important Limitations

- Results depend on the data currently stored in MySQL.
- The player statistics represent the matches that have been synchronized, not necessarily every match in a complete season.
- The database does not currently store separate fours and sixes values.
- Some player team information may be incomplete.
- Query 21 currently lists all matches rather than filtering by a selected team.
- Average runs and wickets are calculated per statistics-table row, not per complete player career.
- Aggregated statistics should be interpreted according to the available data and its completeness.

## 7. Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- MySQL Connector/Python
- Cricbuzz API

## 8. Conclusion

The SQL Analytics module demonstrates the use of SQL retrieval, joins, filtering, grouping, aggregate functions, sorting, and result limiting to analyze cricket match and player data. It integrates MySQL queries with a Streamlit interface and supports exporting query results to CSV.
