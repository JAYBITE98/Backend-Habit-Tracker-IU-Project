print("=== DEBUG START ===")


def main():
    # Test 1: Database
    print("1. Testing database...")
    try:
        from db import Database
        db = Database("debug_test.db")
        print("✅ Database: OK")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return

    # Test 2: Habit Manager
    print("2. Testing habit manager...")
    try:
        from habit_manager import HabitManager
        manager = HabitManager(db)

        # Check if set_current_user exists
        if hasattr(manager, 'set_current_user'):
            manager.set_current_user(1)
            print("✅ HabitManager.set_current_user: OK")
        else:
            print("❌ HabitManager missing set_current_user method")
            return

        print("✅ HabitManager: OK")
    except Exception as e:
        print(f"❌ HabitManager error: {e}")
        return

    # Test 3: Analytics
    print("3. Testing analytics...")
    try:
        from analytics import AnalyticsEngine
        analytics = AnalyticsEngine(db)
        print("✅ AnalyticsEngine: OK")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return

    # Test 4: CLI
    print("4. Testing CLI...")
    try:
        from cli import HabitTrackerCLI
        cli = HabitTrackerCLI()
        print("✅ HabitTrackerCLI: OK")
    except Exception as e:
        print(f"❌ CLI error: {e}")
        return

    print("🎉 ALL COMPONENTS WORKING!")

    # Cleanup
    import os
    if os.path.exists("debug_test.db"):
        os.remove("debug_test.db")


if __name__ == "__main__":
    main()