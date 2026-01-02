import smtplib
import ssl

# --- PASTE YOUR DETAILS DIRECTLY HERE ---
TEST_EMAIL = "venkat181199@gmail.com"  # e.g. venkat@gmail.com
TEST_PASSWORD = "gyrqczkbnzzodcve"        # Paste the 16-char code here (no spaces)

print(f"1. Attempting to connect as: {TEST_EMAIL}")
print(f"2. Using Password length: {len(TEST_PASSWORD)}")

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        print("3. Connecting to Gmail Server...")
        server.login(TEST_EMAIL, TEST_PASSWORD)
        print("✅ SUCCESS! The password works.")
        print(">> The issue is your .env file is not being read correctly.")
except Exception as e:
    print("\n❌ FAILURE! Google rejected these specific credentials.")
    print(f"Error Message: {e}")