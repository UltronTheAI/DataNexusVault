import requests
import json
ip_adress = "https://datanexusvault.onrender.com"

# Function to communicate with the Node.js server
def communicate_with_server(endpoint, data):
    url = f"{ip_adress}/{endpoint}"
    response = requests.post(url, json=data)
    return response.json()

# Function to send JSON data to the server
def send_data(token, json_data):
    data = {
        "token": token,
        "data": json_data
    }
    response = communicate_with_server("send-data", data)
    print(f"Send Data Response: {response}")
    return response

# if __name__ == "__main__":
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiaWF0IjoxNzMzMjMyNzMyLCJleHAiOjE3MzMyMzYzMzJ9.F7d8YbKIh6_hDepIYTElFUtoLlUO9BecJbNCqhZ9284'
#     json_data = {
#         "example_key": "example_value",
#         "another_key": "another_value"
#     }
#     send_data(token, json_data)
