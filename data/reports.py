# File: data/reports.py
import sqlite3
from data.database import DB_NAME

def calculate_totals(cursor, user_id, date_filter_sql, params):
    """Helper function to calculate totals based on dynamic filters"""
    # 1. Calculate Income
    query = f"SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'Income' {date_filter_sql}"
    cursor.execute(query, (user_id, *params))
    income = cursor.fetchone()[0] or 0.0

    # 2. Calculate Expenses
    query = f"SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'Expense' {date_filter_sql}"
    cursor.execute(query, (user_id, *params))
    expense = cursor.fetchone()[0] or 0.0
    
    return income, expense, income - expense

def get_monthly_report(user_id, month, year):
    """Calculates totals for a specific month (e.g., 11, 2025)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # SQLite uses strftime to extract parts of the date string (YYYY-MM-DD)
    # %m gives '01', '11' etc.
    sql_filter = "AND strftime('%m', date) = ? AND strftime('%Y', date) = ?"
    
    # Ensure month is two digits (e.g., 5 -> '05')
    month_str = f"{int(month):02d}"
    year_str = str(year)
    
    income, expense, balance = calculate_totals(cursor, user_id, sql_filter, (month_str, year_str))
    conn.close()
    return income, expense, balance

def get_yearly_report(user_id, year):
    """Calculates totals for a specific year"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    sql_filter = "AND strftime('%Y', date) = ?"
    income, expense, balance = calculate_totals(cursor, user_id, sql_filter, (str(year),))
    
    conn.close()
    return income, expense, balance

def get_all_time_report(user_id):
    """Calculates totals for all time"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    income, expense, balance = calculate_totals(cursor, user_id, "", ())
    conn.close()
    return income, expense, balance