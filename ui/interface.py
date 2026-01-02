# File: ui/interface.py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table # <--- Add this with other imports

# Initialize the Console (This is the screen)
console = Console()

def show_welcome():
    """Prints a beautiful welcome banner"""
    console.clear() # Wipes the screen clean
    
    # Create a "Panel" (A box with a border)
    title_text = Text("PERSONAL FINANCE MANAGER", justify="center", style="bold cyan")
    welcome_panel = Panel(
        title_text,
        subtitle="Manage your money like a pro",
        border_style="green",
        padding=(1, 5) # Adds space inside the box
    )
    
    console.print(welcome_panel)
    console.print("\n") # Add an empty line

def show_menu():
    """Prints the main menu options"""
    console.print("[1] [bold green]Login[/bold green]")
    console.print("[2] [bold blue]Register[/bold blue]")
    console.print("[3] [bold yellow]Forgot Password[/bold yellow]")
    console.print("[4] [bold red]Exit[/bold red]")
    console.print("\n")
# File: ui/interface.py (Add this to the bottom)

# File: ui/interface.py (Update this function)

# File: ui/interface.py

def show_dashboard_menu():
    console.print("\n[bold cyan]--- USER DASHBOARD ---[/bold cyan]")
    console.print("[1] Add Income 💰")
    console.print("[2] Add Expense 💸")
    console.print("[3] View Reports (Monthly/Yearly) 📊")
    console.print("[4] Set Budget Limits 🛡️")
    console.print("[5] Manage Transactions (Edit/Delete) ✏️")
    console.print("[6] View Transaction History 📜")
    console.print("[7] Backup & Restore Data 💾")  # <--- NEW
    console.print("[8] Logout")                  # <--- SHIFTED           # Shifted down              # <--- CHANGED NUMBER

# File: ui/interface.py (Add to bottom)

def show_report(income, expense, balance):
    """Displays the financial summary in a nice table"""
    
    # Create a table with a title
    table = Table(title="💰 Monthly Financial Report", show_header=True, header_style="bold magenta")
    
    # Add columns
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Amount ($)", justify="right", style="green")
    
    # Add rows
    table.add_row("Total Income", f"+ {income:.2f}")
    table.add_row("Total Expenses", f"- {expense:.2f}", style="red")
    table.add_row("NET SAVINGS", f"= {balance:.2f}", style="bold white on blue")
    
    console.print("\n")
    console.print(table)
    console.print("\n")