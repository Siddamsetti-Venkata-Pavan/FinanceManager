# File: data/transactions.py
import sqlite3
from datetime import datetime
from data.database import DB_NAME

def add_transaction(user_id, amount, category, type, date=None):
    """
    Saves a transaction.
    If 'date' is provided (YYYY-MM-DD), it uses that.
    If not, it defaults to today's date.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # If no date provided, use today
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
    INSERT INTO transactions (user_id, amount, category, type, date)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, amount, category, type, date))
    
    conn.commit()
    conn.close()
    return True

# File: data/transactions.py (Add to bottom)

def get_user_transactions(user_id):
    """Fetches all transactions for a user to display them"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, category, amount, type FROM transactions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def edit_transaction(transaction_id, user_id, new_amount, new_category):
    """Updates an existing transaction"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if the transaction actually belongs to this user (Security Check)
    cursor.execute("SELECT id FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return False, "Transaction not found or access denied."
    
    # Perform Update
    cursor.execute('''
        UPDATE transactions 
        SET amount = ?, category = ? 
        WHERE id = ?
    ''', (new_amount, new_category, transaction_id))
    
    conn.commit()
    conn.close()
    return True, "Update successful!"

# File: data/transactions.py (Add this function to the bottom)

def delete_transaction(transaction_id, user_id):
    """Removes a transaction from the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Security Check: Ensure this transaction belongs to this user
    cursor.execute("SELECT id FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return False, "Transaction not found or access denied."
    
    # 2. Perform Delete
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    return True, "Transaction deleted successfully!"