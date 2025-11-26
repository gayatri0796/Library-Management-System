from books import add_book, remove_book, view_books
from users import add_user, remove_user, view_users
from transactions import issue_book, return_book, view_logs
import os

ADMIN_FILE = os.path.join(os.path.dirname(__file__), "data", "admin.txt")

def create_admin_first_time():
    print("No admin found! Create the first admin account.")
    username = input("Enter new admin username: ")
    password = input("Enter new admin password: ")
    with open(ADMIN_FILE, "w") as f:
        f.write(f"{username},{password}\n")
    print(" Admin account created successfully!")
def login_admin():
    #Check if admin exests 
    if not os.path.exists(ADMIN_FILE) or os.stat(ADMIN_FILE).st_size == 0:
        create_admin_first_time()

    with open(ADMIN_FILE) as f:
        line = f.readline().strip()
        if "," not in line:
            create_admin_first_time()
            line = open(ADMIN_FILE).readline().strip()
    
    stored_username, stored_password = [x.strip() for x in line.split(",")]

    attempts = 3
    while attempts > 0:
        u = input("Enter admin username: ").strip()
        p = input("Enter admin password: ").strip()
        if u == stored_username and p == stored_password:
            print("\nLogin successful!\n")
            return True
        else:
            attempts -= 1
            print(f" Wrong credentials. Attempts left: {attempts}")
    return False

def admin_menu():
    while True:
        print("\n---- Library Menu ----")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. View Books")
        print("4. Add User")
        print("5. Remove User")
        print("6. View Users")
        print("7. Issue Book")
        print("8. Return Book")
        print("9. View Logs")
        print("10. Exit")
        choice = input("Enter choice: ")

        if choice == "1": 
            add_book()
        elif choice == "2": 
            remove_book()
        elif choice == "3": 
            view_books()
        elif choice == "4": 
            add_user()
        elif choice == "5": 
            remove_user()
        elif choice == "6": 
            view_users()
        elif choice == "7": 
            issue_book()
        elif choice == "8": 
            return_book()
        elif choice == "9": 
            view_logs()
        elif choice == "10": 
            print("Exit From Library Management System...")
            break
        else: print("Invalid choice.")
