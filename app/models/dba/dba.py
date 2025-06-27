from app.models.dba.schema_loader import load_schema
from app.models.dba.schema_loader import insert_data_from_json
from config import db_config
import os
import sqlite3


def init_db():
    if not os.path.exists(db_config.DB_DIR):
        os.makedirs(db_config.DB_DIR)
        print(f"Created database directory: {db_config.DB_DIR}")

    if not os.path.exists(db_config.DB_PATH):
        # This will create the SQLite file
        conn = sqlite3.connect(db_config.DB_PATH)
        conn.close()
        print(f"Initialized empty database at {db_config.DB_PATH}")
    else:
        print(f"Database already exists at {db_config.DB_PATH}")


def dba(run_schema: bool = True, run_data: bool = True):
    if run_schema:
        init_db()
        load_schema(db_config.SCHEMA_PATH, db_config.DB_PATH)
    if run_data:
        DATA_PATH = os.path.join(db_config.DATA_FILE_PATH, "finance_income_data.json")
        insert_data_from_json(DATA_PATH, db_config.DB_PATH, "finance_income")
