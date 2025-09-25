Backend Habit Tracker - IU Computer Science Project
A comprehensive Python-based habit tracking system featuring database persistence, functional programming for analytics, and object-oriented design for core entities.

📋 Table of Contents
Features

Project Structure

Installation

Usage

Development

Testing

API Documentation

Contributing

🌟 Features
Core Functionality
Habit Management: Create, update, delete, and track habits

Streak Tracking: Automatic streak calculation and maintenance

Progress Analytics: Comprehensive habit completion statistics

Data Persistence: SQLite database with efficient CRUD operations

CLI Interface: User-friendly command-line interface

Advanced Features
Modular Architecture: Separated concerns for maintainability

Functional Programming: Pure functions for analytics and data processing

Object-Oriented Design: Robust entity modeling with classes

Error Handling: Comprehensive exception management

Data Validation: Input validation and sanitization

🏗️ Project Structure
text
Habit_Tracker/
├── src/                    # Main source code
│   ├── habit.py           # Habit class definition and core logic
│   ├── habit_manager.py   # Habit management and business logic
│   ├── analytics.py       # Basic analytics functions
│   ├── advanced_analytics.py # Advanced statistical analysis
│   ├── db.py              # Database operations and connection handling
│   └── cli.py             # Command-line interface
├── tests/                 # Test suites and debugging tools
│   ├── unit/              # Unit tests (to be created)
│   ├── debug_db.py        # Database debugging utilities
│   ├── debug_auth.py      # Authentication debugging
│   ├── debug_simple.py    # Basic functionality tests
│   ├── debug_streak.py    # Streak calculation tests
│   ├── check_cli.py       # CLI interface validation
│   ├── check_encoding.py  # Encoding and data format tests
│   ├── check_syntax.py    # Syntax and code validation
│   ├── check_system.py    # System integration tests
│   ├── final_test_suite.py # Comprehensive test suite
│   └── generate_data_test.py # Test data generation
├── scripts/               # Utility scripts
│   └── deep_check.py      # Deep system analysis
├── data/                  # Database files and data storage
│   ├── debug.db          # Development database
│   └── final_test.db     # Testing database
├── docs/                  # Documentation (to be created)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
🚀 Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Step-by-Step Setup
Clone the Repository

bash
git clone https://github.com/JAVBITF89/Backend-Habit-Tracker-IU-Project.git
cd Backend-Habit-Tracker-IU-Project
Create Virtual Environment

bash
python -m venv venv
Activate Virtual Environment

Windows:

bash
venv\Scripts\activate
macOS/Linux:

bash
source venv/bin/activate
Install Dependencies

bash
pip install -r requirements.txt
💻 Usage
Running the Application
bash
# Navigate to src directory
cd src

# Run the main CLI interface
python cli.py

# Or run specific modules
python habit_manager.py
python analytics.py
Basic Commands
The CLI interface supports the following operations:

create habit - Add a new habit to track

list habits - View all tracked habits

complete habit - Mark a habit as completed

view analytics - Display habit statistics

export data - Export habit data to file

Example Session
bash
$ python cli.py
Welcome to Habit Tracker!

1. Create new habit
2. View all habits
3. Mark habit complete
4. View analytics
5. Exit

Choose an option: 1
Enter habit name: Exercise daily
Habit 'Exercise daily' created successfully!
🔧 Development
Technology Stack
Language: - **Python 3.13.5** (latest stable version)

Database: SQLite3

Architecture: Modular with separation of concerns

Programming Paradigms: OOP + Functional Programming

Code Architecture
Model Layer (habit.py): Data structures and business logic

Service Layer (habit_manager.py): Application logic and coordination

Persistence Layer (db.py): Database operations and storage

Presentation Layer (cli.py): User interface and interaction

Analytics Layer (analytics.py, advanced_analytics.py): Data analysis and reporting

Key Design Patterns
Repository Pattern: Database abstraction

Service Layer: Business logic encapsulation

Factory Pattern: Object creation

Strategy Pattern: Analytics algorithm selection

🧪 Testing
Running Tests
bash
# Run all test suites
cd tests
python final_test_suite.py

# Run specific test categories
python debug_db.py        # Database tests
python check_cli.py       # CLI functionality tests
python debug_streak.py    # Streak calculation tests
Test Categories
Unit Tests: Individual component testing

Integration Tests: Component interaction testing

System Tests: End-to-end functionality testing

Performance Tests: Speed and efficiency validation

Debugging Utilities
The project includes comprehensive debugging tools:

debug_db.py: Database connection and query debugging

debug_auth.py: Authentication and authorization tests

generate_data_test.py: Test data generation for scalability testing

📊 API Documentation
Core Classes
Habit Class
python
class Habit:
    def __init__(self, name, frequency, target):
        # Habit initialization
        pass
    
    def mark_complete(self):
        # Mark habit as completed
        pass
    
    def get_streak(self):
        # Calculate current streak
        pass
Analytics Functions
python
def calculate_completion_rate(habits):
    # Calculate overall completion percentage
    pass

def get_longest_streak(habits):
    # Identify the longest streak across all habits
    pass

def analyze_habit_patterns(habits):
    # Advanced pattern recognition
    pass
🤝 Contributing
Development Workflow
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

Code Standards
Follow PEP 8 style guide

Write docstrings for all functions and classes

Include unit tests for new functionality

Update documentation accordingly

📝 License
This project is developed as part of IU Computer Science curriculum. All rights reserved.

👨‍💻 Author
JULIUS FALANA - IU DATA Science Student

GitHub: @JAVBITF89

Project: Backend Habit Tracker - IU Project

🔄 Version History
v1.0.0 (Current)

Initial project setup

Core habit tracking functionality

SQLite database integration

Basic CLI interface

Comprehensive test suite

🆘 Support
For issues and questions:

Check existing documentation

Review test cases for usage examples

Open an issue on GitHub

Contact the development team