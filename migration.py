import sqlite3
import os
from database import DATA_DIR

def migrate_db():
    db_path = os.path.join(DATA_DIR, "data.db")
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "due_date" not in columns:
            print("Migrating: Adding due_date column to tasks table")
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date DATETIME")
            
        if "photos" not in columns:
            print("Migrating: Adding photos column to tasks table")
            cursor.execute("ALTER TABLE tasks ADD COLUMN photos JSON DEFAULT '[]'")
            
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.close()
