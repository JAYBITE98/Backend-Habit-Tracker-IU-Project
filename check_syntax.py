import sys
import importlib


def check_file_syntax(filename):
    """Check if a Python file has syntax errors."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # Try to compile the code
        compile(source_code, filename, 'exec')
        print(f"✅ {filename}: No syntax errors")
        return True
    except SyntaxError as e:
        print(f"❌ {filename}: Syntax error on line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  {filename}: Other error: {e}")
        return False


# Check all our files
files_to_check = [
    'db.py',
    'habit.py',
    'habit_manager.py',
    'analytics.py',
    'cli.py',
    'test_data_generator.py'
]

print("🔍 Checking all files for syntax errors...")
print("=" * 50)

all_good = True
for filename in files_to_check:
    try:
        if check_file_syntax(filename):
            print(f"   {filename} - OK")
        else:
            all_good = False
            print(f"   {filename} - ERROR")
    except FileNotFoundError:
        print(f"❌ {filename}: File not found")
        all_good = False

print("=" * 50)
if all_good:
    print("🎉 All files passed syntax check!")
else:
    print("⚠️  Some files have errors")

# Test basic imports
print("\n🔍 Testing imports...")
try:
    from db import Database
    from habit_manager import HabitManager

    print("✅ Basic imports work")
except ImportError as e:
    print(f"❌ Import error: {e}")