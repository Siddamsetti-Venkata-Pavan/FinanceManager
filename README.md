# 💰 Personal Finance Manager (CLI)

A secure, terminal-based application to track income, expenses, and budgets. Built with Python, SQLite, and Rich.

## 🚀 Features
* **Secure Authentication:** User login with Hashed Passwords (SHA-256).
* **OTP Recovery:** Forgot Password? Reset it via real Email OTP (Gmail SMTP).
* **Smart Budgeting:** Set category limits and get live warnings when overspending.
* **Visual Reports:** View monthly/yearly financial summaries in color-coded tables.
* **Data Safety:** Built-in Backup & Restore functionality.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Database:** SQLite
* **UI:** Rich (for terminal formatting)
* **Security:** Hashlib, Smtplib, Dotenv

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/FinanceManager.git](https://github.com/Siddamsetti-Venkata-Pavan/FinanceManager.git)
    cd FinanceManager
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory and add your email credentials:
    ```text
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_app_password
    ```

4.  **Run the App**
    ```bash
    python main.py
    ```

