def inspect_cli_file():
    """See what's actually in the cli.py file."""

    print("=== INSPECTING CLI.PY ===")

    # Read the cli.py file
    try:
        with open('cli.py', 'r') as f:
            content = f.read()

        # Look for class definitions
        lines = content.split('\n')
        class_lines = [line for line in lines if line.strip().startswith('class ')]

        if class_lines:
            print("Classes found in cli.py:")
            for class_line in class_lines:
                print(f"  {class_line.strip()}")
        else:
            print("❌ No classes found in cli.py")

        # Look for function definitions
        function_lines = [line for line in lines if
                          line.strip().startswith('def ') and not line.strip().startswith('def __')]

        if function_lines:
            print("\nFunctions found in cli.py:")
            for func_line in function_lines:
                print(f"  {func_line.strip()}")
        else:
            print("❌ No functions found in cli.py")

    except FileNotFoundError:
        print("❌ cli.py file not found!")
    except Exception as e:
        print(f"❌ Error reading file: {e}")


if __name__ == "__main__":
    inspect_cli_file()