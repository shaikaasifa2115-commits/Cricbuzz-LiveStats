# 🏏 Cricbuzz LiveStats

## 1. Project Overview

Cricbuzz LiveStats is a cricket analytics dashboard developed using Python, Streamlit, MySQL, and the Cricbuzz Cricket API through RapidAPI.

The application retrieves cricket match information, displays available scorecards, analyzes player statistics, executes SQL queries, and provides CRUD operations for managing player records.

## 2. Objectives

- Display available cricket match information.
- View available match scorecards and batting and bowling statistics.
- Analyze player performance using statistical summaries.
- Perform SQL-based cricket data analysis.
- Create, view, update, and delete player records.
- Store match and player statistics in MySQL.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web dashboard |
| MySQL | Relational database |
| Cricbuzz Cricket API | Match and scorecard data |
| RapidAPI | API access and authentication |
| Pandas | Data processing and tables |
| mysql-connector-python | Python–MySQL connectivity |
| python-dotenv | Environment variable management |

## 4. Project Features

### Home

- Displays project objectives and technologies.
- Shows database summary metrics.
- Provides project structure information and run commands.

### Live Match Dashboard

- Browse available matches.
- Search and filter matches by team and category.
- View match status, teams, series, and venue.
- View available scorecards and batting and bowling details.

### Top Player Statistics

- Analyze recorded runs and wickets.
- View top run scorers and wicket-takers.
- Explore player performance summaries.
- Filter statistics by team when team information is available.

### SQL Analytics

- Execute 25 predefined SQL queries.
- Explore cricket data using MySQL.
- Display query results in tables.
- Download query results as CSV files.
- Refer to `SQL_Queries_Documentation.md` for explanations of all 25 predefined queries and the SQL concepts used.

### CRUD Operations

- Create player records.
- View and search player records.
- Update player information.
- Delete player records with confirmation.
- Display operation success messages.

## 5. Project Structure

```text
Cricbuzz-LiveStats/
├── main.py
├── database.py
├── api_service.py
├── scorecard_service.py
├── player_stats_service.py
├── sync_matches.py
├── sync_all_player_stats.py
├── test_api.py
├── test_db.py
├── requirements.txt
├── README.md
├── SQL_Queries_Documentation.md
├── schema.sql
├── cricbuzz_livestats.sql
├── .env
├── .gitignore
├── venv/
└── dashboard_pages/
    ├── 2_Top_Player_Stats.py
    ├── 3_SQL_Analytics.py
    └── 4_CRUD_Operations.py
```

**Note:** The `venv/` folder contains the local Python environment. It should not be uploaded to GitHub. The `.env` file contains private credentials and must also be excluded.

## 6. Prerequisites

- Python compatible with the packages in `requirements.txt`.
- MySQL Server 8.0 or a compatible version.
- Visual Studio Code (recommended).
- A RapidAPI account with access to the Cricbuzz Cricket API.

## 7. Installation

Open the project folder in VS Code.

Create and activate a virtual environment in Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If the virtual environment already exists, activate it rather than creating another one.

## 8. Environment Configuration

Create a `.env` file in the project root directory with the following settings:

```env
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
MYSQL_PASSWORD=your_mysql_password
```

Replace the placeholders with your own credentials. Never publish your API key or database password.

## 9. Database Configuration

Create the database in MySQL if it does not already exist:

```sql
CREATE DATABASE cricbuzz_livestats;
```

The application connects to the local MySQL server using `database.py` and the password configured in `.env`.

The project database includes these tables:

- `matches` — match information.
- `players` — player information.
- `player_match_stats` — player performance by match.
- `venues` — venue information.
- `teams` — team information.

The `schema.sql` file contains the database structure. The `cricbuzz_livestats.sql` file is a database dump that can be used for backup or restoration.

Import the SQL dump only when needed. Importing it into an existing database may cause conflicts or affect existing data, depending on the dump's contents.

## 10. Synchronizing Data

To retrieve and save match information:

```powershell
python sync_matches.py
```

To retrieve scorecards and synchronize player statistics for stored matches:

```powershell
python sync_all_player_stats.py
```

Data collection depends on API availability, subscription limits, and the matches returned by the API.

## 11. Running the Application

Activate the virtual environment and run:

```powershell
streamlit run main.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

Use the sidebar to navigate between Home, Live Match, Top Player Stats, SQL Analytics, and CRUD Operations.

## 12. Testing

Test API connectivity:

```powershell
python test_api.py
```

Test MySQL connectivity:

```powershell
python test_db.py
```

Verify the dashboard by checking match browsing, scorecard retrieval, player statistics, SQL query execution, CSV downloads, and CRUD operations.

## 13. Data and Limitations

- Match and scorecard availability depends on the external API.
- Player statistics cover the matches synchronized into the database.
- Rankings may not represent a complete tournament or season.
- Some player or team information may be missing from API responses.
- API request limits may affect synchronization.
- Detailed batting fields that are not stored in the database cannot be included in database-based analytics.

## 14. Future Enhancements

- Schedule automatic data synchronization.
- Improve player profiles and team-level analytics.
- Add more visualizations for batting and bowling performance.
- Improve error logging and API retry handling.
- Add authentication and role-based access.
- Support historical tournament comparisons.

## 15. Conclusion

Cricbuzz LiveStats demonstrates the integration of Python, Streamlit, MySQL, external API data, and SQL analytics in a cricket-focused dashboard. It combines match exploration, scorecard viewing, player performance analysis, database queries, and CRUD functionality in a single application.
