def main():
    print("=== DEEP CHECK ===")

    # Test 1: Basic db import
    print("1. Testing db import...")
    try:
        from db import Database
        print("✅ from db import Database - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 2: Create database instance
    print("2. Testing database creation...")
    try:
        db = Database("test_deep.db")
        print("✅ Database() creation - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 3: Test habit import
    print("3. Testing habit import...")
    try:
        from habit import BaseHabit, DailyHabit, WeeklyHabit
        print("✅ habit imports - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 4: Test habit manager import
    print("4. Testing habit manager import...")
    try:
        from habit_manager import HabitManager
        print("✅ HabitManager import - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 5: Create habit manager
    print("5. Testing habit manager creation...")
    try:
        manager = HabitManager(db)
        print("✅ HabitManager() creation - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 6: Check if set_current_user method exists
    print("6. Testing set_current_user method...")
    try:
        if hasattr(manager, 'set_current_user'):
            manager.set_current_user(1)
            print("✅ set_current_user method - OK")
        else:
            print("❌ set_current_user method missing!")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 7: Test analytics import
    print("7. Testing analytics import...")
    try:
        from analytics import AnalyticsEngine
        print("✅ AnalyticsEngine import - OK")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print("🎉 ALL CHECKS PASSED! The system is working.")

    # Cleanup
    import os
    if os.path.exists("test_deep.db"):
        os.remove("test_deep.db")


if __name__ == "__main__":
    main()