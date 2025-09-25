from src.db import Database


class HabitManager:
    """
    Manages habit operations and business logic.
    """

    def __init__(self, db: Database):
        self.db = db
        self.current_user_id = None  # Will be set after login

    def set_current_user(self, user_id: int):
        """Set the currently logged-in user."""
        self.current_user_id = user_id

    def add_habit(self, name: str, habit_type: str):
        """
        Add a new habit for the current user.
        """
        if not self.current_user_id:
            raise ValueError("No user logged in")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Habits (user_id, name, type) VALUES (?, ?, ?)",
            (self.current_user_id, name, habit_type)
        )
        conn.commit()
        conn.close()
        # Should NOT add a completion here!

    def list_habits(self):
        """
        List all habits for the current user.
        """
        if not self.current_user_id:
            raise ValueError("No user logged in")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT habit_id, name, type, created_at FROM Habits WHERE user_id = ? AND is_active = TRUE",
            (self.current_user_id,)
        )
        habits = cursor.fetchall()
        conn.close()
        return habits

    def check_off_habit(self, habit_id: int, notes: str = None, mood_score: int = None):
        """
        Record a completion for a habit (with user validation).
        """
        if not self.current_user_id:
            raise ValueError("No user logged in")

        # Verify the habit belongs to the current user
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT habit_id FROM Habits WHERE habit_id = ? AND user_id = ?",
            (habit_id, self.current_user_id)
        )
        if not cursor.fetchone():
            conn.close()
            raise ValueError("Habit not found or access denied")

        cursor.execute(
            "INSERT INTO Completions (habit_id, notes, mood_score) VALUES (?, ?, ?)",
            (habit_id, notes, mood_score)
        )
        conn.commit()
        conn.close()