import os
from datetime import datetime
from prettytable import PrettyTable

BOOK_FILE = os.path.join(os.path.dirname(__file__), "data", "books.txt")
USER_FILE = os.path.join(os.path.dirname(__file__), "data", "users.txt")
ISSUED_FILE = os.path.join(os.path.dirname(__file__), "data", "issued_books.txt")
LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "logs.txt")

FINE = 50

def log_action(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def issue_book():
    username = input("Enter username: ").strip()
    book_id = input("Enter Book ID to issue: ").strip()

    if not os.path.exists(BOOK_FILE):
        print("No books found.")
        return

    lines = open(BOOK_FILE).readlines()
    issued = False

    with open(BOOK_FILE, "w") as f:
        for line in lines:
            parts = line.strip().split(",")

            # Handle both old (4 fields) and new (5 fields) book records
            if len(parts) == 5:
                bid, title, author, quantity, avail = parts
            elif len(parts) == 4:
                bid, title, author, avail = parts
                quantity = "1"  # Default for old entries
            else:
                f.write(line)
                continue

            # Check and issue book
            if bid == book_id and avail == "Yes" and int(quantity) > 0:
                new_quantity = str(int(quantity) - 1)
                new_avail = "Yes" if int(new_quantity) > 0 else "No"
                f.write(f"{bid},{title},{author},{new_quantity},{new_avail}\n")
                print(f"Book '{title}' issued to {username}.")
                log_action(f"Book issued: {title} to {username}")
                issued = True
            # Record the issue for returning later
                with open(ISSUED_FILE, "a") as iss_f:
                    iss_f.write(f"{username},{bid},{datetime.now().strftime('%Y-%m-%d')}\n")

    issued = True

    if not issued:
        print("Book not available or already issued.")

def return_book():
    username = input("Enter username: ").strip()
    b_id = input("Enter Book ID to return: ").strip()

    if not os.path.exists(ISSUED_FILE):
        print(" No issued book records found.")
        return

    issued = open(ISSUED_FILE).readlines()
    new_issued = []
    found = False

    for line in issued:
        parts = line.strip().split(",")
        if len(parts) < 3:
            new_issued.append(line)
            continue

        u, bid, date_str = parts[0], parts[1], parts[2]
        if u == username and bid == b_id:
            found = True
            try:
                days = (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days
            except Exception:
                days = 0
            fine = FINE if days > 7 else 0
            if fine > 0:
                print(f"Book overdue! Fine: Rs.{fine}")
            log_action(f"Book returned: {b_id} by {username} (Fine Rs.{fine})")
            # it is removed from issued records
        else:
            new_issued.append(line)

    with open(ISSUED_FILE, "w") as f:
        f.writelines(new_issued)

    # Make the book available again and increment quantity
    if os.path.exists(BOOK_FILE):
        books = open(BOOK_FILE).readlines()
        with open(BOOK_FILE, "w") as f:
            for line in books:
                parts = line.strip().split(",")
                # normalize parsing for both old and new formats
                if len(parts) == 5:
                    bid, title, author, quantity, avail = parts
                elif len(parts) == 4:
                    bid, title, author, avail = parts
                    quantity = "1"
                else:
                    f.write(line)
                    continue

                if bid == b_id:
                    # increment quantity and set available
                    try:
                        new_quantity = str(int(quantity) + 1)
                    except Exception:
                        new_quantity = "1"
                    new_avail = "Yes" if int(new_quantity) > 0 else "No"
                    f.write(f"{bid},{title},{author},{new_quantity},{new_avail}\n")
                else:
                    f.write(f"{bid},{title},{author},{quantity},{avail}\n")

    if found:
        print("Book returned successfully.")
    else:
        print(" No record found for this user and book.")


def view_logs():
    if not os.path.exists(LOG_FILE):
        print("No logs available.")
        return
    print("\n----  Library Logs ----")
    for line in open(LOG_FILE):
        print(line.strip())
