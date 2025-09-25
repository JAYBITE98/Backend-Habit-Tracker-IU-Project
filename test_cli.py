from cli import HabitTrackerCLI
from db import Database
from habit_manager import HabitManager


def test_cli_initialization():
    """Test that CLI initializes correctly."""
    cli = HabitTrackerCLI()

    # These should be None initially (no user logged in)
    assert cli.current_user_id is None, "current_user_id should be None before login"
    assert cli.current_username is None, "current_username should be None before login"

    # Check that database and manager are properly initialized
    assert isinstance(cli.db, Database), "db should be a Database instance"
    assert isinstance(cli.manager, HabitManager), "manager should be a HabitManager instance"

    # Manager should also have no current user initially
    assert cli.manager.current_user_id is None, "manager should have no current user initially"

    print("✅ CLI initialization test passed!")


def test_cli_after_login():
    """Test CLI after simulating a login."""
    cli = HabitTrackerCLI()

    # Simulate a login by setting the user directly
    cli.current_user_id = 1
    cli.current_username = "testuser"
    cli.manager.set_current_user(1)

    assert cli.current_user_id == 1, "current_user_id should be 1 after login"
    assert cli.current_username == "testuser", "current_username should be set after login"
    assert cli.manager.current_user_id == 1, "manager should have current user after login"

    print("✅ CLI after login test passed!")


if __name__ == "__main__":
    test_cli_initialization()
    test_cli_after_login()
    print("🎉 All CLI tests passed!")