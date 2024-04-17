import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Constants for expense categories
CATEGORIES = ["Food", "Transportation", "Entertainment", "Others"]

# Data structure to store expenses
expenses = []
recurring_expenses = []

def add_expense():
  """Function to add a new expense"""
  while True:
    try:
      amount = float(input("Enter expense amount: "))
      if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
      break
    except ValueError as e:
      print(f"Error: {e}")

  description = input("Enter expense description: ")
  if not description:
    print("Error: Description cannot be empty.")
    return

  category = int(input("Select a category:\n" + "\n".join(f"{i+1}. {category}" for i, category in enumerate(CATEGORIES)) + "\n"))
  if 1 <= category <= len(CATEGORIES):
    category_name = CATEGORIES[category - 1]
    expense = {"amount": amount, "description": description, "category": category_name, "date": datetime.now().strftime("%Y-%m-%d")}
    expenses.append(expense)
    print("Expense added successfully!")
  else:
    print("Invalid category selected.")

def add_recurring_expense():
  """Function to add a recurring expense"""
  while True:
    try:
      amount = float(input("Enter expense amount: "))
      if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
      break
    except ValueError as e:
      print(f"Error: {e}")

  description = input("Enter expense description: ")
  if not description:
    print("Error: Description cannot be empty.")
    return

  category = int(input("Select a category:\n" + "\n".join(f"{i+1}. {category}" for i, category in enumerate(CATEGORIES)) + "\n"))
  if 1 <= category <= len(CATEGORIES):
    category_name = CATEGORIES[category - 1]
  else:
    print("Invalid category selected.")
    return

  frequency = input("Enter frequency (weekly, monthly, yearly): ")
  if frequency not in ["weekly", "monthly", "yearly"]:
    print("Invalid frequency. Please choose from 'weekly', 'monthly', or 'yearly'.")
    return

  recurring_expense = {"amount": amount, "description": description, "category": category_name, "frequency": frequency}
  recurring_expenses.append(recurring_expense)
  print("Recurring expense added successfully!")

def view_expenses(start_date=None, end_date=None, category=None, keyword=None):
  """Function to view expenses"""
  if not expenses:
    print("No expenses found.")
    return

  filtered_expenses = expenses.copy()
  if start_date and end_date:
    try:
      start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
      end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
      filtered_expenses = [expense for expense in filtered_expenses if start_date <= datetime.strptime(expense["date"], "%Y-%m-%d").date() <= end_date]
    except ValueError as e:
      print(f"Error: {e}")
      return

  if category:
    filtered_expenses = [expense for expense in filtered_expenses if expense["category"] == category]

  if keyword:
    filtered_expenses = [expense for expense in filtered_expenses if keyword.lower() in expense["description"].lower()]

  print("\nExpenses:")
  for expense in filtered_expenses:
    print(f"{expense['date']} - {expense['description']} (Category: {expense['category']}) - ${expense['amount']:.2f}")

def view_monthly_summary():
  """Function to view monthly expense summary"""
  if not expenses:
    print("No expenses found.")
    return

  monthly_summary = {}
  for expense in expenses:
    month_year = expense["date"].split("-")[:2]
    month_year = "-".join(month_year)
    if month_year in monthly_summary:
      monthly_summary[month_year] += expense["amount"]
    else:
      monthly_summary[month_year] = expense["amount"]

  print("\nMonthly Expense Summary:")
  for month_year, total in monthly_summary.items():
    print(f"{month_year}: ${total:.2f}")

def view_category_summary():
  """Function to view category-wise expense summary"""
  if not expenses:
    print("No expenses found.")
    return

  category_summary = {category: 0 for category in CATEGORIES}
  for expense in expenses:
    category_summary[expense["category"]] += expense["amount"]

  print("\nCategory-wise Expense Summary:")
  for category, total in category_summary.items():
    print(f"{category}: ${total:.2f}")

