import sqlite3
import pandas as pd
from pathlib import Path
import re

# === CONFIGURATION ===
DB_PATH = "../db/energy_usage.db"
SQL_FILE = "energy_queries.sql"
EXPORT_DIR = Path("../exports")
EXPORT_DIR.mkdir(exist_ok=True)

# === PARSE SQL FILE ===
def parse_sql_file(path):
    with open(path, "r") as f:
        sql_content = f.read()

    # Split by comment marker -- name: query_name
    pattern = r"--\s*name:\s*(\w+)\s*\n(.*?)(?=(--\s*name:|\Z))"
    queries = re.findall(pattern, sql_content, flags=re.DOTALL)

    return [(name.strip(), query.strip()) for name, query, _ in queries]

# === EXPORT FUNCTION ===
def export_queries_to_csv(db_path, queries):
    conn = sqlite3.connect(db_path)

    for name, query in queries:
        print(f"Running query: {name}")
        df = pd.read_sql_query(query, conn)
        output_file = EXPORT_DIR / f"{name}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")

    conn.close()
    print("✅ All queries exported!")

# === MAIN ===
if __name__ == "__main__":
    parsed_queries = parse_sql_file(SQL_FILE)
    export_queries_to_csv(DB_PATH, parsed_queries)
