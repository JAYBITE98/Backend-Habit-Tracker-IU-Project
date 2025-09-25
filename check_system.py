print("=== SYSTEM CHECK ===")
print("1. Testing basic Python...")
print("✅ Basic Python is working")

print("2. Testing imports...")
try:
    from db import Database

    print("✅ db.py import works")

    from habit_manager import HabitManager

    print("✅ habit_manager.py import works")

    print("🎉 All imports successful!")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")