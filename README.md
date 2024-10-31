
# MAD2 Library Management System (LMS)

The Library Management System (LMS) is a comprehensive web application designed to streamline library operations, enabling users to register, search, and request eBooks, and allowing librarians to manage book inventories and user requests. Key features include JWT-based authentication, user and librarian roles, automated notifications, and efficient background task handling.

## Project Structure

```
MAD2
│
├── code
│   ├── Back           # Backend code for LMS
│   └── front-end      # Frontend code for LMS
│
└── Report             # Project report and documentation
```

## Prerequisites

Ensure you have Node.js and Python and Vue3.js CLI installed on your system.

## Setup Instructions

### Step 1: Install Frontend Dependencies

```bash
npm install
```

### Step 2: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

### Backend Setup

Open the backend terminal:

```bash
cd code/Back
python app.py
```

### Frontend Setup

In a new terminal, run the frontend server:

```bash
cd code/front-end
npm run serve
```

## Additional Services

1. **Redis Server**

   In WSL, start Redis:

   ```bash
   redis-server
   ```

2. **Celery Workers and Scheduler**

   - **Worker Terminal**: Open a new terminal and run the Celery worker:

   ```bash
   celery -A app.celery worker --loglevel=info
   ```

   - **Scheduler Terminal**: Open another terminal for Celery beat scheduler:

   ```bash
   celery -A app.celery beat --loglevel=info
   ```

## Key Features

- **User Functionality**: Users can register, log in, search and download eBooks, and receive automated email notifications for updates.
- **Librarian Module**: Librarians manage books, approve user access requests, and generate reports via a dedicated dashboard.
- **Security**: JWT-based authentication for secure access control.
- **Asynchronous Processing**: Redis and Celery handle background tasks efficiently, ensuring smooth user experience.
