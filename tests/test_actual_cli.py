def test_actual_cli():
    print("=== TESTING ACTUAL CLI CONTENT ===")

    try:
        # First, let's see what's available in cli module
        import cli
        print("✅ cli module imported successfully")

        # List all available classes and functions
        print("\nAvailable in cli module:")
        for item in dir(cli):
            if not item.startswith('__'):
                print(f"  - {item}")

        # Try to find the main class
        if hasattr(cli, 'SimpleHabitTrackerCLI'):
            print("\n✅ Found SimpleHabitTrackerCLI class")
            from cli import SimpleHabitTrackerCLI
            cli_instance = SimpleHabitTrackerCLI()
            print("✅ SimpleHabitTrackerCLI instance created")

        elif hasattr(cli, 'HabitTrackerCLI'):
            print("\n✅ Found HabitTrackerCLI class")
            from cli import HabitTrackerCLI
            cli_instance = HabitTrackerCLI()
            print("✅ HabitTrackerCLI instance created")

        else:
            print("\n❌ No recognizable CLI class found")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_actual_cli()