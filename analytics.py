from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from db import Database


class AnalyticsEngine:
    """
    Functional programming analytics for habit streaks and statistics.
    """

    def __init__(self, db: Database):
        self.db = db

    def get_habits_by_periodicity(self, user_id: int, periodicity: str) -> List[Tuple]:
        """
        Get habits filtered by periodicity (daily/weekly).
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT habit_id, name, type, created_at FROM Habits WHERE user_id = ? AND type = ? AND is_active = TRUE",
            (user_id, periodicity)
        )
        habits = cursor.fetchall()
        conn.close()
        return habits

    def calculate_current_streak(self, habit_id: int) -> int:
        """
        Calculate the current streak for a habit.
        """
        completions = self._get_completions_sorted(habit_id)
        if not completions:
            return 0

        streak = 0
        today = datetime.now().date()
        current_date = today

        # For daily habits
        if self._get_habit_type(habit_id) == 'daily':
            while current_date >= completions[0].date():
                if any(comp.date() == current_date for comp in completions):
                    streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break

        # For weekly habits
        else:
            current_week = current_date.isocalendar()[1]
            current_year = current_date.year

            while True:
                week_completions = [comp for comp in completions
                                    if comp.isocalendar()[1] == current_week
                                    and comp.year == current_year]

                if week_completions:
                    streak += 1
                    current_date -= timedelta(weeks=1)
                    current_week = current_date.isocalendar()[1]
                    current_year = current_date.year
                else:
                    break

        return streak

    def calculate_longest_streak(self, habit_id: int) -> int:
        """
        Calculate the longest streak for a habit.
        """
        completions = self._get_completions_sorted(habit_id)
        if not completions:
            return 0

        longest_streak = 0
        current_streak = 1

        # For daily habits
        if self._get_habit_type(habit_id) == 'daily':
            for i in range(1, len(completions)):
                if (completions[i].date() - completions[i - 1].date()).days == 1:
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1

            longest_streak = max(longest_streak, current_streak)

        # For weekly habits
        else:
            for i in range(1, len(completions)):
                current_week = completions[i].isocalendar()[1]
                prev_week = completions[i - 1].isocalendar()[1]

                if current_week == prev_week + 1 or (current_week == 1 and prev_week == 52):
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1

            longest_streak = max(longest_streak, current_streak)

        return longest_streak

    def get_longest_streak_all(self, user_id: int) -> Tuple[Optional[str], int]:
        """
        Get the habit with the longest streak across all habits.
        """
        habits = self.get_habits_by_periodicity(user_id, 'daily') + self.get_habits_by_periodicity(user_id, 'weekly')

        longest_habit = None
        longest_streak = 0

        for habit in habits:
            habit_id, name, habit_type, created_at = habit
            streak = self.calculate_longest_streak(habit_id)

            if streak > longest_streak:
                longest_streak = streak
                longest_habit = name

        return longest_habit, longest_streak

    def _get_completions_sorted(self, habit_id: int) -> List[datetime]:
        """Get completions for a habit, sorted by date."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM Completions WHERE habit_id = ? ORDER BY timestamp",
            (habit_id,)
        )
        completions = [datetime.fromisoformat(row[0]) for row in cursor.fetchall()]
        conn.close()
        return completions

    def _get_habit_type(self, habit_id: int) -> str:
        """Get the type of a habit (daily/weekly)."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM Habits WHERE habit_id = ?", (habit_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'daily'


# Functional programming style functions (as in original design)
def get_habits_by_periodicity(habits: List, periodicity: str) -> List:
    """Filter habits by periodicity (FP style)."""
    return [h for h in habits if h[2] == periodicity]


def calculate_longest_streak(analytics: AnalyticsEngine, habit_id: int) -> int:
    """Calculate longest streak (FP style wrapper)."""
    return analytics.calculate_longest_streak(habit_id)


def get_longest_streak_all(analytics: AnalyticsEngine, user_id: int) -> Tuple[Optional[str], int]:
    """Get longest streak across all habits (FP style wrapper)."""
    return analytics.get_longest_streak_all(user_id)