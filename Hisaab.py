import mysql.connector as sql
import matplotlib.pyplot as plt
import pandas as pd
import time as ti
from getpass import getpass
from collections import defaultdict

class AccountingSoftware:
    def __init__(self):
        self.logged_in = False
        self.user_id = None
        self.db_connection = None
        self.current_company = None
        self.companies = {}
        self.current_company_data = defaultdict(list)

    def login(self):
        print("**********Welcome To Hisaab Software**********")
        for _ in range(4):
            a = input("Enter Your Login ID: ")
            b = getpass("Enter Your Password: ")

            if self.authenticate_user(a, b):
                self.logged_in = True
                self.user_id = a
                break
            else:
                print("Invalid credentials. Please try again.")

        if not self.logged_in:
            print("Too many failed login attempts. Lockdown initiated.")
            return

    def authenticate_user(self, username, password):
        # Implement a real authentication mechanism here, e.g., database lookup
        return username == "Rajas" and password == "Rajas"

    def create_company(self):
        company_name = input("Enter Company Name: ")
        if company_name in self.companies:
            print("Company already exists.")
        else:
            self.companies[company_name] = {}
            print(f"Company '{company_name}' created successfully.")

    def select_company(self):
        if not self.companies:
            print("No companies available.")
            return

        print("Available Companies:")
        for i, company in enumerate(self.companies.keys()):
            print(f"{i + 1}. {company}")

        while True:
            try:
                company_index = int(input("Select a company (1-{}): ".format(len(self.companies))))
                if 1 <= company_index <= len(self.companies):
                    self.current_company = list(self.companies.keys())[company_index - 1]
                    break
                else:
                    print("Invalid choice. Please select a valid company.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def manage_company_data(self):
        while True:
            print(f"Managing data for '{self.current_company}'")
            print("===========================================")
            print("Enter 1 To Add Sales Transaction")
            print("Enter 2 To Add Purchase Transaction")
            print("Enter 3 To View Transactions")
            print("Enter 4 To Delete Transaction")
            print("Enter 5 To Go Back")
            choice = input("Enter Your Choice: ")

            if choice == '1':
                self.add_sales_transaction()
            elif choice == '2':
                self.add_purchase_transaction()
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                self.delete_transaction()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def add_sales_transaction(self):
        if self.current_company is None:
            print("No company selected.")
            return

        print(f"Adding Sales Transaction for '{self.current_company}'")
        voucher_number = int(input("Enter Voucher Number: "))
        date = int(input("Enter Date Of Invoice: "))
        month = input("Enter Month Of Invoice: ")
        product = input("Enter Product Name: ")
        price = int(input("Enter Price Of Single Product: "))
        quantity = int(input("Enter Quantity: "))
        gst = int(input("Enter Gst: "))

        total_price = quantity * price
        tax = ((gst / 100) * total_price) + total_price

        transaction = {
            "Voucher_Number": voucher_number,
            "Date": date,
            "Month": month,
            "Product": product,
            "Price": price,
            "Quantity": quantity,
            "Gst": gst,
            "Total_Price": tax
        }

        self.current_company_data[self.current_company].append(transaction)
        print("Sales transaction added successfully.")

    def add_purchase_transaction(self):
        if self.current_company is None:
            print("No company selected.")
            return

        print(f"Adding Purchase Transaction for '{self.current_company}'")
        voucher_number = int(input("Enter Voucher Number: "))
        date = int(input("Enter Date Of Purchase: "))
        month = input("Enter Month Of Purchase: ")
        product = input("Enter Product Name: ")
        price = int(input("Enter Price Of Single Product: "))
        quantity = int(input("Enter Quantity: "))
        gst = int(input("Enter Gst: "))

        total_price = quantity * price
        tax = ((gst / 100) * total_price) + total_price

        transaction = {
            "Voucher_Number": voucher_number,
            "Date": date,
            "Month": month,
            "Product": product,
            "Price": price,
            "Quantity": quantity,
            "Gst": gst,
            "Total_Price": tax
        }

        self.current_company_data[self.current_company].append(transaction)
        print("Purchase transaction added successfully.")

    def view_transactions(self):
        if self.current_company is None:
            print("No company selected.")
            return

        print(f"Viewing Transactions for '{self.current_company}'")
        print("Sales Transactions:")
        sales_data = self.current_company_data.get(self.current_company, [])
        self.display_transactions(sales_data)

        print("Purchase Transactions:")
        purchase_data = self.current_company_data.get(self.current_company, [])
        self.display_transactions(purchase_data)

    def display_transactions(self, transactions):
        if not transactions:
            print("No transactions available.")
        else:
            for i, transaction in enumerate(transactions):
                print(f"Transaction {i + 1}:")
                self.display_transaction(transaction)
                print("----------------------------")

    def display_transaction(self, transaction):
        for key, value in transaction.items():
            print(f"{key}: {value}")

    def delete_transaction(self):
        if self.current_company is None:
            print("No company selected.")
            return

        print(f"Deleting Transaction for '{self.current_company}'")
        transaction_type = input("Enter transaction type (Sales or Purchase): ").strip().lower()
        
        if transaction_type not in ["sales", "purchase"]:
            print("Invalid transaction type.")
            return
        
        transaction_list = self.current_company_data.get(self.current_company, [])
        
        if not transaction_list:
            print(f"No {transaction_type} transactions available for deletion.")
            return

        transaction_index = int(input(f"Enter the index of the {transaction_type} transaction to delete: "))

        if 0 <= transaction_index < len(transaction_list):
            deleted_transaction = transaction_list.pop(transaction_index)
            print(f"{transaction_type.capitalize()} transaction deleted:")
            self.display_transaction(deleted_transaction)
        else:
            print("Invalid transaction index.")

    def check_profit_or_loss(self):
        if self.current_company is None:
            print("No company selected.")
            return

        sales_data = self.current_company_data.get(self.current_company, [])
        purchase_data = self.current_company_data.get(self.current_company, [])

        total_sales = sum(transaction["Total_Price"] for transaction in sales_data)
        total_purchase = sum(transaction["Total_Price"] for transaction in purchase_data)

        print(f"Total Sales: {total_sales}")
        print(f"Total Purchase: {total_purchase}")

        if total_sales > total_purchase:
            print("You are in Profit.")
        elif total_sales < total_purchase:
            print("You are in Loss.")
        else:
            print("You are neither in Profit nor in Loss.")

    def generate_sales_chart(self):
        if self.current_company is None:
            print("No company selected.")
            return

        sales_data = self.current_company_data.get(self.current_company, [])
        if not sales_data:
            print("No sales data available for chart.")
            return

        # Prepare data for the chart
        months = []
        total_sales = []
        for transaction in sales_data:
            months.append(transaction["Month"])
            total_sales.append(transaction["Total_Price"])

        # Create a line chart
        plt.figure(figsize=(10, 6))
        plt.plot(months, total_sales, marker='o', linestyle='-')
        plt.title(f'Sales Over Time for {self.current_company}')
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.grid(True)

        # Show the chart
        plt.show()

    def logout(self):
        self.logged_in = False
        self.user_id = None
        self.current_company = None

    def run(self):
        self.login()
        if self.logged_in:
            while True:
                print("Main Menu:")
                print("1. Create Company")
                print("2. Select Company")
                print("3. Manage Company Data")
                print("4. View Transactions")
                print("5. Delete Transaction")
                print("6. Check Profit or Loss")
                print("7. Generate Sales Chart")
                print("8. Logout")
                choice = input("Enter Your Choice: ")

                if choice == '1':
                    self.create_company()
                elif choice == '2':
                    self.select_company()
                elif choice == '3':
                    self.manage_company_data()
                elif choice == '4':
                    self.view_transactions()
                elif choice == '5':
                    self.delete_transaction()
                elif choice == '6':
                    self.check_profit_or_loss()
                elif choice == '7':
                    self.generate_sales_chart()
                elif choice == '8':
                    self.logout()
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

        print("Program Terminated")
        print("Thank You For Choosing Hisaab Software...")

if __name__ == "__main__":
    app = AccountingSoftware()
    app.run()
