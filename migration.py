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

        if "latitude" not in columns:
            print("Migrating: Adding latitude column to tasks table")
            cursor.execute("ALTER TABLE tasks ADD COLUMN latitude FLOAT")

        if "longitude" not in columns:
            print("Migrating: Adding longitude column to tasks table")
            cursor.execute("ALTER TABLE tasks ADD COLUMN longitude FLOAT")
            
        if "photos" not in columns:
            print("Migrating: Adding photos column to tasks table")
            cursor.execute("ALTER TABLE tasks ADD COLUMN photos JSON DEFAULT '[]'")
            
        # Migrate sites table
        cursor.execute("PRAGMA table_info(sites)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "latitude" not in columns:
            print("Migrating: Adding latitude column to sites table")
            cursor.execute("ALTER TABLE sites ADD COLUMN latitude FLOAT")
            
        if "longitude" not in columns:
            print("Migrating: Adding longitude column to sites table")
            cursor.execute("ALTER TABLE sites ADD COLUMN longitude FLOAT")
            
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.close()
