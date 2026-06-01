# GenAI Health Assistant

A comprehensive Generative AI platform for transformative healthcare, featuring an AI chatbot, symptom checker, medical image analysis, and drug information system.

## 🚀 Features
- **AI Chatbot**: Intelligent medical assistant powered by Google Gemini.
- **Symptom Checker**: ML-based disease prediction from user symptoms.
- **Image Analysis**: AI-driven analysis of medical scans and images.
- **Drug Info**: Database of common medications and their usages.
- **Admin Dashboard**: Custom-built premium panel for managing users and system data.

---

## 💻 Setup Instructions for Other Laptops

Follow these exact steps to get the project running on a new machine.

### 1. Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **MySQL Server**: Installed and running (XAMPP, WAMP, or standalone MySQL).

### 2. Clone and Prepare Environment
Extract the project folder and open a terminal (Cmd or PowerShell) inside it.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup (MySQL)
1. Open your MySQL client (e.g., phpMyAdmin or MySQL Workbench).
2. Create a new database named `genai_health`:
   ```sql
   CREATE DATABASE genai_health;
   ```

### 4. Configuration (.env)
Create a file named `.env` in the root directory (if not already present) and add the following:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DB_NAME=genai_health
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
SECRET_KEY=django-insecure-genai-health-assistant-key-12345
```
> [!IMPORTANT]
> Replace `your_mysql_password` with your actual MySQL root password.
> Get a free API key from [Google AI Studio](https://aistudio.google.com/) for `GEMINI_API_KEY`.

### 5. Initialize the Application
Run the following commands in order to set up the database schema and sample data:

```bash
# Apply database migrations
python manage.py migrate

# Initialize sample data and create admin user
python init_db.py
```
> [!NOTE]
> The `init_db.py` script creates a default admin account:
> - **Username**: `admin`
> - **Password**: `admin123`

### 6. Run the Application
Start the development server:
```bash
python manage.py runserver
```
Access the application at: `http://127.0.0.1:8000/`

---

## 🛠️ Management & Administration
The project includes a custom **Admin Dashboard** for authorized staff members.
- **Link**: Visible in the sidebar after logging in as admin.
- **Capabilities**: Manage users, view chat logs, review predictions, and audit image analyses.

---

## 📂 Troubleshooting
- **MySQL Connection Error**: Ensure MySQL service is running and the credentials in `.env` match your local setup.
- **Gemini Response Error**: Verify your `GEMINI_API_KEY` is valid and you have an active internet connection.
- **Static Files**: If images/styles don't load, run `python manage.py collectstatic`.
