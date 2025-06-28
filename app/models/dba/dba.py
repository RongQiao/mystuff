from app.models.dba.schema_loader import load_schema, insert_data_from_json
from config import db_config
from pathlib import Path
import sqlite3

def init_db():
    if not db_config.DB_DIR.exists():
        db_config.DB_DIR.mkdir(parents=True)
        print(f"Created database directory: {db_config.DB_DIR}")

    if not db_config.DB_PATH.exists():
        # This will create the SQLite file
        conn = sqlite3.connect(db_config.DB_PATH)
        conn.close()
        print(f"Initialized empty database at {db_config.DB_PATH}")
    else:
        print(f"Database already exists at {db_config.DB_PATH}")


def drop_all_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        table = table_name[0]
        if table == "sqlite_sequence":  # Skip internal table used for AUTOINCREMENT
            continue
        cursor.execute(f'DROP TABLE IF EXISTS "{table}";')
        print(f"Dropped table: {table}")

    conn.commit()
    conn.close()


def dba(run_schema: bool = True, run_data: bool = True):
    if run_schema:
        # make sure db is initialzed
        init_db()
        # drop all tables if there are old data -- for development phase
        drop_all_tables(db_config.DB_PATH)
        # create tables
        path = Path(db_config.SCHEMA_PATH)
        schema_files = list(path.glob('*.json'))
        for schema in schema_files:
            load_schema(schema, db_config.DB_PATH)

    if run_data:
        data_path = db_config.DATA_FILE_PATH / "people_individual.json"
        insert_data_from_json(data_path, db_config.DB_PATH, "people_individual")
        data_path = db_config.DATA_FILE_PATH / "rong_salary_upto_2024.json"
        insert_data_from_json(data_path, db_config.DB_PATH, "finance_income")
        data_path = db_config.DATA_FILE_PATH / "finance_invest_account.json"
        insert_data_from_json(data_path, db_config.DB_PATH, "finance_invest_account")
        data_path = db_config.DATA_FILE_PATH / "finance_invest_account_value.json"
        insert_data_from_json(data_path, db_config.DB_PATH, "finance_invest_account_value")

