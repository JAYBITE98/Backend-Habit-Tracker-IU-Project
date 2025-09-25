from analytics import AnalyticsEngine
from db import Database
import os
from datetime import datetime, timedelta


def test_streak_calculations():
    """Test streak calculation algorithms."""

    test_db_path = "test_analytics.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = Database(test_db_path)
    analytics = AnalyticsEngine(db)

    try:
        # Setup test data
        conn = db.get_connection()
        cursor = conn.cursor()

        # Add a test user and habit
        cursor.execute("INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
                       ("testuser", "test@test.com", "hash"))
        cursor.execute("INSERT INTO Habits (user_id, name, type) VALUES (?, ?, ?)",
                       (1, "Test Daily Habit", "daily"))
        habit_id = cursor.lastrowid

        # Add completions for a 5-day streak
        base_date = datetime.now() - timedelta(days=10)
        for i in range(5):
            comp_date = base_date + timedelta(days=i)
            cursor.execute("INSERT INTO Completions (habit_id, timestamp) VALUES (?, ?)",
                           (habit_id, comp_date))

        conn.commit()
        conn.close()

        # Test streak calculations
        current_streak = analytics.calculate_current_streak(habit_id)
        longest_streak = analytics.calculate_longest_streak(habit_id)

        assert current_streak == 0, "Current streak should be 0 (no recent completions)"
        assert longest_streak == 5, "Longest streak should be 5"

        print("✅ All analytics tests passed!")

    finally:
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
            except PermissionError:
                pass


if __name__ == "__main__":
    test_streak_calculations()