# Student Mark Registration System

A Django-based web application developed to manage student records, modules, coursework marks, and data visualization using an SQLite database.

## Features

- User login and signup
- Add student information
- Add module information
- Input coursework marks
- Update existing marks
- View student marks
- Calculate total marks
- Search records by module
- Visualize student data
- Store data using SQLite
- Logout functionality

## Technologies Used

- Python
- Django
- SQLite
- SQL
- HTML
- CSS
- Matplotlib

## Project Structure

- `mark_registration_system/` - Main Django project
- `marks/` - Main Django application
- `templates/` - HTML templates
- `static/` - CSS files
- `migrations/` - Django database migrations
- `db.sqlite3` - SQLite database
- `manage.py` - Django management file

## How to Run the Project

1. Open the project in VS Code.

2. Activate the virtual environment.

3. Install Django if required:

```bash
pip install django
```

4. Go to the folder containing `manage.py`.

5. Run the Django development server:

```bash
python manage.py runserver
```

6. Open the following address in your browser:

```text
http://127.0.0.1:8000/
```
