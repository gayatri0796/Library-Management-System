from admin import login_admin, admin_menu
import os

# Check that data  folder is  exists
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

if __name__ == "__main__":
    if login_admin():
        admin_menu()
    else:
        print("Too many failed attempts. Exit...")
