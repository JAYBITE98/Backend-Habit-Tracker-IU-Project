def main():
    print("=== QUICK CHECK ===")
    print("This is running as a regular Python script!")

    # Test a simple import
    try:
        import db
        print("✅ db.py can be imported")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()