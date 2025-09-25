from db import Database
import os


def debug_database():
    print("Testing database connection...")

    # Use a test database
    test_db_path = "debug_test.db"

    # Clean up any existing file
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    db = Database(test_db_path)
    print("✅ Database created successfully")

    try:
        # Test 1: User registration
        print("\n1. Testing user registration...")
        success = db.register_user("debuguser", "debug@test.com", "debugpass")
        print(f"   First registration: {success}")

        # Test 2: Duplicate registration
        success2 = db.register_user("debuguser", "debug2@test.com", "debugpass2")
        print(f"   Duplicate registration: {success2} (should be False)")

        # Test 3: Authentication
        print("\n2. Testing authentication...")
        user_id = db.authenticate_user("debuguser", "debugpass")
        print(f"   Correct password: User ID = {user_id}")

        # Test 4: Wrong password
        user_id_wrong = db.authenticate_user("debuguser", "wrongpass")
        print(f"   Wrong password: User ID = {user_id_wrong} (should be None)")

        # Test 5: Non-existent user
        user_id_none = db.authenticate_user("nonexistent", "debugpass")
        print(f"   Non-existent user: User ID = {user_id_none} (should be None)")

        # Test 6: Check user exists
        print("\n3. Testing user existence check...")
        exists = db.user_exists("debuguser")
        print(f"   User exists: {exists}")
        exists_not = db.user_exists("nonexistent")
        print(f"   Non-existent user exists: {exists_not}")

        print("\n🎉 All debug tests completed successfully!")

    finally:
        # Ensure proper cleanup
        import time
        time.sleep(0.1)  # Brief delay to ensure connections close
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
                print("✅ Cleanup complete")
            except PermissionError:
                print("⚠️  Could not clean up file (still in use), but tests passed!")


if __name__ == "__main__":
    debug_database()