from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from db import Database


class AdvancedAnalytics:
    """
    Advanced analytics with functional programming principles.
    Implements real streak calculation algorithms.
    """

    def __init__(self, db: Database):
        self.db = db

    def get_habits_by_periodicity(self, user_id: int, periodicity: str) -> List[Tuple]:
        """
        Pure function: Filter habits by periodicity.
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

    def get_completions_for_habit(self, habit_id: int) -> List[datetime]:
        """
        Pure function: Get all completions for a habit, sorted by date.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp FROM Completions WHERE habit_id = ? ORDER BY timestamp",
            (habit_id,)
        )
        completions = []
        for row in cursor.fetchall():
            if row[0]:  # Only process if timestamp is not None
                timestamp_str = str(row[0])
                try:
                    # Handle different timestamp formats
                    if 'Z' in timestamp_str:
                        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.fromisoformat(timestamp_str)
                    completions.append(dt)
                except ValueError as e:
                    print(f"Warning: Could not parse timestamp '{timestamp_str}': {e}")
                    continue
        conn.close()
        return completions

    def calculate_current_streak(self, habit_id: int) -> int:
        """
        Calculate current streak using FP principles.
        """
        completions = self.get_completions_for_habit(habit_id)
        if not completions:
            return 0

        habit_type = self.get_habit_type(habit_id)
        today = datetime.now().date()

        if habit_type == 'daily':
            return self._calculate_daily_streak(completions, today)
        else:
            return self._calculate_weekly_streak(completions, today)

    def calculate_longest_streak(self, habit_id: int) -> int:
        """
        Calculate longest streak using FP principles.
        """
        completions = self.get_completions_for_habit(habit_id)
        if not completions:
            return 0

        habit_type = self.get_habit_type(habit_id)

        if habit_type == 'daily':
            return self._calculate_longest_daily_streak(completions)
        else:
            return self._calculate_longest_weekly_streak(completions)

    def _calculate_daily_streak(self, completions: List[datetime], today: datetime.date) -> int:
        """Calculate current streak for daily habits."""
        streak = 0
        current_date = today

        completion_dates = {comp.date() for comp in completions}

        while current_date in completion_dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak

    def _calculate_weekly_streak(self, completions: List[datetime], today: datetime.date) -> int:
        """Calculate current streak for weekly habits."""
        streak = 0
        current_date = today
        current_week = current_date.isocalendar()[1]
        current_year = current_date.year

        completion_weeks = set()
        for comp in completions:
            comp_week = comp.isocalendar()[1]
            comp_year = comp.year
            completion_weeks.add((comp_year, comp_week))

        while (current_year, current_week) in completion_weeks:
            streak += 1
            current_date -= timedelta(weeks=1)
            current_week = current_date.isocalendar()[1]
            current_year = current_date.year

        return streak

    def _calculate_longest_daily_streak(self, completions: List[datetime]) -> int:
        """Calculate longest streak for daily habits."""
        if not completions:
            return 0

        dates = sorted(list({comp.date() for comp in completions}))

        longest_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

        return longest_streak

    def _calculate_longest_weekly_streak(self, completions: List[datetime]) -> int:
        """Calculate longest streak for weekly habits."""
        if not completions:
            return 0

        weeks = sorted(list({(comp.year, comp.isocalendar()[1]) for comp in completions}))

        longest_streak = 1
        current_streak = 1

        for i in range(1, len(weeks)):
            current_year, current_week = weeks[i]
            prev_year, prev_week = weeks[i - 1]

            if (current_year == prev_year and current_week == prev_week + 1) or \
                    (current_year == prev_year + 1 and current_week == 1 and prev_week == 52):
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

        return longest_streak

    def get_habit_type(self, habit_id: int) -> str:
        """Get the type of a habit."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM Habits WHERE habit_id = ?", (habit_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'daily'

    def get_longest_streak_all(self, user_id: int) -> Tuple[Optional[str], int]:
        """
        Get the habit with the longest streak across all habits.
        """
        daily_habits = self.get_habits_by_periodicity(user_id, 'daily')
        weekly_habits = self.get_habits_by_periodicity(user_id, 'weekly')
        all_habits = daily_habits + weekly_habits

        longest_habit_name = None
        longest_streak = 0

        for habit in all_habits:
            habit_id, name, habit_type, created_at = habit
            streak = self.calculate_longest_streak(habit_id)

            if streak > longest_streak:
                longest_streak = streak
                longest_habit_name = name

        return longest_habit_name, longest_streak


# Functional programming style wrapper functions
def calculate_longest_streak(analytics: AdvancedAnalytics, habit_id: int) -> int:
    """FP-style wrapper for longest streak calculation."""
    return analytics.calculate_longest_streak(habit_id)


def get_longest_streak_all(analytics: AdvancedAnalytics, user_id: int) -> Tuple[Optional[str], int]:
    """FP-style wrapper for getting longest streak across all habits."""
    return analytics.get_longest_streak_all(user_id)


def get_habits_by_periodicity(analytics: AdvancedAnalytics, user_id: int, periodicity: str) -> List[Tuple]:
    """FP-style wrapper for filtering habits by periodicity."""
    return analytics.get_habits_by_periodicity(user_id, periodicity)