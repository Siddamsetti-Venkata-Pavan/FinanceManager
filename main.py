# File: main.py
import sys
import random
from ui.interface import show_welcome, show_menu, show_dashboard_menu, show_report
from data.database import initialize_db
from data.auth import register_user, login_user, get_user_recovery_info, reset_password, hash_password
from data.transactions import add_transaction, get_user_transactions, edit_transaction
from data.budgets import set_budget, check_budget_status
from utils.validators import validate_username, validate_password, validate_email
from rich.console import Console
from data.transactions import add_transaction, get_user_transactions, edit_transaction, delete_transaction # <--- ADD delete_transaction
from data.reports import get_monthly_report, get_yearly_report, get_all_time_report # <--- Updated Imports
from utils.email_service import send_otp_email # <--- NEW IMPORT
from data.backup import create_backup, list_backups, restore_backup

def run_dashboard(user_id):
    """
    The main dashboard loop where the user manages finances.
    Includes: Income, Expense, Budget Warnings, Reports, and Editing.
    """
    while True:
        show_dashboard_menu()
        choice = input("Select an option: ")
        
        # [1] ADD INCOME
        # [1] ADD INCOME
        if choice == '1':
            print("\n--- ADD INCOME ---")
            try:
                date_input = input("Date (YYYY-MM-DD) [Press Enter for Today]: ")
                amount = float(input("Enter Amount: "))
                category = input("Source (e.g. Salary): ")
                
                # If user just hit Enter, make it None so the function uses Today
                final_date = date_input if date_input.strip() != "" else None
                
                add_transaction(user_id, amount, category, "Income", final_date)
                print(">> ✅ Income saved!")
            except ValueError:
                print(">> ❌ Error: Invalid number.")

        # [2] ADD EXPENSE
        elif choice == '2':
            print("\n--- ADD EXPENSE ---")
            try:
                date_input = input("Date (YYYY-MM-DD) [Press Enter for Today]: ")
                amount = float(input("Enter Amount: "))
                category = input("Category (e.g. Food): ")
                
                final_date = date_input if date_input.strip() != "" else None
                
                # 1. Save
                add_transaction(user_id, amount, category, "Expense", final_date)
                print(">> ✅ Expense saved!")
                
                # 2. Check Budget
                spent, limit = check_budget_status(user_id, category)
                if limit and spent > limit:
                    Console().print(f"[bold red on white]⚠ WARNING: You have exceeded your {category} budget![/]")
                    print(f"   (Limit: ${limit} | Spent: ${spent})")
                    
            except ValueError:
                print(">> ❌ Error: Invalid number.")
        
        # [3] VIEW REPORTS (UPDATED)
        elif choice == '3':
            print("\n--- FINANCIAL REPORTS ---")
            print("[1] Monthly Report")
            print("[2] Yearly Report")
            print("[3] All-Time Summary")
            
            rep_choice = input("Select Report Type: ")
            
            if rep_choice == '1':
                try:
                    m = input("Enter Month (1-12): ")
                    y = input("Enter Year (e.g. 2025): ")
                    income, expense, balance = get_monthly_report(user_id, m, y)
                    print(f"\n>> REPORT FOR {m}/{y}")
                    show_report(income, expense, balance)
                except ValueError:
                    print(">> Invalid date.")
                    
            elif rep_choice == '2':
                try:
                    y = input("Enter Year (e.g. 2025): ")
                    income, expense, balance = get_yearly_report(user_id, y)
                    print(f"\n>> REPORT FOR YEAR {y}")
                    show_report(income, expense, balance)
                except ValueError:
                    print(">> Invalid year.")
                    
            elif rep_choice == '3':
                income, expense, balance = get_all_time_report(user_id)
                print("\n>> ALL-TIME SUMMARY")
                show_report(income, expense, balance)
            
            input("Press Enter to continue...")

        # [4] SET BUDGET (Keep same...)
        elif choice == '4':
            print("\n--- SET BUDGET LIMIT ---")
            cat = input("Category (e.g. Food): ")
            try:
                # Ask for the limit
                lim = float(input("Max Amount ($): "))
                
                # Save to database
                set_budget(user_id, cat, lim)
                print(f">> ✅ Budget for '{cat}' set to ${lim}")
                
            except ValueError:
                print(">> ❌ Invalid amount. Please enter a number.")
            
            input("Press Enter to continue...") 

        # [5] MANAGE TRANSACTIONS (Edit OR Delete)
        elif choice == '5':
            print("\n--- MANAGE TRANSACTIONS ---")
            
            # 1. Fetch data
            rows = get_user_transactions(user_id)
            
            if not rows:
                print(">> No transactions found.")
            else:
                # 2. Show the list so user knows the ID
                print(f"{'ID':<5} {'Date':<12} {'Type':<10} {'Amount':<10} {'Category'}")
                print("-" * 60)
                for r in rows:
                    # r = (id, date, category, amount, type)
                    print(f"{r[0]:<5} {r[1]:<12} {r[4]:<10} ${r[3]:<9} {r[2]}")
                print("-" * 60)
                
                # 3. Ask for action
                print("\nWhat would you like to do?")
                print("[E] Edit a transaction")
                print("[D] Delete a transaction")
                print("[C] Cancel")
                action = input("Select Option (E/D/C): ").upper()
                
                # --- EDIT LOGIC ---
                if action == 'E':
                    try:
                        t_id = int(input("Enter ID to edit: "))
                        new_amt = float(input("New Amount: "))
                        new_cat = input("New Category: ")
                        success, msg = edit_transaction(t_id, user_id, new_amt, new_cat)
                        print(f">> {'✅' if success else '❌'} {msg}")
                    except ValueError:
                        print(">> ❌ Invalid input.")

                # --- DELETE LOGIC ---
                elif action == 'D':
                    try:
                        t_id = int(input("Enter ID to DELETE: "))
                        confirm = input(f"Are you sure you want to delete ID {t_id}? (y/n): ")
                        
                        if confirm.lower() == 'y':
                            success, msg = delete_transaction(t_id, user_id)
                            print(f">> {'✅' if success else '❌'} {msg}")
                        else:
                            print(">> ⚠ Operation cancelled.")
                    except ValueError:
                        print(">> ❌ Invalid ID.")
                
                elif action == 'C':
                    print(">> returning to menu...")
                
                else:
                    print(">> ❌ Invalid selection.")
            
            # Important: Pause so user can read the result before screen clears
            input("Press Enter to continue...")

        # [6] VIEW TRANSACTION HISTORY (NEW!)
        elif choice == '6':
            print("\n--- TRANSACTION HISTORY ---")
            rows = get_user_transactions(user_id)
            
            if not rows:
                print(">> No transactions found.")
            else:
                # Use Rich Table for a better look
                from rich.table import Table
                table = Table(title="📜 Transaction History")
                
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Date", style="magenta")
                table.add_column("Type", style="bold")
                table.add_column("Category", style="blue")
                table.add_column("Amount", justify="right", style="green")
                
                for r in rows:
                    # r = (id, date, category, amount, type)
                    # We format amount based on type
                    amt_str = f"${r[3]:.2f}"
                    type_str = r[4]
                    if type_str == "Expense":
                        amt_str = f"-${r[3]:.2f}"
                        table.add_row(str(r[0]), r[1], f"[red]{type_str}[/]", r[2], f"[red]{amt_str}[/]")
                    else:
                        table.add_row(str(r[0]), r[1], f"[green]{type_str}[/]", r[2], f"[green]{amt_str}[/]")
                        
                Console().print(table)
            
            input("Press Enter to continue...")

        # [7] BACKUP & RESTORE
        elif choice == '7':
            print("\n--- DATA MANAGEMENT ---")
            print("[1] Create New Backup")
            print("[2] Restore from Backup")
            
            sub_choice = input("Select Option: ")
            
            # CREATE BACKUP
            if sub_choice == '1':
                print(">> Creating backup...")
                success, msg = create_backup()
                print(f">> {'✅' if success else '❌'} {msg}")
            
            # RESTORE BACKUP
            elif sub_choice == '2':
                backups = list_backups()
                if not backups:
                    print(">> ❌ No backups found.")
                else:
                    print("\nAvailable Backups:")
                    for i, filename in enumerate(backups, 1):
                        print(f"[{i}] {filename}")
                    
                    try:
                        sel = int(input("Select Backup to Restore (Number): "))
                        if 1 <= sel <= len(backups):
                            target_file = backups[sel-1]
                            confirm = input(f"⚠ WARNING: This will overwrite ALL current data with '{target_file}'.\nAre you sure? (yes/no): ")
                            
                            if confirm.lower() == 'yes':
                                success, msg = restore_backup(target_file)
                                print(f">> {'✅' if success else '❌'} {msg}")
                                if success:
                                    # Force exit so the database reloads cleanly
                                    sys.exit()
                            else:
                                print(">> Operation cancelled.")
                        else:
                            print(">> Invalid selection.")
                    except ValueError:
                        print(">> Invalid input.")
            
            input("Press Enter to continue...")

        # [8] LOGOUT
        elif choice == '8':
            print("\nLogging out...")
            break
            
        else:
            print("Invalid choice.")

