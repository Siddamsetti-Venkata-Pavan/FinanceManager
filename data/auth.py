# File: data/auth.py
import sqlite3
import hashlib
from data.database import DB_NAME, get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email, question, answer):
    """Registers user with extended details"""
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(password)
    # Store answer in lowercase for easier matching later
    hashed_answer = hash_password(answer.lower()) 
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, security_question, security_answer) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_pw, email, question, hashed_answer))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Error: Username already exists."

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    
    return user[0] if user else None

def get_user_recovery_info(username):
    """Fetches Email and Security Question for a username"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email, security_question, security_answer FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row # Returns (email, question, hashed_answer)

def reset_password(username, new_password):
    """Updates the password in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(new_password)
    
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pw, username))
    conn.commit()
    conn.close()
    return True