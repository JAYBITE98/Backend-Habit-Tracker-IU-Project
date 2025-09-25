from src.db import Database
from src.habit_manager import HabitManager
from datetime import datetime, timedelta
import random


class TestDataGenerator:
    """
    Generates 4 weeks of test data for habits as specified in the requirements.
    """

    def __init__(self, db_path="habits.db"):
        self.db = Database(db_path)
        self.manager = HabitManager(self.db)

    def generate_test_data(self, user_id=1):
        """
        Generate 4 weeks of test data with specific patterns:
        - Includes missed days/weeks
        - Crosses month boundaries
        - Realistic completion patterns
        """
        print("Generating 4 weeks of test data...")

        # Set the current user
        self.manager.set_current_user(user_id)

        # Define test habits (same as predefined habits)
        test_habits = [
            ("Drink eight glasses of water daily", "daily"),
            ("Spend 30 minutes exercising daily", "daily"),
            ("30 Minutes of meditation daily", "daily"),
            ("Clean the house once weekly", "weekly"),
            ("Call relatives once a week", "weekly")
        ]

        # Add habits if they don't exist
        habit_ids = []
        for name, habit_type in test_habits:
            self.manager.add_habit(name, habit_type)
            habit_ids.append(self._get_last_habit_id())
            print(f"✅ Added habit: {name}")

        # Generate 4 weeks of completion data (starting from 28 days ago)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=28)  # 4 weeks back

        self._generate_daily_habits_data(habit_ids[:3], start_date, end_date)  # First 3 are daily
        self._generate_weekly_habits_data(habit_ids[3:], start_date, end_date)  # Last 2 are weekly

        print("🎉 Test data generation complete!")

    def _get_last_habit_id(self):
        """Get the ID of the most recently added habit."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(habit_id) FROM Habits")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else 1

    def _generate_daily_habits_data(self, habit_ids, start_date, end_date):
        """Generate realistic daily habit data with some missed days."""
        current_date = start_date

        while current_date <= end_date:
            for habit_id in habit_ids:
                # Simulate realistic completion patterns:
                # - 85% chance of completion on weekdays
                # - 60% chance on weekends
                # - Specific missed days to test streak breaks

                is_weekend = current_date.weekday() >= 5  # Saturday/Sunday
                completion_chance = 0.85 if not is_weekend else 0.60

                # Create intentional streak breaks for testing
                if current_date.day == 15:  # Miss day 15 for streak break testing
                    completion_chance = 0.1

                if random.random() < completion_chance:
                    # Add completion with random time during the day
                    completion_time = current_date.replace(
                        hour=random.randint(8, 20),
                        minute=random.randint(0, 59)
                    )
                    self._add_completion(habit_id, completion_time)

            current_date += timedelta(days=1)

    def _generate_weekly_habits_data(self, habit_ids, start_date, end_date):
        """Generate weekly habit data with some missed weeks."""
        current_date = start_date

        while current_date <= end_date:
            for habit_id in habit_ids:
                # Weekly habits: 80% chance of completion each week
                # Miss one specific week for testing
                if current_date.weekday() == 0:  # Monday each week
                    completion_chance = 0.8

                    # Miss week containing the 20th for testing
                    if 18 <= current_date.day <= 24:
                        completion_chance = 0.1

                    if random.random() < completion_chance:
                        completion_time = current_date.replace(
                            hour=random.randint(10, 18),
                            minute=random.randint(0, 59)
                        )
                        self._add_completion(habit_id, completion_time)

            current_date += timedelta(days=1)

    def _add_completion(self, habit_id, timestamp):
        """Add a completion record to the database."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Completions (habit_id, timestamp) VALUES (?, ?)",
            (habit_id, timestamp)
        )
        conn.commit()
        conn.close()


def main():
    """Generate test data for the current user."""
    generator = TestDataGenerator()
    generator.generate_test_data(user_id=1)
    print("\n📊 Use inspect_db.py to view the generated data!")


if __name__ == "__main__":
    main()