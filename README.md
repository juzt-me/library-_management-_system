# Library Management System

A web-based Library Management System built with Django and MongoDB, featuring user authentication, book management, and lending operations.

## Features

- User Authentication & Authorization
- Book Management (Add, Update, Delete)
- Member Management
- Book Lending System
- Search and Filter Books
- Email Notifications
- Responsive UI with Bootstrap

## Prerequisites

- Python 3.7 or higher
- MongoDB 4.0 or higher
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add the following:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=library_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to access the application.

## Usage

1. Register as a new member or log in with existing credentials
2. Browse available books in the library
3. Search for books by title, author, or category
4. Borrow books (requires authentication)
5. View borrowed books and return dates in the dashboard
6. Return books and view any applicable fines
7. Administrators can manage books and members through the admin interface

## Admin Interface

Access the admin interface at http://localhost:8000/admin with your superuser credentials to:
- Manage books (add, edit, delete)
- Manage members
- View and manage lending records
- Monitor fines and overdue books

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. "# library-_management-_system" 
"# library-_management-_system" 
"# library-_management-_system" 
"# library-_management-_system" 
