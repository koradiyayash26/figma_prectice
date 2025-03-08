# Dictionary to store user data
users = {}

def add_user():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    account_type = input("Enter account type (Savings/Current): ")
    
    if name in users:
        print("User already exists!")
    else:
        # Add user details to the dictionary
        users[name] = {
            "password": password,
            "account_type": account_type
        }
        print(f"User {name} added successfully!")

def authenticate_user():
    print(users)
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    
    if name in users:
        if users[name]["password"] == password:
            print(f"Welcome, {name}! Authentication successful.")
            print(f"Account Type: {users[name]['account_type']}")
        else:
            print("Incorrect password! Authentication failed.")
    else:
        print("User not found!")

def main():
    while True:
        print("\n--- User Management ---")
        print("1. Add User")
        print("2. Authenticate User")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_user()
        elif choice == "2":
            authenticate_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
