"""
InnoSphere Database Initialization Script
Executes SQL initialization files in sequence and verifies integrity.
Compatible with MySQL 8.0+
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'atharv@27')
DB_NAME = os.getenv('DB_NAME', 'innosphere_db')

SQL_DIR = os.path.dirname(__file__)

SQL_FILES = [
    '01_create_database.sql',
    '02_create_tables.sql',
    '03_indexes.sql',
    '04_views.sql',
    '05_functions.sql',
    '06_stored_procedures.sql',
    '07_triggers.sql',
    '08_sample_seed_data.sql'
]

def split_sql_statements(content):
    """
    Splits SQL statements handling DELIMITER $$ properly.
    """
    statements = []
    current_delimiter = ';'
    buffer = []

    lines = content.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith('DELIMITER'):
            parts = stripped.split()
            if len(parts) >= 2:
                current_delimiter = parts[1]
            continue
        
        # Check if line ends with current delimiter
        if current_delimiter != ';' and stripped.endswith(current_delimiter):
            # remove delimiter from end
            line_without_delim = line[:line.rfind(current_delimiter)]
            buffer.append(line_without_delim)
            stmt = '\n'.join(buffer).strip()
            if stmt:
                statements.append(stmt)
            buffer = []
        elif current_delimiter == ';' and stripped.endswith(';'):
            line_without_delim = line[:line.rfind(';')]
            buffer.append(line_without_delim)
            stmt = '\n'.join(buffer).strip()
            if stmt:
                statements.append(stmt)
            buffer = []
        else:
            buffer.append(line)

    leftover = '\n'.join(buffer).strip()
    if leftover:
        statements.append(leftover)

    return statements

def run_setup():
    print("=" * 70)
    print(" InnoSphere - Database Initialization & Seed Script")
    print("=" * 70)
    print(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}...")

    # Connect to MySQL server without database first
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("Connected to MySQL Server successfully.")
    except Exception as e:
        print(f"ERROR: Could not connect to MySQL server: {e}")
        sys.exit(1)

    for sql_file in SQL_FILES:
        filepath = os.path.join(SQL_DIR, sql_file)
        if not os.path.exists(filepath):
            print(f"WARNING: File {sql_file} not found. Skipping.")
            continue

        print(f"\n--> Executing: {sql_file}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        statements = split_sql_statements(content)
        success_count = 0
        for stmt in statements:
            stmt = stmt.strip()
            # Skip pure comments or empty strings
            if not stmt or stmt.startswith('--') and '\n' not in stmt:
                continue
            try:
                cursor.execute(stmt)
                success_count += 1
            except mysql.connector.Error as err:
                print(f"   [SQL ERROR in {sql_file}]: {err.msg}")
                print(f"   Statement excerpt: {stmt[:120]}...")
        
        conn.commit()
        print(f"   Completed: {success_count} statements executed.")

    # Verification Step
    print("\n" + "=" * 70)
    print(" Verifying Database Tables, Views, Functions & Procedures")
    print("=" * 70)

    cursor.execute("USE innosphere_db;")

    # Check tables
    cursor.execute("SHOW FULL TABLES WHERE Table_Type = 'BASE TABLE';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Base Tables ({len(tables)}): {', '.join(tables)}")

    # Check views
    cursor.execute("SHOW FULL TABLES WHERE Table_Type = 'VIEW';")
    views = [row[0] for row in cursor.fetchall()]
    print(f"Views ({len(views)}): {', '.join(views)}")

    # Check procedures
    cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'innosphere_db';")
    procs = [row[1] for row in cursor.fetchall()]
    print(f"Stored Procedures ({len(procs)}): {', '.join(procs)}")

    # Check functions
    cursor.execute("SHOW FUNCTION STATUS WHERE Db = 'innosphere_db';")
    funcs = [row[1] for row in cursor.fetchall()]
    print(f"Stored Functions ({len(funcs)}): {', '.join(funcs)}")

    # Test Stored Function
    cursor.execute("SELECT fn_calculate_profile_completion(6) AS profile_pct;")
    fn_result = cursor.fetchone()
    print(f"Function Test fn_calculate_profile_completion(Atharv Hinge): {fn_result[0]}%")

    # Test View Query
    cursor.execute("SELECT project_title, team_name, average_score, leaderboard_rank FROM vw_hackathon_leaderboard LIMIT 2;")
    print("Leaderboard View Preview:")
    for row in cursor.fetchall():
        print(f"   Rank #{row[3]}: {row[0]} | Team: {row[1]} | Avg Score: {row[2]}")

    cursor.close()
    conn.close()
    print("\n Database setup completed successfully with all constraints and seed data.")
    print("=" * 70)

if __name__ == '__main__':
    run_setup()
