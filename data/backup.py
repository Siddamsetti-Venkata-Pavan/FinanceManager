# File: data/backup.py
import shutil
import os
from datetime import datetime
from data.database import DB_NAME

BACKUP_DIR = "backups"

def create_backup():
    """Creates a copy of the database with a timestamp"""
    # 1. Create the 'backups' folder if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # 2. Generate a unique filename (e.g., finance_2023-10-25_14-30-00.db)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"finance_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # 3. Copy the file
    try:
        shutil.copy(DB_NAME, backup_path)
        return True, f"Backup created: {backup_filename}"
    except FileNotFoundError:
        return False, "Database file not found. Run the app first."
    except Exception as e:
        return False, str(e)

def list_backups():
    """Returns a list of all backup files"""
    if not os.path.exists(BACKUP_DIR):
        return []
    
    # Get all .db files in the backups folder
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
    # Sort them (newest first)
    files.sort(reverse=True)
    return files

def restore_backup(filename):
    """Overwrites the current database with a backup file"""
    backup_path = os.path.join(BACKUP_DIR, filename)
    
    if not os.path.exists(backup_path):
        return False, "Backup file does not exist."
    
    try:
        # Dangerous Operation: Overwrite current DB
        shutil.copy(backup_path, DB_NAME)
        return True, "System restored successfully! Please restart the app."
    except Exception as e:
        return False, str(e)