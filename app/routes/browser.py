from config import db_config
from flask import Blueprint, render_template
import sqlite3

from app.routes.aaa import fetch_login_data

browser_bp = Blueprint("browser", __name__)
DB_PATH = db_config.DB_PATH


@browser_bp.route('/')
def index():
    return render_template('index.html')

@browser_bp.route('/myaaa')
def myaaa():
    login_info = fetch_login_data( DB_PATH)
    return render_template('myaaa.html', login_info=login_info)

@browser_bp.route('/myfinance')
def myfinance():
    return render_template('myfinance.html')

@browser_bp.route("/mytable")
def mytable():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template("tables.html", tables=tables)


def generate_select_query_account_value():
    return """
        SELECT
            finance_invest_account_value.id,
            finance_invest_account_value.amount,
            finance_invest_account_value.check_date,
            finance_invest_account_value.note,
            finance_invest_account.name_full,
            finance_invest_account.company
        FROM finance_invest_account_value
        JOIN finance_invest_account ON finance_invest_account_value.account_id = finance_invest_account.id;
    """


def generate_select_query_income():
    return """
        SELECT
            finance_income.category,
            finance_income.amount,
            finance_income.received_date,
            finance_income.source,
            finance_income.note,
            people_individual.first_name,
            people_individual.last_name
        FROM finance_income
        JOIN people_individual ON finance_income.by_who = people_individual.id;
    """


def generate_select_query_stock():
    return """
    SELECT
            finance_invest_stock_hold.id,
            finance_invest_stock.name_full,
            finance_invest_stock_hold.quantity,
            finance_invest_stock_hold.current_value,
            finance_invest_stock_hold.check_date,
            finance_invest_stock.type,
            finance_invest_account.name_full
        FROM finance_invest_stock_hold
        JOIN finance_invest_stock ON finance_invest_stock_hold.stock_id = finance_invest_stock.id
        JOIN finance_invest_account ON finance_invest_stock_hold.account_id = finance_invest_account.id;
    """




def generate_select_query(table_name):
    if table_name == "finance_income":
        query = generate_select_query_income()
    elif table_name == "finance_invest_account_value":
        query = generate_select_query_account_value()
    elif table_name == "finance_invest_stock_hold":
        query = generate_select_query_stock()
    elif table_name == "aaa_login":
        query = generate_select_query_aaa_login()
    else:
        query = f"SELECT * FROM {table_name}"

    return query



@browser_bp.route("/table/<table_name>")
def show_table_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = generate_select_query(table_name)
    cursor.execute(query)
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
