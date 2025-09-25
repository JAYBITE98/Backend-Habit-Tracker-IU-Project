def test_database():
    print("Testing database...")
    try:
        from db import Database
        db = Database("test_components.db")
        print("✅ Database connection OK")
        return db
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None


def test_habit_manager(db):
    print("Testing habit manager...")
    try:
        from habit_manager import HabitManager
        manager = HabitManager(db)
        manager.set_current_user(1)
        print("✅ Habit manager OK")
        return manager
    except Exception as e:
        print(f"❌ Habit manager error: {e}")
        return None


def test_analytics(db):
    print("Testing analytics...")
    try:
        from analytics import AnalyticsEngine
        analytics = AnalyticsEngine(db)
        print("✅ Analytics OK")
        return analytics
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return None


def main():
    print("🔍 Testing all components...")
    print("=" * 40)

    db = test_database()
    if db:
        manager = test_habit_manager(db)
        analytics = test_analytics(db)

    print("=" * 40)
    print("Component testing complete")


if __name__ == "__main__":
    main()