def visualize_expenses(start_date=None, end_date=None, chart_type="bar"):
  """Function to visualize expenses using charts"""
  if not expenses:
    print("No expenses found.")
    return

  filtered_expenses = expenses
  if start_date and end_date:
    try:
      start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
      end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
      filtered_expenses = [expense for expense in expenses if start_date <= datetime.strptime(expense["date"], "%Y-%m-%d").date() <= end_date]
    except ValueError as e:
      print(f"Error: {e}")
      return

  category_totals = {category: 0 for category in CATEGORIES}
  for expense in filtered_expenses:
    category_totals[expense["category"]] += expense["amount"]

  categories = list(category_totals.keys())
  amounts = list(category_totals.values())

  if chart_type == "bar":
    plt.bar(categories, amounts)
    plt.xlabel("Categories")
    plt.ylabel("Total Expenses")
    plt.title("Category-wise Expense Visualization")
  elif chart_type == "pie":
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.axis("equal")
    plt.title("Category-wise Expense Visualization")
  elif chart_type == "line":
    dates = sorted(set([expense["date"] for expense in filtered_expenses]))
    date_totals = {date: sum(expense["amount"] for expense in filtered_expenses if expense["date"] == date) for date in dates}
    plt.plot(dates, [date_totals[date] for date in dates])
    plt.xlabel("Date")
    plt.ylabel("Total Expenses")
    plt.title("Daily Expense Visualization")
  else:
    print("Invalid chart type. Choose from 'bar', 'pie', or 'line'.")
    return

  plt.show()

def save_expenses():
  """Function to save expenses to a CSV file"""
  filename = "expenses.csv"
  with open(filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["date", "description", "category", "amount"])
    writer.writeheader()
    writer.writerows(expenses)
  print(f"Expenses saved to '{filename}'.")

def load_expenses():
  """Function to load expenses from a CSV file"""
  global expenses
  filename = "expenses.csv"
  try:
    with open(filename, mode="r") as file:
      reader = csv.DictReader(file)
      expenses = list(reader)
    print(f"Expenses loaded from '{filename}'.")
  except FileNotFoundError:
    print(f"'{filename}' not found. Starting with an empty expense list.")
def process_recurring_expenses():
  today = datetime.now().date()
  for recurring_expense in recurring_expenses:
    last_expense_date = max((expense["date"] for expense in expenses if expense["description"] == recurring_expense["description"]), default=None)
    last_expense_date = datetime.strptime(last_expense_date, "%Y-%m-%d").date() if last_expense_date else None # Convert string to date

    if recurring_expense["frequency"] == "weekly":
      if last_expense_date is None or (today - last_expense_date).days >= 7:
        # ... 
        expense = {
          "amount": recurring_expense["amount"],
          "description": recurring_expense["description"],
          "category": recurring_expense["category"],
          "date": today.strftime("%Y-%m-%d")
        }
        expenses.append(expense)
    elif recurring_expense["frequency"] == "monthly":
      last_expense_date = max([datetime.strptime(expense["date"], "%Y-%m-%d").date() for expense in expenses if expense["description"] == recurring_expense["description"]], default=None)
      if last_expense_date is None or (today.replace(day=1) - last_expense_date.replace(day=1)).days >= 30:
        expense = {
          "amount": recurring_expense["amount"],
          "description": recurring_expense["description"],
          "category": recurring_expense["category"],
          "date": today.strftime("%Y-%m-%d")
        }
        expenses.append(expense)
    elif recurring_expense["frequency"] == "yearly":
      last_expense_date = max([datetime.strptime(expense["date"], "%Y-%m-%d").date() for expense in expenses if expense["description"] == recurring_expense["description"]], default=None)
      if last_expense_date is None or (today.year - last_expense_date.year) >= 1:
        expense = {
          "amount": recurring_expense["amount"],
          "description": recurring_expense["description"],
          "category": recurring_expense["category"],
          "date": today.strftime("%Y-%m-%d")
        }
        expenses.append(expense)
def main():
    load_expenses()  # Load any expenses from CSV

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. Add Recurring Expense")
        print("3. View Expenses")
        print("4. View Monthly Summary")
        print("5. View Category Summary")
        print("6. Visualize Expenses")
        print("7. Save Expenses")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            add_recurring_expense()
        elif choice == '3':
            view_expenses()  # Add options for filtering here
        elif choice == '4':
            view_monthly_summary()
        elif choice == '5':
            view_category_summary()
        elif choice == '6':
            visualize_expenses()  # Add options for start/end dates, chart type
        elif choice == '7':
            save_expenses()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

    process_recurring_expenses()  # Process recurring expenses before exit

if __name__ == "__main__":
    main()
