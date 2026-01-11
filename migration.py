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

        if "property_manager" not in columns:
            print("Migrating: Adding property_manager column to sites table")
            cursor.execute("ALTER TABLE sites ADD COLUMN property_manager INTEGER")

        if "facility_manager" not in columns:
            print("Migrating: Adding facility_manager column to sites table")
            cursor.execute("ALTER TABLE sites ADD COLUMN facility_manager INTEGER")
            
        # Create task_photos table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_photos'")
        if not cursor.fetchone():
            print("Migrating: Creating task_photos table")
            cursor.execute("""
                CREATE TABLE task_photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    filename TEXT,
                    content BLOB,
                    mime_type TEXT,
                    created_at DATETIME,
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)

        # Create chat tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_groups'")
        if not cursor.fetchone():
            print("Migrating: Creating chat_groups table")
            cursor.execute("""
                CREATE TABLE chat_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    is_group INTEGER DEFAULT 0,
                    created_at DATETIME
                )
            """)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_members'")
        if not cursor.fetchone():
            print("Migrating: Creating chat_members table")
            cursor.execute("""
                CREATE TABLE chat_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    user_id INTEGER,
                    joined_at DATETIME,
                    FOREIGN KEY (group_id) REFERENCES chat_groups(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_messages'")
        if not cursor.fetchone():
            print("Migrating: Creating chat_messages table")
            cursor.execute("""
                CREATE TABLE chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    sender_id INTEGER,
                    content TEXT,
                    sent_at DATETIME,
                    FOREIGN KEY (group_id) REFERENCES chat_groups(id),
                    FOREIGN KEY (sender_id) REFERENCES users(id)
                )
            """)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_files'")
        if not cursor.fetchone():
            print("Migrating: Creating chat_files table")
            cursor.execute("""
                CREATE TABLE chat_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    filename TEXT,
                    content BLOB,
                    mime_type TEXT,
                    uploaded_at DATETIME,
                    FOREIGN KEY (message_id) REFERENCES chat_messages(id)
                )
            """)

        # Sidebar: Create planner tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='planner_settings'")
        if not cursor.fetchone():
            print("Migrating: Creating planner_settings table")
            cursor.execute("""
                CREATE TABLE planner_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    start_time TEXT DEFAULT '09:00',
                    end_time TEXT DEFAULT '17:00',
                    work_days TEXT DEFAULT '0,1,2,3,4',
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='planner_events'")
        if not cursor.fetchone():
            print("Migrating: Creating planner_events table")
            cursor.execute("""
                CREATE TABLE planner_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    task_id INTEGER,
                    start_datetime DATETIME,
                    end_datetime DATETIME,
                    event_type TEXT,
                    title TEXT,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)
            
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.close()
