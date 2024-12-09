import os
import requests
import json
ip_adress = "https://datanexusvault.onrender.com"

# Function to list files and folders recursively
def list_directory(directory):
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{sub_indent}{f}')

# Function to communicate with the Node.js server
def communicate_with_server(endpoint, data):
    url = f"{ip_adress}/{endpoint}"
    response = requests.post(url, json=data)
    return response.json()

# Function to register a user
def register_user(username, email):
    user_data = {
        "username": username,
        "email": email
    }
    response = communicate_with_server("register", user_data)
    print(f"Register Response: {response}")

# Function to login a user
def login_user(username, email):
    login_data = {
        "username": username,
        "email": email
    }
    response = communicate_with_server("login", login_data)
    print(f"Login Response: {response}")
    return response

# Function to save the current working directory to environment variable
def save_current_directory():
    current_working_directory = os.getcwd()
    os.environ['DataNexusVault'] = current_working_directory
    print(f"Current working directory saved to environment variable 'DataNexusVault': {current_working_directory}")

# Function to save token to token.json
def save_token(username, token):
    token_file_path = 'token.json'
    try:
        with open(token_file_path, 'r') as file:
            tokens = json.load(file)
    except FileNotFoundError:
        tokens = {}

    tokens[username] = token
    with open(token_file_path, 'w') as file:
        json.dump(tokens, file, indent=2)

# Function to load token from token.json
def load_token(username):
    try:
        with open('token.json', 'r') as file:
            tokens = json.load(file)
            return tokens.get(username)
    except FileNotFoundError:
        return None

# if __name__ == "__main__":
#     directory = './'

#     # Save the current working directory to an environment variable
#     save_current_directory()

#     username = "testuser"
#     email = "testuser@example.com"

#     # Register a new user
#     register_user(username, email)

#     # Load token and login
#     token = load_token(username)
#     if token:
#         print(f"User is already logged in with token: {token}")
#     else:
#         # Login the user
#         login_response = login_user(username, email)
#         if 'token' in login_response:
#             token = login_response['token']
#             print(f"Login successful, token: {token}")
#             save_token(username, token)
#         else:
#             print("Login failed.")
