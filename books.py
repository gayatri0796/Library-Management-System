import os
from prettytable import PrettyTable
from datetime import datetime

BOOK_FILE = os.path.join(os.path.dirname(__file__), "data", "books.txt")
LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "logs.txt")

def log_action(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def add_book():
    b_id = input("Enter Book ID: ").strip()
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()
    quantity = input("Enter Quantity: ").strip()

    # Check if file exists, if not create it
    if not os.path.exists(BOOK_FILE):
        open(BOOK_FILE, "w").close()

    # Check for duplicate ID or Title
    with open(BOOK_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue  # Skip invalid lines
            existing_id, existing_title = parts[0], parts[1]
            if b_id == existing_id:
                print("book with this ID already exists! Please use a unique ID.")
                return
            if title.lower() == existing_title.lower():
                print("book with this title already exists!")
                return

    # Determine availability based on quantity
    avail = "Yes" if quantity != "0" else "No"

    # Add new book
    with open(BOOK_FILE, "a") as f:
        f.write(f"{b_id},{title},{author},{quantity},{avail}\n")

    print("Book added successfully.")
    log_action(f"Book added: {title} (ID: {b_id})")


def remove_book():
    b_id = input("Enter Book ID to remove: ").strip()
    if not os.path.exists(BOOK_FILE):
        print("No book records found.")
        return

    found = False  # Flag to check if the book exists
    with open(BOOK_FILE, "r") as f:
        lines = f.readlines()

    with open(BOOK_FILE, "w") as f:
        for line in lines:
            if line.startswith(b_id + ","):
                found = True  # Book found and will be skipped (deleted)
                continue
            f.write(line)

    if found:
        print("Book removed successfully.")
        log_action(f"Book removed: {b_id}")
    else:
        print("Book ID not found — no book removed.")


def view_books():
    table = PrettyTable(["Book ID", "Title", "Author", "Quantity", "Available"])
    if not os.path.exists(BOOK_FILE):
        print("No books found.")
        return

    with open(BOOK_FILE) as f:
        for line in f:
            b_id, title, author, quantity, avail = line.strip().split(",")
            table.add_row([b_id, title, author, quantity, avail])

    print(table)

