import json
import sqlite3


def generate_foreign_key_column(col_name, fk_properties):
    """Generate foreign key constraint SQL."""
    line = f"FOREIGN KEY ({col_name}) REFERENCES {fk_properties['table']}({fk_properties['column']})"
    if od_value := fk_properties.get("on_delete"):
        line += f" ON DELETE {od_value}"
    return line


def generate_common_column(col_properties):
    """Generate column definition SQL."""
    line = f"{col_properties['name']} {col_properties['type']}"
    if col_properties.get("primary_key"):
        line += " PRIMARY KEY"
    if not col_properties.get("nullable", True):
        line += " NOT NULL"
    if d_value := col_properties.get("default"):
        line += f" DEFAULT {d_value}"
    return line


def load_schema(json_path, db_path):
    """Load and create table schema from JSON file."""
    try:
        print(f"Loading schema from: {json_path}")
        with open(json_path, "r") as f:
            schema = json.load(f)

        table_name = schema["table_name"]
        columns = schema["columns"]

        col_defs = []
        fk_constraints = []
        for col in columns:
            # manage if there is foreign key
            if fk_properties := col.get("foreign_key"):
                # Add the column definition first
                line = generate_common_column(col)
                col_defs.append(line)
                # Then add the foreign key constraint
                fk_line = generate_foreign_key_column(col["name"], fk_properties)
                fk_constraints.append(fk_line)
            else:
                line = generate_common_column(col)
                col_defs.append(line)

        # Add foreign key constraints at the end
        col_defs.extend(fk_constraints)

        create_stmt = (
            f"CREATE TABLE IF NOT EXISTS {table_name} (\n  "
            + ",\n  ".join(col_defs)
            + "\n);"
        )

        # print(f"Generated SQL for {table_name}:")
        # print(create_stmt)
        # print("---")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(create_stmt)
        conn.commit()
        conn.close()

        print(f"Table `{table_name}` created in {db_path}.")
    except FileNotFoundError:
        print(f"ERROR: Schema file not found: {json_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in schema file {json_path}: {e}")
        raise
    except KeyError as e:
        print(f"ERROR: Missing required key '{e}' in schema file {json_path}")
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error processing schema file {json_path}: {e}")
        raise


def insert_data_from_json(json_data_path, db_path, table_name):
    """Insert data from JSON file into database table."""
    try:
        print(f"Loading data from: {json_data_path}")
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

        for i, record in enumerate(records):
            values = tuple(record.get(k, "") for k in keys)
            sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            try:
                cursor.execute(sql_query, values)
            except sqlite3.OperationalError as err:
                print(f"ERROR: SQL error on record {i+1} in {json_data_path}")
                print(f"Query: {sql_query}")
                print(f"Values: {values}")
                print(f"Error: {err}")
                raise err

        conn.commit()
        conn.close()
        print(f"Inserted {len(records)} records into `{table_name}`.")
    except FileNotFoundError:
        print(f"ERROR: Data file not found: {json_data_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in data file {json_data_path}: {e}")
        print(f"Line {e.lineno}, column {e.colno}: {e.msg}")
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error processing data file {json_data_path}: {e}")
        raise
