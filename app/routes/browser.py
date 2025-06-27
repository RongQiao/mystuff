from config import db_config
from flask import Blueprint, render_template
import sqlite3

browser_bp = Blueprint("browser", __name__)
DB_PATH = db_config.DB_PATH


@browser_bp.route("/")
def list_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template("tables.html", tables=tables)


@browser_bp.route("/table/<table_name>")
def show_table_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    summary = None
    if table_name == "finance_income":
        cursor.execute("SELECT SUM(amount) FROM finance_income")
        total_income = cursor.fetchone()[0] or 0

        cursor.execute(
            """
            SELECT period_type, SUM(amount)
            FROM finance_income
            GROUP BY period_type
        """
        )
        by_period = cursor.fetchall()

        summary = {"total_income": total_income, "by_period": by_period}

    conn.close()
    return render_template(
        "table_data.html",
        table_name=table_name,
        columns=column_names,
        rows=rows,
        summary=summary,
    )
