# File: utils/email_service.py
import smtplib
import ssl
import os
from pathlib import Path  # <--- NEW: Helps find files
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. Force Python to find .env in the main folder
# This says: "Go to this file's folder, then go up one level"
current_dir = Path(__file__).resolve().parent
main_dir = current_dir.parent
env_path = main_dir / ".env"

# 2. Load it explicitly
load_dotenv(dotenv_path=env_path)

# 3. Get values
SENDER_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")

# Debug Print: This will show up in your console so you know it loaded
# (It prints the first 2 chars of the password just to prove it exists)
if SENDER_EMAIL and APP_PASSWORD:
    print(f"[SYSTEM] Loaded Email Config: {SENDER_EMAIL} | Pass: {APP_PASSWORD[:2]}***")
else:
    print("[SYSTEM] ❌ ERROR: Could not load .env file")

def send_otp_email(receiver_email, otp):
    """
    Sends the OTP to the user's email address using Gmail SMTP.
    """
    subject = "Your Finance Manager OTP"
    body = f"""
    Hello,

    You requested a password reset for your Finance Manager account.
    
    Your OTP code is: {otp}
    
    If you did not request this, please ignore this email.
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True, "OTP sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {e}"