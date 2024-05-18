# Property Listing Web App

## Description
This is a property listing web application where users can view properties listed by various sellers. Users can filter properties by type and search for properties based on location, title, or description.

## Features
- View properties listed by sellers
- Filter properties by type (e.g., apartment, house, condo, etc.)
- Search for properties based on location, title, or description
- Pagination for browsing through property listings
- View details of the property owner upon expressing interest in a property

## Tech Stack
- **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
- **Backend:** Python (Django)
- **Database:** SQLite (default for Django)
- **Deployment:** [Optional: Mention deployment platform if applicable]

## Setup
To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Jatin-tec/Rentify.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Rentify
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
    ```bash
    venv\Scripts\activate
    ```
    - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations to create database tables:
    ```bash
    python manage.py migrate
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. Access the application in your web browser at `http://127.0.0.1:8000/`

## Contributors
- [Your Name](https://github.com/Jatin-tec)
