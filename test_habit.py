import pytest
from habit import DailyHabit, WeeklyHabit
from datetime import datetime


def test_daily_habit_creation():
    habit = DailyHabit("Drink water", datetime.now())
    assert habit.name == "Drink water"
    assert isinstance(habit.creation_date, datetime)


def test_weekly_habit_creation():
    habit = WeeklyHabit("Clean house", datetime.now())
    assert habit.name == "Clean house"