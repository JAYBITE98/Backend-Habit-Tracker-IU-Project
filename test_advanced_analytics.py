from advanced_analytics import AdvancedAnalytics
from db import Database


def test_advanced_analytics():
    print("=== TESTING ADVANCED ANALYTICS ===")

    # Use the main database (since we have test data)
    db = Database()
    analytics = AdvancedAnalytics(db)

    # Test with user_id 2 (our test user)
    user_id = 2

    print("1. Testing periodicity filter...")
    daily_habits = analytics.get_habits_by_periodicity(user_id, 'daily')
    weekly_habits = analytics.get_habits_by_periodicity(user_id, 'weekly')
    print(f"   Daily habits: {len(daily_habits)}")
    print(f"   Weekly habits: {len(weekly_habits)}")

    print("2. Testing streak calculations...")
    if daily_habits:
        habit_id = daily_habits[0][0]
        habit_name = daily_habits[0][1]

        current_streak = analytics.calculate_current_streak(habit_id)
        longest_streak = analytics.calculate_longest_streak(habit_id)

        print(f"   {habit_name}:")
        print(f"     Current streak: {current_streak} days")
        print(f"     Longest streak: {longest_streak} days")

    print("3. Testing longest streak across all habits...")
    longest_habit, longest_streak = analytics.get_longest_streak_all(user_id)
    print(f"   Longest streak: {longest_habit} ({longest_streak} days/weeks)")

    print("🎉 Advanced analytics test completed!")


if __name__ == "__main__":
    test_advanced_analytics()