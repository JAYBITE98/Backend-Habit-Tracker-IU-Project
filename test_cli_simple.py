print("=== TESTING CLI ===")

try:
    from cli import HabitTrackerCLI

    print("✅ CLI imports OK")

    cli = HabitTrackerCLI()
    print("✅ CLI object created OK")

    print("🎉 CLI is working!")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback

    traceback.print_exc()