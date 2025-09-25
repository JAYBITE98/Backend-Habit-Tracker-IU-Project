import sqlite3
import os


def inspect_database():
    """Inspect the database structure and contents."""

    if not os.path.exists("habits.db"):
        print("❌ habits.db file not found!")
        return

    print("✅ Database file found!")
    print(f"📊 File size: {os.path.getsize('habits.db')} bytes")

    # Connect to the database
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # List all tables
    print("\n📋 TABLES IN DATABASE:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name} ---")

        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"Total rows: {count}")

        # Show some sample data (first 3 rows)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            rows = cursor.fetchall()
            print("Sample data:")
            for row in rows:
                print(f"  {row}")

    conn.close()


if __name__ == "__main__":
    inspect_database()