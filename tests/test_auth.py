from src.db import Database
import os


def test_user_authentication():
    """Test user registration and login."""

    # Use a test database to avoid affecting main data
    test_db_path = "test_habits.db"

    # Clean up any existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    test_db = Database(test_db_path)

    try:
        # Test registration
        result1 = test_db.register_user("testuser", "test@email.com", "password123")
        assert result1 == True, "Registration should succeed"

        # Test duplicate registration
        result2 = test_db.register_user("testuser", "test2@email.com", "password456")
        assert result2 == False, "Duplicate username should fail"

        # Test authentication
        user_id = test_db.authenticate_user("testuser", "password123")
        assert user_id is not None, "Valid login should succeed"
        assert user_id == 1, "First user should have ID 1"

        # Test wrong password
        user_id = test_db.authenticate_user("testuser", "wrongpassword")
        assert user_id is None, "Wrong password should fail"

        # Test non-existent user
        user_id = test_db.authenticate_user("nonexistent", "password123")
        assert user_id is None, "Non-existent user should fail"

        print("✅ All authentication tests passed!")

    finally:
        # Clean up
        import time
        time.sleep(0.1)
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
            except PermissionError:
                pass  # Ignore cleanup errors for tests


if __name__ == "__main__":
    test_user_authentication()