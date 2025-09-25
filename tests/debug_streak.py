# debug_streak.py
from src.db import Database
from src.habit_manager import HabitManager
from src.advanced_analytics import AdvancedAnalytics


def debug_streak_calculation():
    print("=== DEBUG STREAK CALCULATION ===")

    # Use a fresh test database
    db = Database("debug_streak.db")
    manager = HabitManager(db)
    analytics = AdvancedAnalytics(db)

    # Create test user and habit
    db.register_user("debuguser", "debug@test.com", "debugpass")
    user_id = db.authenticate_user("debuguser", "debugpass")
    manager.set_current_user(user_id)

    # Add a new habit
    manager.add_habit("Debug Habit", "daily")
    habits = manager.list_habits()
    habit_id = habits[0][0]

    print(f"Created habit ID: {habit_id}")
    print(f"Habbit has no completions yet")

    # Test streak calculation
    current_streak = analytics.calculate_current_streak(habit_id)
    longest_streak = analytics.calculate_longest_streak(habit_id)

    print(f"Current streak: {current_streak}")
    print(f"Longest streak: {longest_streak}")

    # Check what completions exist
    completions = analytics.get_completions_for_habit(habit_id)
    print(f"Number of completions found: {len(completions)}")

    if completions:
        print("Completions found (should be 0):")
        for comp in completions:
            print(f"  - {comp}")

    # Cleanup
    import os
    if os.path.exists("debug_streak.db"):
        os.remove("debug_streak.db")


if __name__ == "__main__":
    debug_streak_calculation()