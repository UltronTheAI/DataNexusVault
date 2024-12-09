import requests
import json
ip_adress = "https://datanexusvault.onrender.com"

# Function to communicate with the Node.js server
def communicate_with_server(endpoint, data):
    url = f"{ip_adress}/{endpoint}"
    response = requests.post(url, json=data)
    return response.json()

# Function to retrieve data from the server using token
def retrieve_data(token):
    data = {"token": token}
    response = communicate_with_server("retrieve-data", data)
    print(f"Retrieve Data Response: {response}")
    return response

# if __name__ == "__main__":
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiaWF0IjoxNzMzMjMyNzMyLCJleHAiOjE3MzMyMzYzMzJ9.F7d8YbKIh6_hDepIYTElFUtoLlUO9BecJbNCqhZ9284'
#     retrieve_data(token)
