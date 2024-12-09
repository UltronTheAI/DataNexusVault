# DataNexusVault

**DataNexusVault** is a comprehensive, token-based data management system that allows users to manage databases and tables, and perform CRUD operations efficiently. The system utilizes AI to ensure data integrity by validating data against predefined schemas.

### Why DataNexusVault?

DataNexusVault was created to provide a highly flexible and scalable database solution that can be easily deployed and accessed from anywhere in the world. It uses local storage for data but can be spawned and hosted anywhere, making it an incredibly useful database system for global applications.

Absolutely! Below is a section in the README.md that provides example Python code demonstrating how to use the DataNexusVault database system with the provided `database_client.py` module.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
   - [Example Usage with Python](#example-usage-with-python)
   - [CLI Commands](#cli-commands)
   - [Web Interface - Coming Soon!](#web-interface)
3. [Configuration](#configuration)
   - [Database Configuration](#database-configuration)
   - [Table Schema](#table-schema)
   - [Tokens](#tokens)
4. [Database File Structure](#database-file-structure)
5. [API Reference](#api-reference)
6. [License](#license)

## Example Usage with Python

**database_client.py**:

```python
from database_client import DatabaseClient

# Configure the AI model with the API key
client = DatabaseClient()
client.configure_ai_model(api_key_file='gemini_api.txt')

# Register a new user
client.register_user("your_username", "your_email@example.com")

# Log in the user and obtain a token
login_response = client.login_user("your_username", "your_email@example.com")
token = login_response.get('token')
print(f"Token: {token}")

# Send data to the database
data_to_send = {
    "config": {
        "db_name": "example_db",
        "table_name": "example_table"
    },
    "email": "example@example.com",
    "password": "example_password"
}
send_response = client.send_data(data_to_send)
print(f"Send Data Response: {send_response}")

# Retrieve data from the database
retrieved_data = client.retrieve_data()
print(f"Retrieved Data: {retrieved_data}")
```

### Explanation:
- **Configure the AI Model**: Initialize the AI model using the `configure_ai_model` method.
- **Register a User**: Register a new user by calling `register_user` with the desired username and email.
- **Log in the User**: Log in the user using `login_user` and obtain the token from the response. Save the token for future requests.
- **Send Data**: Use `send_data` to send data to the specified database and table.
- **Retrieve Data**: Retrieve data from the database using the `retrieve_data` method.

### Running the Example

1. Save the example code in a Python file, e.g., `example_usage.py`.
2. Ensure that your `api.txt` file contains the necessary API key.
3. Run the example script:
   ```sh
   python example_usage.py
   ```

This example demonstrates the basic usage of the DataNexusVault system, highlighting how to perform essential operations such as user registration, login, data insertion, and data retrieval.

By following this example, you can extend the functionality to suit your specific requirements and build more complex interactions with your database. If you need further assistance, feel free to explore the API reference or contact us for support. Happy coding! 🎉

## Features

- Token-based authentication for secure access.
- AI-powered schema validation.
- User-friendly CLI for managing databases and tables.
- Web interface with Tailwind CSS for a seamless user experience.
- Automatic data retrieval and processing.

### Tokens

Tokens are a crucial part of DataNexusVault's security mechanism, ensuring that only authenticated users can access and manipulate the data. Here's a detailed explanation of how tokens work in our system:

## Why Tokens?

Tokens provide a secure way to verify user identity and ensure that only authorized users can perform operations on the database. They help in maintaining session security and preventing unauthorized access.

### How to Obtain a Token

To interact with the DataNexusVault system, you first need to register and log in to obtain a token.

**Register User:**
```
POST /register
{
  "username": "your_username",
  "email": "your_email@example.com"
}
```

**Login User:**
```
POST /login
{
  "username": "your_username",
  "email": "your_email@example.com"
}
```

Upon successful login, a token will be provided in the response:
```
{
  "message": "Login successful",
  "token": "your_generated_token"
}
```

### Storing the Token

Once you have obtained the token, store it securely in a file (e.g., `main/token.txt`). This token will be used for all subsequent requests to interact with the database.

### Using the Token

Include the token in your requests to authenticate and authorize your actions. For example, to send data:
```
POST /send-data
{
  "token": "your_token",
  "data": {
    "config": {
      "db_name": "example_db",
      "table_name": "example_table"
    },
    "email": "example@example.com",
    "password": "example_password"
  }
}
```

### Changing the Token

If you need to update the token (e.g., if it expires or you want to use a new one), use the `change_token` CLI command:
```sh
python cli.py change_token --new-token "your_new_token"
```

This command will update the token stored in `token.txt` with the new token provided.

By using tokens, DataNexusVault ensures that your data remains secure and accessible only to authorized users.

## Database File Structure

DataNexusVault organizes your data in a structured directory format. Below is an overview of how the files and directories are organized within the `DB` directory:

```
DB/
├── db_config.json
├── example_db/
│   ├── list.json
│   ├── example_table/
│   │   ├── table_config.json
│   │   ├── 1609459200.json
│   │   └── 1609459260.json
└── another_db/
    ├── list.json
    ├── another_table/
        ├── table_config.json
        ├── 1609459320.json
        └── 1609459380.json
```

#### Explanation:

1. **db_config.json**: This file contains a list of all databases in the system.
    ```json
    {
      "databases": [
        "example_db",
        "another_db"
      ]
    }
    ```

2. **Databases**: Each database is represented by a directory within the `DB` directory. For example, `example_db/` and `another_db/` are two databases.

3. **list.json**: Each database directory contains a `list.json` file, which lists all tables in that database.
    ```json
    {
      "tables": [
        "example_table",
        "another_table"
      ]
    }
    ```

4. **Tables**: Each table is represented by a directory within its respective database directory. For example, `example_table/` within `example_db/`.

5. **table_config.json**: Each table directory contains a `table_config.json` file that defines the schema for that table.
    ```json
    {
      "columns": {
        "email": "$string",
        "password": "$string"
      }
    }
    ```

6. **Data Files**: Data entries are stored as JSON files within their respective table directories. The filenames are typically timestamps or unique identifiers.
    ```json
    {
      "email": "example@example.com",
      "password": "example_password"
    }
    ```

### Example:

- **DB/db_config.json**: Lists all databases.
- **DB/example_db/list.json**: Lists all tables in the `example_db` database.
- **DB/example_db/example_table/table_config.json**: Defines the schema for the `example_table` table.
- **DB/example_db/example_table/1609459200.json**: A data entry for the `example_table` table.

By understanding this file structure, you can efficiently navigate and manage your databases, tables, and data entries within DataNexusVault.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/DataNexusVault.git
   cd DataNexusVault
   ```

2. **Install required packages:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies:**
   ```sh
   cd server
   npm install
   ```

4. **Set up Tailwind CSS:**
   ```sh
   npx tailwindcss init
   ```

5. **Configure Tailwind CSS:**
   - Update `tailwind.config.js`:
     ```javascript
     module.exports = {
       purge: ['./public/**/*.html'],
       darkMode: false,
       theme: {
         extend: {},
       },
       variants: {
         extend: {},
       },
       plugins: [],
     }
     ```

6. **Build Tailwind CSS:**
   ```sh
   npx tailwindcss build -o public/dist/output.css
   ```

## Usage

### CLI Commands

Run the CLI tool to manage databases and tables:

```sh
python cli.py [command]
```

**Commands:**

- `list_databases`: List all available databases.
- `list_tables`: List all tables within a specified database.
- `view_table_data`: View data in a specified table.
- `view_table_schema`: View schema of a specified table.
- `create_database`: Create a new database.
- `create_table`: Create a new table in a specified database.
- `insert_data`: Insert data into a specified table.
- `set_table_schema`: Set the schema for a specified table.
- `rename_table`: Rename a table in a specified database.
- `rename_database`: Rename a database.
- `delete_table`: Delete a table from a specified database.
- `delete_database`: Delete a database.
- `change_token`: Change the token stored in token.txt.

### Web Interface

1. **Start the server:**
   ```sh
   cd server
   node server.js
   ```

2. **Access the web interface:**
   Open your browser and navigate to `http://localhost:3000`.

## Configuration

### Database Configuration

**db_config.json**:
```json
{
  "databases": [
    "example_db"
  ]
}
```

### Table Schema

**table_config.json**:
```json
{
  "columns": {
    "email": "$string",
    "password": "$string"
  }
}
```

## API Reference

- **Register User:**
  ```
  POST /register
  {
    "username": "testuser",
    "email": "testuser@example.com"
  }
  ```

- **Login User:**
  ```
  POST /login
  {
    "username": "testuser",
    "email": "testuser@example.com"
  }
  ```

- **Send Data:**
  ```
  POST /send-data
  {
    "token": "your_token",
    "data": {
      "config": {
        "db_name": "example_db",
        "table_name": "example_table"
      },
      "email": "example@example.com",
      "password": "example_password"
    }
  }
  ```

- **Retrieve Data:**
  ```
  POST /retrieve-data
  {
    "token": "your_token"
  }
  ```

## License

This project is licensed under the MIT License.