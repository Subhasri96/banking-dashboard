
# Banking Dashboard – Flask + PostgreSQL

A simple, full-stack **Banking Dashboard** built with **Flask**, **PostgreSQL**, and **HTML/JavaScript**.  
It allows users to **register, log in, add transactions (credit/debit)**, and view a dynamic balance dashboard — all backed by session-based authentication.

---

## Features

-  **User Registration & Login**
  - Secure password hashing with Werkzeug
  - Session-based authentication

-  **Add & Track Transactions**
  - Supports both **Credit** and **Debit**
  - Automatically calculates running balance

-  **Dynamic Dashboard**
  - Displays total balance and transaction history
  - Real-time updates after each transaction

-  **Session Management**
  - User stays logged in via Flask sessions
  - Logout clears session safely

-  **Cross-Origin Ready**
  - CORS enabled for frontend-backend communication

---

## Tech Stack
 Layer    : Technology 
-------|-------------
 Backend : Flask (Python) 
 Database: PostgreSQL 
 ORM  :LAlchemy 
 Auth | Flask Sessions + Password Hashing |
| Config | python-dotenv |
| Deployment Ready | Flask-CORS for API access |

---

##  Project Structure

banking-dashboard/
│
├── backend/
│ ├── app.py # Flask backend with all routes and DB models
│ ├── requirements.txt # Dependencies
│ └── .env # Database credentials and secret key
│
├── frontend/
│ ├── register.html # Registration page
│ ├── login.html # Login page
│ └── dashboard.html # Dashboard with transactions
│
└── README.md

## Environment Setup

### Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate     
pip install -r requirements.txt
DATABASE_URL=postgresql://postgres:shubha_2021@localhost:5432/bankdb
SECRET_KEY=f9a3b7e178d4e9cd4737b0b62817f5a013dbd1a2a79a4e3139b9f57f42fd6c87

# Database Setup
Then open the Python shell or run:
python
>>> from app import db
>>> db.create_all()
>>> exit()

This creates user and transaction tables inside bankdb.
# Running the app
Start Flask server:
python app.py( see  * Running on http://127.0.0.1:5000/)
open the HTML files directly in your browser,
or start a simple local server:
python -m http.server 5500
Register: http://127.0.0.1:5500/register.html

Login: http://127.0.0.1:5500/login.html

Dashboard: http://127.0.0.1:5500/dashboard.html