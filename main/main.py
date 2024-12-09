import os
import time
import json
import typing_extensions as typing
from Modules.loader import *
import google.generativeai as genai
from Modules.communicator import communicate_with_server
from Modules.retrieve_data import retrieve_data
from Modules.save_data import process_and_save_data, save_data, load_table_config

# Configure the AI model
def configure_model():
    with open('api.txt', 'r') as file:
        api_key = file.read().strip()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

# Function to check if data matches the schema
def check_schema(model, data, schema):
    class Recipe(typing.TypedDict):
        matched: bool
    prompt = f"Check if the given data matches the schema. Data: {json.dumps(data)}. Schema: {json.dumps(schema)}.\n"
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=list[Recipe]
    ))
    return json.loads(response.text)

# Function to read token from token.txt
def read_token():
    try:
        with open('token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Function to save token to token.txt
def save_token(token):
    with open('token.txt', 'w') as file:
        file.write(token)

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

# Main function to periodically request data from the server
def main():
    token = read_token()
    
    if not token:
        username = "testuser"
        email = "testuser@example.com"

        register_user(username, email)
        login_response = login_user(username, email)
        
        if 'token' in login_response:
            token = login_response['token']
            print(f"Login successful, token: {token}")
            save_token(token)
        else:
            print("Failed to obtain token. Exiting.")
            return

    # Configure the AI model
    model = configure_model()
    
    while True:
        response = retrieve_data(token)
        if 'data' in response:
            config = response['data'].get('config', {})
            db_name = config.get('db_name')
            table_name = config.get('table_name')
            filename = response.get('filename')

            if db_name and table_name and filename:
                table_config = load_table_config(db_name, table_name)
                
                # Check if the data matches the schema using AI model
                data_without_config = {k: v for k, v in response['data'].items() if k != 'config'}
                schema_check_result = check_schema(model, data_without_config, table_config)
                
                if schema_check_result[0]['matched']:
                    save_data(db_name, table_name, data_without_config, filename)
                else:
                    print(f"Data does not match schema for table {table_name} in db {db_name}")
        time.sleep(10)

if __name__ == "__main__":
    main()
