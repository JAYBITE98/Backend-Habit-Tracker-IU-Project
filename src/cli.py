import sys
from db import Database
from habit_manager import HabitManager
from advanced_analytics import AdvancedAnalytics
from datetime import datetime


class HabitTrackerCLI:
    """
    Complete CLI with user authentication and all features.
    """

    def __init__(self):
        self.db = Database()
        self.manager = HabitManager(self.db)
        self.current_user_id = None
        self.current_username = None

    def auth_menu(self):
        """
        Authentication menu (login/register).
        """
        while True:
            print("\n" + "=" * 50)
            print("          HABIT TRACKER - WELCOME")
            print("=" * 50)
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            print("=" * 50)

            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
                if self.login():
                    self.main_menu()
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def login(self):
        """
        User login functionality.
        """
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            self.manager.set_current_user(user_id)
            print(f"✅ Welcome back, {username}!")
            return True
        else:
            print("❌ Invalid username or password.")
            return False

    def register(self):
        """
        User registration functionality.
        """
        print("\n--- Register ---")
        username = input("Choose a username: ").strip()
        email = input("Email: ").strip()
        password = input("Choose a password: ").strip()

        if not username or not email or not password:
            print("❌ All fields are required.")
            return

        if self.db.register_user(username, email, password):
            print("✅ Registration successful! Please login.")
        else:
            print("❌ Username or email already exists.")

    def main_menu(self):
        """
        Main application menu (after login).
        """
        while True:
            print(f"\n" + "=" * 50)
            print(f"     HABIT TRACKER - Welcome {self.current_username}!")
            print("=" * 50)
            print("1. List all habits")
            print("2. Add a new habit")
            print("3. Check off a habit")
            print("4. View analytics")
            print("5. Delete/Deactivate habit")
            print("6. Add predefined habits")
            print("7. Export data")
            print("8. Logout")
            print("=" * 50)

            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                self.list_habits()
            elif choice == "2":
                self.add_habit()
            elif choice == "3":
                self.check_off_habit()
            elif choice == "4":
                self.analytics_menu()
            elif choice == "5":
                self.delete_habit()
            elif choice == "6":
                self.add_predefined_habits()
            elif choice == "7":
                self.export_data()
            elif choice == "8":
                self.logout()
                break
            else:
                print("Invalid choice. Please enter a number between 1-8.")

    def list_habits(self):
        """
        Display all habits for the current user.
        """
        try:
            habits = self.manager.list_habits()
            if not habits:
                print("No habits found. Add some habits to get started!")
                return

            print("\n--- Your Habits ---")
            for habit in habits:
                habit_id, name, habit_type, created_at = habit
                print(f"ID: {habit_id} | {name} ({habit_type}) | Created: {created_at}")
            print("-------------------\n")
        except Exception as e:
            print(f"Error listing habits: {e}")

    def add_habit(self):
        """
        Add a new habit through simple input prompts.
        """
        print("\n--- Add New Habit ---")
        name = input("Enter habit name: ").strip()
        if not name:
            print("Habit name cannot be empty.")
            return

        print("Select habit type:")
        print("1. Daily")
        print("2. Weekly")
        type_choice = input("Enter choice (1 or 2): ").strip()

        if type_choice == "1":
            habit_type = "daily"
        elif type_choice == "2":
            habit_type = "weekly"
        else:
            print("Invalid choice. Habit not added.")
            return

        try:
            self.manager.add_habit(name, habit_type)
            print(f"✅ Habit '{name}' added successfully!\n")
        except Exception as e:
            print(f"Error adding habit: {e}")

    def add_predefined_habits(self):
        """
        Add the 5 predefined habits from the PDF.
        """
        predefined_habits = [
            ("Drink eight glasses of water daily", "daily"),
            ("Spend 30 minutes exercising daily", "daily"),
            ("30 Minutes of meditation daily", "daily"),
            ("Clean the house once weekly", "weekly"),
            ("Call relatives once a week", "weekly")
        ]

        print("\n--- Adding Predefined Habits ---")
        for name, habit_type in predefined_habits:
            try:
                self.manager.add_habit(name, habit_type)
                print(f"✅ Added: {name}")
            except Exception as e:
                print(f"❌ Error adding {name}: {e}")

    def check_off_habit(self):
        """
        Check off (complete) a habit.
        """
        try:
            habits = self.manager.list_habits()
            if not habits:
                print("No habits found. Add some habits first!")
                return

            print("\n--- Check Off Habit ---")
            print("Available habits:")
            for habit in habits:
                habit_id, name, habit_type, created_at = habit
                print(f"{habit_id}: {name} ({habit_type})")

            habit_id = int(input("Enter habit ID to check off: ").strip())
            notes = input("Add optional notes (press Enter to skip): ").strip()
            mood_score = input("Add optional mood score 1-10 (press Enter to skip): ").strip()

            mood_int = int(mood_score) if mood_score and mood_score.isdigit() else None

            self.manager.check_off_habit(habit_id, notes, mood_int)
            print("✅ Habit checked off successfully!\n")
        except ValueError:
            print("Invalid habit ID. Please enter a number.")
        except Exception as e:
            print(f"Error checking off habit: {e}")

    def delete_habit(self):
        """Delete or deactivate a habit."""
        habits = self.manager.list_habits()
        if not habits:
            print("No habits found to delete.")
            return

        print("\n--- Delete/Deactivate Habit ---")
        print("Available habits:")
        for habit in habits:
            habit_id, name, habit_type, created_at = habit
            print(f"{habit_id}: {name} ({habit_type})")

        try:
            habit_id = int(input("Enter habit ID to delete: ").strip())
            confirm = input("Are you sure? This will remove all completion data. (y/n): ").strip().lower()

            if confirm == 'y':
                self._delete_habit_from_db(habit_id)
                print("✅ Habit deleted successfully!")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Invalid habit ID. Please enter a number.")

    def _delete_habit_from_db(self, habit_id):
        """Delete a habit from the database."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # First delete completions (due to foreign key constraints)
        cursor.execute("DELETE FROM Completions WHERE habit_id = ?", (habit_id,))
        # Then delete the habit
        cursor.execute("DELETE FROM Habits WHERE habit_id = ?", (habit_id,))

        conn.commit()
        conn.close()

    def export_data(self):
        """Export habit data to a text file."""
        print("\n--- Export Data ---")
        filename = input("Enter filename for export (without extension): ").strip()
        if not filename:
            filename = "habit_export"

        filename += ".txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("HABIT TRACKER DATA EXPORT\n")
                f.write("=" * 50 + "\n\n")

                habits = self.manager.list_habits()
                f.write(f"Total Habits: {len(habits)}\n\n")

                for habit in habits:
                    habit_id, name, habit_type, created_at = habit
                    completions = self._get_completion_count(habit_id)

                    f.write(f"Habit: {name} ({habit_type})\n")
                    f.write(f"Created: {created_at}\n")
                    f.write(f"Total Completions: {completions}\n")

                    # Get completion dates
                    conn = self.db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT timestamp FROM Completions WHERE habit_id = ? ORDER BY timestamp",
                        (habit_id,)
                    )
                    dates = [row[0][:10] for row in cursor.fetchall()]  # Get just the date part
                    conn.close()

                    f.write(f"Completion Dates: {', '.join(dates)}\n")
                    f.write("-" * 30 + "\n\n")

                f.write(f"Export generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            print(f"✅ Data exported to {filename}")

        except Exception as e:
            print(f"❌ Error exporting data: {e}")

    def analytics_menu(self):
        """
        Display analytics sub-menu with advanced FP analytics.
        """
        analytics = AdvancedAnalytics(self.db)

        while True:
            print("\n--- Advanced Analytics Menu ---")
            print("1. View current streaks")
            print("2. View longest streaks")
            print("3. View habit statistics")
            print("4. Filter by periodicity")
            print("5. View longest streak overall")
            print("6. Back to main menu")

            try:
                choice = input("Enter your choice (1-6): ").strip()

                if choice == "1":
                    self.view_current_streaks(analytics)
                elif choice == "2":
                    self.view_longest_streaks(analytics)
                elif choice == "3":
                    self.view_habit_statistics(analytics)
                elif choice == "4":
                    self.filter_by_periodicity(analytics)
                elif choice == "5":
                    self.view_longest_streak_overall(analytics)
                elif choice == "6":
                    break
                else:
                    print("Invalid choice. Please enter a number between 1-6.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def view_current_streaks(self, analytics):
        """Display current streaks using advanced analytics."""
        print("\n--- Current Streaks ---")
        habits = self.manager.list_habits()

        for habit in habits:
            habit_id, name, habit_type, created_at = habit
            streak = analytics.calculate_current_streak(habit_id)
            period = "days" if habit_type == "daily" else "weeks"
            print(f"📊 {name}: {streak} {period} (current streak)")

    def view_longest_streaks(self, analytics):
        """Display longest streaks using advanced analytics."""
        print("\n--- Longest Streaks ---")
        habits = self.manager.list_habits()

        for habit in habits:
            habit_id, name, habit_type, created_at = habit
            streak = analytics.calculate_longest_streak(habit_id)
            period = "days" if habit_type == "daily" else "weeks"
            print(f"🏆 {name}: {streak} {period} (longest streak)")

    def view_habit_statistics(self, analytics):
        """Display comprehensive statistics for each habit."""
        print("\n--- Habit Statistics ---")
        habits = self.manager.list_habits()

        for habit in habits:
            habit_id, name, habit_type, created_at = habit
            completions = self._get_completion_count(habit_id)
            current_streak = analytics.calculate_current_streak(habit_id)
            longest_streak = analytics.calculate_longest_streak(habit_id)

            success_rate = self._calculate_success_rate(habit_id, habit_type, created_at)

            print(f"\n📈 {name} ({habit_type}):")
            print(f"   Total completions: {completions}")
            print(f"   Success rate: {success_rate}%")
            print(f"   Current streak: {current_streak}")
            print(f"   Longest streak: {longest_streak}")
            print(f"   Created: {created_at[:10]}")

    def view_longest_streak_overall(self, analytics):
        """Display the longest streak across all habits."""
        print("\n--- Longest Streak Overall ---")
        longest_habit, longest_streak = analytics.get_longest_streak_all(self.current_user_id)

        if longest_habit:
            print(f"🎯 CHAMPION HABIT: {longest_habit}")
            print(f"🔥 LONGEST STREAK: {longest_streak} days/weeks")

            # Show some encouragement based on streak length
            if longest_streak >= 30:
                print("💎 LEGENDARY! You're building amazing habits!")
            elif longest_streak >= 14:
                print("⭐ EXCELLENT! You're very consistent!")
            elif longest_streak >= 7:
                print("👍 GREAT JOB! Keep up the good work!")
            else:
                print("💪 GOOD START! Every streak begins with one completion!")
        else:
            print("No streak data available yet. Keep building those habits!")

    def filter_by_periodicity(self, analytics):
        """Filter habits by periodicity with statistics."""
        print("\n--- Filter by Periodicity ---")
        print("1. Daily habits")
        print("2. Weekly habits")

        choice = input("Enter choice (1-2): ").strip()
        periodicity = "daily" if choice == "1" else "weekly" if choice == "2" else None

        if periodicity:
            habits = analytics.get_habits_by_periodicity(self.current_user_id, periodicity)

            print(f"\n--- {periodicity.upper()} HABITS ---")
            for habit in habits:
                habit_id, name, habit_type, created_at = habit
                completions = self._get_completion_count(habit_id)
                current_streak = analytics.calculate_current_streak(habit_id)

                print(f"● {name}")
                print(f"  Completions: {completions} | Current streak: {current_streak}")
        else:
            print("Invalid choice.")

    def _get_completion_count(self, habit_id):
        """Get the number of completions for a habit."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Completions WHERE habit_id = ?", (habit_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _calculate_success_rate(self, habit_id, habit_type, created_date):
        """Calculate success rate for a habit."""
        # Calculate days/weeks since creation
        created = datetime.fromisoformat(
            created_date.replace('Z', '+00:00')) if 'Z' in created_date else datetime.fromisoformat(created_date)
        now = datetime.now()

        if habit_type == 'daily':
            days_since_creation = (now - created).days
            expected_completions = max(days_since_creation, 1)  # At least 1
        else:
            weeks_since_creation = (now - created).days // 7
            expected_completions = max(weeks_since_creation, 1)

        actual_completions = self._get_completion_count(habit_id)

        if expected_completions > 0:
            success_rate = (actual_completions / expected_completions) * 100
            return round(success_rate, 1)
        return 0.0

    def logout(self):
        """Log out the current user."""
        self.current_user_id = None
        self.current_username = None
        self.manager.set_current_user(None)
        print("✅ Logged out successfully.")


def main():
    """
    Main entry point for the Habit Tracker CLI.
    """
    cli = HabitTrackerCLI()
    cli.auth_menu()


if __name__ == "__main__":
    main()