# File: data/budgets.py
import sqlite3
from data.database import DB_NAME

def set_budget(user_id, category, limit):
    """Sets or updates a budget limit for a category"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Check if a budget already exists for this specific category
    cursor.execute("SELECT id FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
    row = cursor.fetchone()
    
    if row:
        # UPDATE existing row
        # (We use the ID we just found to be precise)
        budget_id = row[0]
        cursor.execute("UPDATE budgets SET limit_amount = ? WHERE id = ?", (limit, budget_id))
    else:
        # INSERT new row
        cursor.execute("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", (user_id, category, limit))
    
    conn.commit()
    conn.close()
    return True

def check_budget_status(user_id, category):
    """
    Returns: (spent_amount, limit_amount)
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Get the Limit
    cursor.execute("SELECT limit_amount FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return 0.0, None # No budget set, return None for limit
        
    limit = row[0]
    
    # 2. Get Total Spent in this category
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND category = ? AND type = 'Expense'
    ''', (user_id, category))
    
    result = cursor.fetchone()
    spent = result[0] if result[0] is not None else 0.0
    
    conn.close()
    return spent, limit