import os
import requests
import json

ip_adress = "http://192.168.1.4:5000"
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

def main():
    token = ''
    
    # Example data to send
    json_data = {
        "config": {
            "db_name": "a",
            "table_name": "b"
        },
        "email": "kk@gmail.com",
    }
    
    # Sending data to the server
    send_data(token, json_data)

if __name__ == "__main__":
    main()
