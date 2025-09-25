from src.db import Database
from src.habit_manager import HabitManager
from datetime import datetime, timedelta
import random


class TestDataGenerator:
    """
    Generates 4 weeks of test data for habits.
    """

    def __init__(self, db_path="habits.db"):
        self.db = Database(db_path)
        self.manager = HabitManager(self.db)

    def setup_test_user(self):
        """Create a test user if needed."""
        try:
            # Try to create test user
            self.db.register_user("testuser", "test@test.com", "testpass")
            print("✅ Created test user")
        except:
            # User probably already exists
            print("ℹ️  Test user already exists")

        # Login the test user
        user_id = self.db.authenticate_user("testuser", "testpass")
        self.manager.set_current_user(user_id)
        return user_id

    def generate_test_data(self, user_id=1):
        """
        Generate 4 weeks of test data with specific patterns.
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
        existing_habits = self.manager.list_habits()

        if not existing_habits:
            print("Adding test habits...")
            for name, habit_type in test_habits:
                self.manager.add_habit(name, habit_type)
                # Get the newly created habit ID
                habits = self.manager.list_habits()
                habit_id = habits[-1][0]  # Get the last added habit
                habit_ids.append(habit_id)
                print(f"✅ Added habit: {name} (ID: {habit_id})")
        else:
            print("Using existing habits...")
            for habit in existing_habits:
                habit_ids.append(habit[0])
                print(f"ℹ️  Using existing habit: {habit[1]} (ID: {habit[0]})")

        # Generate 4 weeks of completion data (starting from 28 days ago)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=28)  # 4 weeks back

        print(f"Generating data from {start_date.date()} to {end_date.date()}")

        # Track total completions
        total_completions = 0

        # Generate data for each habit
        for habit_id in habit_ids:
            completions = self._generate_habit_completions(habit_id, start_date, end_date)
            total_completions += completions
            print(f"✅ Habit ID {habit_id}: {completions} completions")

        print(f"🎉 Generated {total_completions} total completions across {len(habit_ids)} habits!")

    def _generate_habit_completions(self, habit_id, start_date, end_date):
        """Generate completions for a single habit."""
        completions = 0
        current_date = start_date

        # Get habit type to determine frequency
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM Habits WHERE habit_id = ?", (habit_id,))
        habit_type = cursor.fetchone()[0]
        conn.close()

        while current_date <= end_date:
            if habit_type == "daily":
                # Daily habit - 70% chance of completion each day
                if random.random() < 0.7:
                    self._add_completion(habit_id, current_date)
                    completions += 1
                current_date += timedelta(days=1)
            else:
                # Weekly habit - complete once per week
                if current_date.weekday() == 0:  # Monday
                    if random.random() < 0.8:  # 80% chance weekly
                        self._add_completion(habit_id, current_date)
                        completions += 1
                current_date += timedelta(days=1)

        return completions

    def _add_completion(self, habit_id, date):
        """Add a completion record with random time."""
        # Add some randomness to the time
        random_time = date.replace(
            hour=random.randint(8, 20),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Completions (habit_id, timestamp) VALUES (?, ?)",
            (habit_id, random_time)
        )
        conn.commit()
        conn.close()


def main():
    """Generate test data."""
    print("=== HABIT TRACKER TEST DATA GENERATOR ===")

    generator = TestDataGenerator()

    # Setup test user
    user_id = generator.setup_test_user()
    print(f"Using user ID: {user_id}")

    # Generate test data
    generator.generate_test_data(user_id)

    print("\n📊 Test data generation complete!")
    print("💡 Run your CLI to see the generated data!")


if __name__ == "__main__":
    main()