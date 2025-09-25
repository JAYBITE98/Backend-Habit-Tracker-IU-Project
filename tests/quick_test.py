# quick_test.py
print("=== QUICK SYSTEM CHECK ===")

try:
    from cli import HabitTrackerCLI

    cli = HabitTrackerCLI()
    print("✅ CLI imports and initializes correctly")

    from src.advanced_analytics import AdvancedAnalytics
    from src.db import Database

    db = Database()
    analytics = AdvancedAnalytics(db)
    print("✅ Analytics imports correctly")

    print("🎉 System is ready!")

except Exception as e:
    print(f"❌ Error: {e}")