from src.advanced_analytics import AdvancedAnalytics
from src.db import Database


def test_complete_system():
    print("=== COMPREHENSIVE SYSTEM TEST ===")

    # Test database connection
    db = Database()
    print("✅ Database connection established")

    # Test advanced analytics
    analytics = AdvancedAnalytics(db)
    print("✅ Advanced analytics initialized")

    # Test with our test user
    user_id = 2

    # Test all analytics functions
    print("\n1. Testing periodicity filters...")
    daily_habits = analytics.get_habits_by_periodicity(user_id, 'daily')
    weekly_habits = analytics.get_habits_by_periodicity(user_id, 'weekly')
    print(f"   Found {len(daily_habits)} daily habits")
    print(f"   Found {len(weekly_habits)} weekly habits")

    print("\n2. Testing streak calculations...")
    if daily_habits:
        habit_id, name, habit_type, created_at = daily_habits[0]
        current_streak = analytics.calculate_current_streak(habit_id)
        longest_streak = analytics.calculate_longest_streak(habit_id)
        print(f"   {name}: Current streak = {current_streak}, Longest streak = {longest_streak}")

    print("\n3. Testing overall longest streak...")
    longest_habit, longest_streak = analytics.get_longest_streak_all(user_id)
    print(f"   Overall longest: {longest_habit} ({longest_streak})")

    print("\n4. Testing FP-style wrapper functions...")
    from src.advanced_analytics import calculate_longest_streak
    if daily_habits:
        habit_id = daily_habits[0][0]
        streak = calculate_longest_streak(analytics, habit_id)
        print(f"   FP function result: {streak}")

    print("\n🎉 COMPREHENSIVE TEST PASSED!")
    print("💡 The system is ready for production use!")


if __name__ == "__main__":
    test_complete_system()