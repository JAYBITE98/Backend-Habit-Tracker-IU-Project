def main():
    print("=== TESTING CLI EXECUTION ===")

    try:
        # Test if we can create the CLI object
        from cli import HabitTrackerCLI
        cli = HabitTrackerCLI()
        print("✅ HabitTrackerCLI object created OK")

        # Test if main menu method exists
        if hasattr(cli, 'auth_menu'):
            print("✅ auth_menu method exists")
        else:
            print("❌ auth_menu method missing")

        print("✅ CLI setup is working")
        print("\n💡 Now try running cli.py directly!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()