def handle_forgot_password():
    """Handles OTP and Security Question logic"""
    print("\n--- ACCOUNT RECOVERY ---")
    username = input("Enter your Username: ")
    
    user_data = get_user_recovery_info(username)
    if not user_data:
        print(">> ❌ User not found.")
        return

    email, question, stored_answer_hash = user_data
    
    print(f"\nUser found! Recovery Options for {username}:")
    print("[1] Send OTP to Email")
    print("[2] Answer Security Question")
    
    choice = input("Select Option: ")
    verified = False
    
    # --- OPTION 1: EMAIL OTP ---
    if choice == '1':
        otp = str(random.randint(100000, 999999))
        
        print(f"\n[SYSTEM] Sending OTP to {email}...")
        print("Please wait...") # Email takes 1-2 seconds to send
        
        # --- NEW CODE: SEND REAL EMAIL ---
        success, msg = send_otp_email(email, otp)
        
        if success:
            print(f">> ✅ OTP sent! Check your inbox.")
            
            # Now ask user to enter it
            user_otp = input("Enter the OTP you received: ")
            if user_otp == otp:
                verified = True
            else:
                print(">> ❌ Invalid OTP.")
        else:
            print(f">> ❌ Error: {msg}")
            print(">> (Make sure you have internet and correct email settings)")
            
    elif choice == '2':
        print(f"\nSecurity Question: {question}")
        ans = input("Your Answer: ")
        if hash_password(ans.lower()) == stored_answer_hash:
            verified = True
        else:
            print(">> ❌ Wrong Answer.")
    
    if verified:
        print("\n>> ✅ Identity Verified!")
        while True:
            new_pass = input("Enter New Password: ")
            valid, msg = validate_password(new_pass)
            if not valid:
                print(f">> ❌ {msg}")
                continue
            reset_password(username, new_pass)
            print(">> ✅ Password updated! Please login.")
            break

