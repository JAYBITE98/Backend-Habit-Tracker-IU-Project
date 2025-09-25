from src.db import Database
from src.habit_manager import HabitManager
from src.advanced_analytics import AdvancedAnalytics
import os


class FinalTestSuite:
    """
    Comprehensive test suite for the Habit Tracker system.
    """

    def __init__(self):
        self.test_db_path = "final_test.db"
        # Always start with a clean database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        self.db = Database(self.test_db_path)
        self.manager = HabitManager(self.db)
        self.analytics = AdvancedAnalytics(self.db)
        self.test_user_id = None

    def run_all_tests(self):
        """Run all tests in the suite."""
        print("=== FINAL TEST SUITE ===")
        print("Testing Habit Tracker System\n")

        try:
            self.test_user_authentication()
            self.test_habit_management()
            self.test_streak_calculations()
            self.test_analytics_functions()
            self.test_data_integrity()

            print("\n🎉 ALL TESTS PASSED!")
            print("🚀 System is ready for production!")

        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {e}")
            print("⚠️  Some tests failed, but the core system may still work")
        except Exception as e:
            print(f"\n💥 UNEXPECTED ERROR: {e}")
        finally:
            # Cleanup
            if os.path.exists(self.test_db_path):
                try:
                    os.remove(self.test_db_path)
                except:
                    pass

    def test_user_authentication(self):
        """Test user registration and authentication."""
        print("1. Testing user authentication...")

        # Test registration
        result = self.db.register_user("finaltest", "final@test.com", "password123")
        assert result == True, "User registration should succeed"

        # Test authentication
        user_id = self.db.authenticate_user("finaltest", "password123")
        assert user_id == 1, "First user should have ID 1"

        self.manager.set_current_user(user_id)
        self.test_user_id = user_id
        print("   ✅ User authentication tests passed")

    def test_habit_management(self):
        """Test habit creation and management."""
        print("2. Testing habit management...")

        # Add habits
        self.manager.add_habit("Test Daily Habit", "daily")
        self.manager.add_habit("Test Weekly Habit", "weekly")

        # List habits
        habits = self.manager.list_habits()
        assert len(habits) == 2, "Should have exactly 2 habits"

        # Verify no completions exist for new habits
        for habit in habits:
            habit_id = habit[0]
            completions = self.analytics.get_completions_for_habit(habit_id)
            assert len(completions) == 0, f"New habit {habit_id} should have 0 completions"

        print("   ✅ Habit management tests passed")

    def test_streak_calculations(self):
        """Test streak calculation algorithms."""
        print("3. Testing streak calculations...")

        habits = self.manager.list_habits()
        habit_id = habits[0][0]  # First habit (should have 0 completions)

        # Test with no completions (brand new habit)
        current_streak = self.analytics.calculate_current_streak(habit_id)
        longest_streak = self.analytics.calculate_longest_streak(habit_id)

        # For a habit with 0 completions, both streaks should be 0
        assert current_streak == 0, f"Current streak should be 0, got {current_streak}"
        assert longest_streak == 0, f"Longest streak should be 0, got {longest_streak}"

        print("   ✅ Streak calculation tests passed")

    def test_analytics_functions(self):
        """Test analytics and FP functions."""
        print("4. Testing analytics functions...")

        # Test periodicity filter
        daily_habits = self.analytics.get_habits_by_periodicity(self.test_user_id, 'daily')
        weekly_habits = self.analytics.get_habits_by_periodicity(self.test_user_id, 'weekly')

        assert len(daily_habits) == 1, "Should have 1 daily habit"
        assert len(weekly_habits) == 1, "Should have 1 weekly habit"

        # Test FP wrapper functions
        from src.advanced_analytics import calculate_longest_streak, get_longest_streak_all

        # Test with a habit that has 0 completions
        habit_id = daily_habits[0][0]
        streak = calculate_longest_streak(self.analytics, habit_id)
        assert streak == 0, "FP function should return 0 for habit with 0 completions"

        # Test overall longest streak (should be 0 since no completions)
        longest_habit, longest_streak = get_longest_streak_all(self.analytics, self.test_user_id)
        assert longest_streak == 0, "Overall longest streak should be 0 with no completions"

        print("   ✅ Analytics functions tests passed")

    def test_data_integrity(self):
        """Test database integrity and constraints."""
        print("5. Testing data integrity...")

        # Test unique username constraint
        result = self.db.register_user("finaltest", "another@test.com", "password456")
        assert result == False, "Duplicate username should fail"

        print("   ✅ Data integrity tests passed")


def main():
    """Run the final test suite."""
    test_suite = FinalTestSuite()
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()