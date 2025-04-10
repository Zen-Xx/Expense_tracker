import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Expense(Base):
    # Simple table to store expenses
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    category = Column(String)

    amount = Column(Float)

class Budget(Base):
    # Monthly budget per category
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    month = Column(String)  # Format: 'YYYY-MM'
    category = Column(String)
    amount = Column(Float)

    __table_args__ = (UniqueConstraint('month', 'category', name='_month_category_uc'), )

def get_engine():
    return create_engine('sqlite:///expense_tracker.db')

def create_db(engine):
    Base.metadata.create_all(engine)

def log_expense(session):
    print("\n-- Enter the Expense --")
    categories = ["Food", "Rent", "Bills", "Fuel", "Electronics", "Transport", "Entertainment", "Others"]

    # Show category options
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    choice = input("Select category number: ")

    if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
        print("Invalid category choice.")
        return

    selected = categories[int(choice) - 1]

    # If "Others", ask for description + amount separately
    if selected == "Others":
        category = input("Enter description for this expense: ").strip()
        if not category:
            print("Description cannot be empty.")
            return
        amount_str = input("Enter amount: ").strip()
    else:
        category = selected
        amount_str = input("Enter amount: ").strip()

    if not amount_str.replace('.', '', 1).isdigit():
        print("Invalid amount.")
        return
    amount = float(amount_str)

    # Ask for date
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    expense_date = datetime.date.today()
    if date_input:
        try:
            expense_date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")
            return

    # Save expense
    expense = Expense(date=expense_date, category=category, amount=amount)
    session.add(expense)
    session.commit()
    print("Expense logged!")

    # Budget check
    month = expense_date.strftime("%Y-%m")
    budget = session.query(Budget).filter_by(month=month, category=category).first()

    if budget:
        total = session.query(func.sum(Expense.amount)).filter(
            Expense.category == category,
            func.strftime("%Y-%m", Expense.date) == month
        ).scalar() or 0

        remaining = budget.amount - total
        if remaining < 0:
            print(f"Budget exceeded for '{category}'!")
        elif remaining <= 0.1 * budget.amount:
            print(f"Only {remaining:.2f} left in your budget for '{category}'.")


def set_budget(session):
    print("\n-- Set/Update the Budget --")
    month = input("Month (YYYY-MM): ").strip()
    category = input("Category: ").strip()
    try:
        amount = float(input("Budget amount: ").strip())
    except ValueError:
        print("That's not a valid number.")
        return

    budget = session.query(Budget).filter_by(month=month, category=category).first()
    if budget:
        budget.amount = amount
        print("Budget updated.")
    else:
        session.add(Budget(month=month, category=category, amount=amount))
        print("Budget set.")
    session.commit()

def show_total_spending(session):
    print("\n-- Montly spending log --")
    results = session.query(
        func.strftime("%Y-%m", Expense.date).label("month"),
        func.sum(Expense.amount)
    ).group_by("month").all()

    if not results:
        print("No spending data found.")
        return

    for month, total in results:
        print(f"{month}: ₹{total:.2f}")

def compare_spending_vs_budget(session):
    print("\n-- Spending vs Budget --")
    month = input("Enter month (YYYY-MM): ").strip()
    categories = session.query(Expense.category).distinct().all()

    if not categories:
        print("No expenses recorded yet.")
        return

    for (cat,) in categories:
        spent = session.query(func.sum(Expense.amount)).filter(
            Expense.category == cat,
            func.strftime("%Y-%m", Expense.date) == month
        ).scalar() or 0

        budget = session.query(Budget).filter_by(month=month, category=cat).first()
        budget_amt = budget.amount if budget else 0

        print(f"{cat} -> Spent: ₹{spent:.2f}, Budget: ₹{budget_amt:.2f}")

def main():
    engine = get_engine()
    create_db(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n==== Expense Tracking App ====")
        print("1. Enter the Expense")
        print("2. Set/Update the Budget")
        print("3. Montly spending log")
        print("4. Compare Spending vs Budget")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            log_expense(session)
        elif choice == "2":
            set_budget(session)
        elif choice == "3":
            show_total_spending(session)
        elif choice == "4":
            compare_spending_vs_budget(session)
        elif choice == "5":
            print("Thank You!")
            break
        else:
            print("Invalid choice. Try 1 to 5.")

if __name__ == '__main__':
    main()
