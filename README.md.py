# Habit Tracker - Python Application

A comprehensive habit tracking system built with Python, SQLite, and functional programming principles.

## Features

- **User Authentication**: Secure registration and login system
- **Habit Management**: Create daily/weekly habits with completions
- **Advanced Analytics**: Streak calculations using functional programming
- **Data Persistence**: SQLite database with proper relationships
- **CLI Interface**: User-friendly command-line interface

## Technical Architecture

### Core Components
- `habit.py`: OOP classes (BaseHabit, DailyHabit, WeeklyHabit, Completion)
- `db.py`: Database management with SQLite
- `habit_manager.py`: Business logic and habit operations
- `advanced_analytics.py`: FP-based analytics and streak calculations
- `cli.py`: Command-line interface

### Database Schema
Users (user_id, username, email, password_hash, created_at)
Habits (habit_id, user_id, name, type, created_at, is_active)
Completions (completion_id, habit_id, timestamp, notes, mood_score)

## Installation

1. Clone the repository
2. Install dependencies: `pip install questionary`
3. Run: `python cli.py`

## Usage

1. Register a new user or login with test credentials:
   - Username: `testuser`
   - Password: `testpass`

2. Add habits or use predefined habits
3. Track completions with optional notes and mood scores
4. View analytics including streaks and success rates

## Predefined Habits

- Drink eight glasses of water daily
- Spend 30 minutes exercising daily
- 30 Minutes of meditation daily
- Clean the house once weekly
- Call relatives once a week

## Testing

The project includes 4 weeks of test data with realistic completion patterns.

Run tests: `python test_advanced_analytics.py`