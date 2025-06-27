import json
import sqlite3


def load_schema(json_path, db_path):
    with open(json_path, "r") as f:
        schema = json.load(f)

    table_name = schema["table_name"]
    columns = schema["columns"]

    col_defs = []
    for col in columns:
        line = f"{col['name']} {col['type']}"
        if col.get("primary_key"):
            line += " PRIMARY KEY"
        if not col.get("nullable", True):
            line += " NOT NULL"
        col_defs.append(line)

    create_stmt = (
        f"CREATE TABLE IF NOT EXISTS {table_name} (\n  "
        + ",\n  ".join(col_defs)
        + "\n);"
    )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(create_stmt)
    conn.commit()
    conn.close()

    print(f"Table `{table_name}` created in {db_path}.")


def insert_data_from_json(json_data_path, db_path, table_name):
    with open(json_data_path, "r") as f:
        records = json.load(f)

    if not records:
        print(f"No data found in {json_data_path}")
        return

    keys = records[0].keys()
    columns = ", ".join(keys)
    placeholders = ", ".join(["?"] * len(keys))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for record in records:
        values = tuple(record[k] for k in keys)
        cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
        )

    conn.commit()
    conn.close()
    print(f"Inserted {len(records)} records into `{table_name}`.")
