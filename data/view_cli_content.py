def view_cli_content():
    print("=== VIEWING CLI CONTENT ===")

    try:
        # Try reading as binary to see raw content
        with open('cli.py', 'rb') as f:
            raw_content = f.read()

        print(f"File size: {len(raw_content)} bytes")

        # Try to decode with error handling
        try:
            content = raw_content.decode('utf-8')
            print("✅ Successfully decoded as UTF-8")
        except UnicodeDecodeError:
            content = raw_content.decode('latin-1')
            print("✅ Successfully decoded as Latin-1")

        # Show first 500 characters to see the structure
        print("\n=== FIRST 500 CHARACTERS ===")
        print(content[:500])

        # Show last 200 characters
        print("\n=== LAST 200 CHARACTERS ===")
        print(content[-200:])

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    view_cli_content()