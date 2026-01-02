import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

print("Cleaning up duplicate budgets...")

# This SQL query keeps only the LATEST budget for each category and deletes older duplicates
cursor.execute('''
DELETE FROM budgets 
WHERE id NOT IN (
    SELECT MAX(id) 
    FROM budgets 
    GROUP BY user_id, category
)
''')

conn.commit()
conn.close()
print("✅ Fixed! Duplicate budgets removed.")