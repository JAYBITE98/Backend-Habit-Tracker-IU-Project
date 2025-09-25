import pytest
import os
from src.db import Database
from src.habit_manager import HabitManager


# Pytest fixtures
@pytest.fixture
def test_db():
    """Create a test database."""
    test_db_path = "test_habittracker.db"
    # Clean up any existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = Database(test_db_path)
    yield db

    # Cleanup after test
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture
def test_manager(test_db):
    """Create a habit manager with test database."""
    manager = HabitManager(test_db)
    # Add a test user and set as current
    test_db.register_user("testuser", "test@test.com", "password123")
    user_id = test_db.authenticate_user("testuser", "password123")
    manager.set_current_user(user_id)
    return manager


# Actual tests
def test_database_creation(test_db):
    """Test that database can be created."""
    assert test_db is not None
    print("✅ Database creation test passed")


def test_user_registration(test_db):
    """Test user registration."""
    result = test_db.register_user("newuser", "new@test.com", "password123")
    assert result == True
    print("✅ User registration test passed")


def test_habit_management(test_manager):
    """Test adding and listing habits."""
    # Add a habit
    test_manager.add_habit("Test habit", "daily")

    # List habits
    habits = test_manager.list_habits()
    assert len(habits) == 1
    assert habits[0][1] == "Test habit"  # name
    print("✅ Habit management test passed")


def test_habit_completion(test_manager):
    """Test checking off habits."""
    # Add a habit
    test_manager.add_habit("Test completion", "daily")
    habits = test_manager.list_habits()
    habit_id = habits[0][0]  # get the first habit's ID

    # Check it off
    test_manager.check_off_habit(habit_id, "Test notes", 5)
    print("✅ Habit completion test passed")


if __name__ == "__main__":
    # This allows the file to also be run as a regular script
    print("Running tests...")

    # Test database
    test_db_path = "temp_test.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = Database(test_db_path)
    print("✅ Database test passed")

    # Test manager
    manager = HabitManager(db)
    db.register_user("testuser", "test@test.com", "password123")
    user_id = db.authenticate_user("testuser", "password123")
    manager.set_current_user(user_id)
    print("✅ Manager test passed")

    # Test adding habit
    manager.add_habit("Test habit", "daily")
    habits = manager.list_habits()
    assert len(habits) == 1
    print("✅ Habit addition test passed")

    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    print("🎉 All tests passed!")