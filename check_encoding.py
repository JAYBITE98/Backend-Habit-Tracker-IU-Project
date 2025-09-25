def check_file_encoding():
    print("=== CHECKING FILE ENCODING ===")

    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open('cli.py', 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✅ File can be read with {encoding} encoding")
                print(f"   File size: {len(content)} characters")
                break
            except UnicodeDecodeError:
                print(f"❌ Failed with {encoding} encoding")

    except FileNotFoundError:
        print("❌ cli.py file not found!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_file_encoding()