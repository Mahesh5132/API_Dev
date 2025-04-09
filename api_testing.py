import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/users"

def get_users():
    """Fetch all users from the API."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("\nUsers List:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("\nError:", response.status_code, response.text)

def add_user():
    """Add a new user by taking input from the user."""
    name = input("Enter name: ")
    email = input("Enter email: ")
    
    user_data = {"name": name, "email": email}
    response = requests.post(BASE_URL, json=user_data)
    
    if response.status_code == 200:
        print("\n✅ User added successfully!")
        print(response.json())
    else:
        print("\n❌ Error:", response.status_code, response.text)

def delete_user():
    """Delete a user by user ID."""
    user_id = input("Enter user ID to delete: ")
    
    response = requests.delete(f"{BASE_URL}/{user_id}")
    
    if response.status_code == 200:
        print("\n✅ User deleted successfully!")
        print(response.json())
    else:
        print("\n❌ Error:", response.status_code, response.text)

def main():
    """Menu-driven program to test API endpoints."""
    while True:
        print("\n📌 API Testing Menu:")
        print("1. Get all users (GET)")
        print("2. Add a new user (POST)")
        print("3. Delete a user (DELETE)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            get_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            print("\n👋 Exiting...")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
