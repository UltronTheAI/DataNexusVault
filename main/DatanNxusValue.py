import os
import json
import time
import typing
import google.generativeai as genai
from Modules.communicator import communicate_with_server
from Modules.retrieve_data import retrieve_data
from Modules.save_data import process_and_save_data, save_data, load_table_config

class DatabaseClient:
    def __init__(self, token_file='main/token.txt'):
        self.token = self.read_token(token_file)
        self.model = None

    def read_token(self, token_file):
        try:
            with open(token_file, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"Token file {token_file} not found.")
            return None

    def save_token(self, token, token_file='main/token.txt'):
        with open(token_file, 'w') as file:
            file.write(token)
        self.token = token

    def register_user(self, username, email):
        user_data = {
            "username": username,
            "email": email
        }
        response = communicate_with_server("register", user_data)
        print(f"Register Response: {response}")

    def login_user(self, username, email):
        login_data = {
            "username": username,
            "email": email
        }
        response = communicate_with_server("login", login_data)
        print(f"Login Response: {response}")
        if 'token' in response:
            self.save_token(response['token'])
        return response

    def retrieve_data(self):
        response = retrieve_data(self.token)
        if 'data' in response:
            return response['data']
        return None

    def send_data(self, data):
        response = communicate_with_server("send-data", {"token": self.token, "data": data})
        print(f"Send Data Response: {response}")
        return response

    def check_schema(self, data, schema):
        if self.model is None:
            print("AI model is not configured.")
            return None

        class Recipe(typing.TypedDict):
            matched: bool
        prompt = f"Check if the given data matches the schema. Data: {json.dumps(data)}. Schema: {json.dumps(schema)}.\n"
        response = self.model.generate_content(prompt, generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[Recipe]
        ))
        return json.loads(response.text)

    def configure_ai_model(self, api_key_file='api.txt'):
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def load_table_config(self, db_name, table_name):
        return load_table_config(db_name, table_name)

    def save_data(self, db_name, table_name, data, filename):
        save_data(db_name, table_name, data, filename)

    def process_and_save_data(self, data):
        process_and_save_data(data)

    def run(self):
        while True:
            data = self.retrieve_data()
            if data:
                config = data.get('config', {})
                db_name = config.get('db_name')
                table_name = config.get('table_name')
                filename = data.get('filename')

                if db_name and table_name and filename:
                    table_config = self.load_table_config(db_name, table_name)

                    # Check if the data matches the schema using AI model
                    data_without_config = {k: v for k, v in data.items() if k != 'config'}
                    schema_check_result = self.check_schema(data_without_config, table_config)

                    if schema_check_result[0]['matched']:
                        self.save_data(db_name, table_name, data_without_config, filename)
                    else:
                        print(f"Data does not match schema for table {table_name} in db {db_name}")
            time.sleep(10)

# # Example usage:
# if __name__ == "__main__":
#     client = DatabaseClient()
#     client.configure_ai_model()
#     # client.register_user("username", "email@example.com")
#     # client.login_user("username", "email@example.com")
#     client.run()