def main():
    initialize_db()
    
    while True:
        show_welcome()
        show_menu()
        
        choice = input("Select an option: ")
        
        # --- LOGIN ---
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            user_id = login_user(username, password)
            
            if user_id:
                run_dashboard(user_id)
            else:
                print("\n[!] Login Failed.")
                retry = input("Forgot Password? (y/n): ")
                if retry.lower() == 'y':
                    handle_forgot_password()

        # --- REGISTER ---
        elif choice == '2':
            print("\n--- REGISTER ---")
            
            # Username Check
            username = input("Choose Username: ")
            valid, msg = validate_username(username)
            if not valid:
                print(f">> ❌ {msg}")
                input("Press Enter...")
                continue
                
            # Email Check
            email = input("Enter Email: ")
            valid, msg = validate_email(email)
            if not valid:
                print(f">> ❌ {msg}")
                input("Press Enter...")
                continue

            # Password Check
            print("Password Rules: 8+ chars, 1 Upper, 1 Lower, 1 Number, 1 Special Char")
            password = input("Choose Password: ")
            valid, msg = validate_password(password)
            if not valid:
                print(f">> ❌ {msg}")
                input("Press Enter...")
                continue
            
            # Security Question
            print("\n--- ACCOUNT RECOVERY SETUP ---")
            question = input("Create a Security Question: ")
            answer = input("Answer: ")

            success, message = register_user(username, password, email, question, answer)
            print(f"\n>> {message}")
            input("Press Enter...")

        # --- EXIT ---
        elif choice == '4':
            sys.exit()

        # --- FORGOT PASSWORD ---
        elif choice == '3':
            handle_forgot_password()
            input("Press Enter...")

        else:
            print("Invalid choice.")
            input()

if __name__ == "__main__":
    main()