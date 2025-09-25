from datetime import datetime
from typing import List, Optional


class BaseHabit:
    """
    Base class for all habits.
    """
    def __init__(self, name: str, creation_date: datetime):
        self.name = name
        self.creation_date = creation_date
        self.completion_records: List['Completion'] = []

    def is_due_on(self, date: datetime) -> bool:
        """
        Check if the habit is due on a given date.
        To be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class DailyHabit(BaseHabit):
    """
    A habit that is due every day.
    """
    def is_due_on(self, date: datetime) -> bool:
        # A daily habit is due every day
        return True


class WeeklyHabit(BaseHabit):
    """
    A habit that is due once per week.
    """
    def is_due_on(self, date: datetime) -> bool:
        # A weekly habit is due if it's the same weekday as creation
        return date.weekday() == self.creation_date.weekday()


class Completion:
    """
    Represents a completion (check-off) of a habit.
    """
    def __init__(self, timestamp: datetime, notes: Optional[str] = None, mood_score: Optional[int] = None):
        self.timestamp = timestamp
        self.notes = notes
        self.mood_score = mood_score