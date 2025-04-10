# Simple Expense Tracker CLI

A Python and SQLAlchemy command-line tool for managing budgets for the month and tracking personal spending. Python or Docker can be used to run it directly.

## Description

With the help of this script, you can easily log your expenses, classify them, create monthly budgets for each category, and see summaries of your spending patterns. Data is persistently stored using a SQLite database.

## Features

* **Log Expenses:** Keep track of individual spending transactions and classify them under either a custom 'Others' category or one of the predefined categories (Food, Rent, Bills, Fuel, Electronics, Transportation, Entertainment).
* **Date Input:** Indicate the current day as the date of the expense or default.
* **Set Budgets:** Establish monthly spending plans for particular categories (for example, allocate funds for "Food" in 2025-04).
* **Update Budgets:** Change the current budgetary amounts for a specific month and category.
* **Monthly Spending Summary:** See a report that summarizes all of your monthly expenses.
* **Spending vs. Budget Comparison:** Compare the actual and budgeted amounts spent in each category for a chosen month.
* **Budget Alerts:** Receive automatic warnings when logging an expense if:
    * The budget for that category in that month is exceeded.
    * Less than 10% of the budget for that category remains for the month.
* **Data Persistence:** All expense and budget data is stored locally in an SQLite database file (`expense_tracker.db`).
* **Docker Support:** Includes a `Dockerfile`.

## Requirements

**For running directly with Python:**
* Python 3.10+
* SQLAlchemy library

**For running with Docker:**
* Docker installed and running.

## Setup (Running Directly with Python)

1.  **Ensure Python 3 is installed** on your system.
2.  **Download/Clone:** Get the `expense_tracker.py` script (and other project files if in a repository).
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```
3.  **Install Dependencies:** Open your terminal or command prompt, navigate to the directory containing the script, and install the required library:
    ```bash
    pip install sqlalchemy
    ```
4.  **Database:** No manual database setup is needed. The script will automatically create the `expense_tracker.db` file in the same directory when you run it for the first time.

## Usage (Running Directly with Python)

1.  **Run the Script:** Open your terminal or command prompt, navigate to the script's directory, and execute it using:
    ```bash
    python expense_tracker.py
    ```
2.  **Follow the Menu:** The application will present a menu with the following options:
    * `1. Enter the Expense`: Guides you through logging a new expense (category, amount, date).
    * `2. Set/Update the Budget`: Allows you to define or change the budget for a specific category and month (use `YYYY-MM` format for the month).
    * `3. Montly spending log`: Displays the total amount spent for each month recorded.
    * `4. Compare Spending vs Budget`: Asks for a month (`YYYY-MM`) and shows spent vs. budget for each category in that month.
    * `5. Exit`: Closes the application.
3.  Enter the number corresponding to your desired action and press Enter. Follow the subsequent prompts.

## Running with Docker

Using Docker allows you to run the application in an isolated container environment without needing to install Python or dependencies directly on your host machine.

1.  **Ensure Docker is installed and running.**
2.  **Build the Docker Image:**
    * Open your terminal or command prompt.
    * Navigate to the directory containing the `Dockerfile` and `expense_tracker.py`.
    * Run the build command:
      ```bash
      docker build -t expense-tracker-app .
      ```

4.  **Run the Docker Container:**
    * Execute the following command in your terminal:
      ```bash
      docker run -it --rm expense-tracker-app
      ```
