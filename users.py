import os
from prettytable import PrettyTable
from datetime import datetime

USER_FILE = os.path.join(os.path.dirname(__file__), "data", "users.txt")
LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "logs.txt")

def log_action(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def add_user():
    username = input("Enter username: ").strip()
    # Check for duplicate username
    if os.path.exists(USER_FILE):
        with open(USER_FILE) as f:
            for line in f:
                existing_user = line.strip().split(",")[0]
                if existing_user == username:
                    print("Username already exists! Please choose another one.")
                    log_action(f"Duplicate username attempted: {username}")
                    return

    password = input("Enter password: ").strip()
    contact = input("Enter contact number: ").strip()
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password},{contact}\n")
    print("User added.")
    log_action(f"User added: {username}")
def remove_user():
    username = input("Enter username to remove: ").strip()
    if not os.path.exists(USER_FILE):
        print("No user records found.")
        return

    found = False
    with open(USER_FILE, "r") as f:
        lines = f.readlines()

    with open(USER_FILE, "w") as f:
        for line in lines:
            if line.startswith(username + ","):
                found = True
                # skip writing this line (effectively deleting it)
                continue
            f.write(line)

    if found:
        print("User removed.")
        log_action(f"User removed: {username}")
    else:
        print("User not found — no user removed.")

def view_users():
    table = PrettyTable(["Username", "Contact No"])
    if not os.path.exists(USER_FILE):
        print("No users found.")
        return
    with open(USER_FILE) as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                u, _, contact = parts
                table.add_row([u, contact])
    print(table)

