import json
import sqlite3


def generate_foreign_key_column(cln_name, fk_properties):
    line = f"FOREIGN KEY ({cln_name}) REFERENCES {fk_properties['table']}({fk_properties['column']})"
    if od_value := fk_properties.get("on_delete"):
        line += f" ON DELETE {od_value}"
    return line


def generate_common_column(cln_properties):
    line = f"{cln_properties['name']} {cln_properties['type']}"
    if cln_properties.get("primary_key"):
        line += " PRIMARY KEY"
    if not cln_properties.get("nullable", True):
        line += " NOT NULL"
    return line


def load_schema(json_path, db_path):
    with open(json_path, "r") as f:
        schema = json.load(f)

    table_name = schema["table_name"]
    columns = schema["columns"]

    col_defs = []
    for col in columns:
        # manage if there is foreign key
        if fk_properties := col.get("foreigh_key"):
            line = generate_foreign_key_column(col["name"], fk_properties)
        else:
            line = generate_common_column(col)
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

    # find a record with most keys
    index = 0
    key_cnt = 0
    for i in range(len(records)):
        if c := len(records[i].keys()) > key_cnt:
            key_cnt = c
            index = i

    keys = records[index].keys()
    columns = ", ".join(keys)
    placeholders = ", ".join(["?"] * len(keys))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for record in records:
        values = tuple(record.get(k, "") for k in keys)
        cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
        )

    conn.commit()
    conn.close()
    print(f"Inserted {len(records)} records into `{table_name}`.")
