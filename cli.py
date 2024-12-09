import os
import json
import typer
from prettytable import PrettyTable
import colorama
from colorama import Fore, Style

app = typer.Typer()
colorama.init()

DB_DIR = 'DB'

@app.command()
def list_databases():
    """ Lists all databases defined in the db_config.json file. \n\nRequirements: None Use Case:\n - To view all the databases that have been created."""
    try:
        with open(os.path.join(DB_DIR, 'db_config.json'), 'r') as file:
            config = json.load(file)
            databases = config.get("databases", [])
            table = PrettyTable()
            table.field_names = ["Databases"]
            for db in databases:
                table.add_row([db])
            print(table)
    except FileNotFoundError:
        typer.echo(f"{Fore.RED}Error: db_config.json not found.{Style.RESET_ALL}")

@app.command()
def list_tables(db_name: str):
    """ Lists all tables within a specified database. \n\nRequirements: - db_name: The name of the database. Use Case: - To view all the tables in a particular database. """
    try:
        with open(os.path.join(DB_DIR, db_name, 'list.json'), 'r') as file:
            config = json.load(file)
            tables = config.get("tables", [])
            table = PrettyTable()
            table.field_names = [f"Tables in {db_name}"]
            for tbl in tables:
                table.add_row([tbl])
            print(table)
    except FileNotFoundError:
        typer.echo(f"{Fore.RED}Error: list.json not found for database {db_name}.{Style.RESET_ALL}")

@app.command()
def view_table_data(db_name: str, table_name: str):
    """ Displays the contents of all JSON files in a specified table. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table. Use Case: - To inspect the data stored in a table. """
    table = PrettyTable()
    table.field_names = ["Filename", "Content"]
    table_dir = os.path.join(DB_DIR, db_name, table_name)
    if not os.path.exists(table_dir):
        typer.echo(f"{Fore.RED}Error: Table directory {table_dir} does not exist.{Style.RESET_ALL}")
        return
    
    for filename in os.listdir(table_dir):
        if filename.endswith('.json'):
            with open(os.path.join(table_dir, filename), 'r') as file:
                content = json.load(file)
                table.add_row([filename, json.dumps(content, indent=2)])

    print(table)

@app.command()
def view_table_schema(db_name: str, table_name: str):
    """ Displays the schema of a specified table. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table. Use Case: - To understand the structure and types of data a table is expected to contain. """
    try:
        with open(os.path.join(DB_DIR, db_name, table_name, 'table_config.json'), 'r') as file:
            schema = json.load(file)
            table = PrettyTable()
            table.field_names = ["Column", "Type"]
            for column, col_type in schema.items():
                table.add_row([column, col_type])
            print(table)
    except FileNotFoundError:
        typer.echo(f"{Fore.RED}Error: table_config.json not found for table {table_name} in database {db_name}.{Style.RESET_ALL}")

@app.command()
def create_database(db_name: str):
    """ Creates a new database with the specified name. \n\nRequirements: - db_name: The name of the database to create. Use Case: - To add a new database to the system. """
    db_path = os.path.join(DB_DIR, db_name)
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        list_path = os.path.join(db_path, 'list.json')
        with open(list_path, 'w') as file:
            json.dump({"tables": []}, file, indent=2)

        config_path = os.path.join(DB_DIR, 'db_config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        config['databases'].append(db_name)
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Database '{db_name}' created successfully.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Database '{db_name}' already exists.{Style.RESET_ALL}")

@app.command()
def create_table(db_name: str, table_name: str):
    """ Creates a new table in the specified database. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table to create. Use Case: - To add a new table to an existing database. """
    db_path = os.path.join(DB_DIR, db_name)
    if os.path.exists(db_path):
        table_path = os.path.join(db_path, table_name)
        if not os.path.exists(table_path):
            os.makedirs(table_path)
            config_path = os.path.join(table_path, 'table_config.json')
            with open(config_path, 'w') as file:
                json.dump({}, file, indent=2)

            list_path = os.path.join(db_path, 'list.json')
            with open(list_path, 'r') as file:
                list_config = json.load(file)
            
            list_config['tables'].append(table_name)
            with open(list_path, 'w') as file:
                json.dump(list_config, file, indent=2)
            
            typer.echo(f"{Fore.GREEN}Table '{table_name}' created successfully in database '{db_name}'.{Style.RESET_ALL}")
        else:
            typer.echo(f"{Fore.RED}Table '{table_name}' already exists in database '{db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Database '{db_name}' does not exist.{Style.RESET_ALL}")

@app.command()
def insert_data(db_name: str, table_name: str, data: str):
    """ Inserts data into a specified table. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table. - data: The JSON string of data to insert. Use Case: - To add new data entries to a table. """
    table_path = os.path.join(DB_DIR, db_name, table_name)
    if os.path.exists(table_path):
        data = json.loads(data)
        config_path = os.path.join(table_path, 'table_config.json')
        with open(config_path, 'r') as file:
            schema = json.load(file)
        
        valid_data = {key: value for key, value in data.items() if not schema or key in schema}
        file_path = os.path.join(table_path, f"{int(time.time())}.json")
        with open(file_path, 'w') as file:
            json.dump(valid_data, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Data inserted successfully into table '{table_name}' in database '{db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Table '{table_name}' does not exist in database '{db_name}'.{Style.RESET_ALL}")

@app.command()
def set_table_schema(db_name: str, table_name: str, schema: str):
    """ Sets the schema for a specified table. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table. - schema: The JSON string of the schema to set. Use Case: - To define the structure and types of data a table should contain. """
    table_path = os.path.join(DB_DIR, db_name, table_name)
    if os.path.exists(table_path):
        schema = json.loads(schema)
        config_path = os.path.join(table_path, 'table_config.json')
        with open(config_path, 'w') as file:
            json.dump(schema, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Schema set successfully for table '{table_name}' in database '{db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Table '{table_name}' does not exist in database '{db_name}'.{Style.RESET_ALL}")

@app.command()
def rename_table(db_name: str, old_table_name: str, new_table_name: str):
    """ Renames a table in the specified database. \n\nRequirements: - db_name: The name of the database. - old_table_name: The current name of the table. - new_table_name: The new name for the table. Use Case: - To change the name of an existing table. """
    db_path = os.path.join(DB_DIR, db_name)
    old_table_path = os.path.join(db_path, old_table_name)
    new_table_path = os.path.join(db_path, new_table_name)
    
    if os.path.exists(old_table_path) and not os.path.exists(new_table_path):
        os.rename(old_table_path, new_table_path)
        
        list_path = os.path.join(db_path, 'list.json')
        with open(list_path, 'r') as file:
            list_config = json.load(file)
        
        list_config['tables'].remove(old_table_name)
        list_config['tables'].append(new_table_name)
        with open(list_path, 'w') as file:
            json.dump(list_config, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Table '{old_table_name}' renamed to '{new_table_name}' in database '{db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Error renaming table '{old_table_name}' to '{new_table_name}'.{Style.RESET_ALL}")

@app.command()
def rename_database(old_db_name: str, new_db_name: str):
    """ Renames a database. \n\nRequirements: - old_db_name: The current name of the database. - new_db_name: The new name for the database. Use Case: - To change the name of an existing database. """
    old_db_path = os.path.join(DB_DIR, old_db_name)
    new_db_path = os.path.join(DB_DIR, new_db_name)
    
    if os.path.exists(old_db_path) and not os.path.exists(new_db_path):
        os.rename(old_db_path, new_db_path)
        
        config_path = os.path.join(DB_DIR, 'db_config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        config['databases'].remove(old_db_name)
        config['databases'].append(new_db_name)
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Database '{old_db_name}' renamed to '{new_db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Error renaming database '{old_db_name}' to '{new_db_name}'.{Style.RESET_ALL}")

@app.command()
def delete_table(db_name: str, table_name: str):
    """ Deletes a table from the specified database. \n\nRequirements: - db_name: The name of the database. - table_name: The name of the table to delete. Use Case: - To remove an existing table from a database. """
    db_path = os.path.join(DB_DIR, db_name)
    table_path = os.path.join(db_path, table_name)
    
    if os.path.exists(table_path):
        for filename in os.listdir(table_path):
            file_path = os.path.join(table_path, filename)
            os.remove(file_path)
        os.rmdir(table_path)
        
        list_path = os.path.join(db_path, 'list.json')
        with open(list_path, 'r') as file:
            list_config = json.load(file)
        
        list_config['tables'].remove(table_name)
        with open(list_path, 'w') as file:
            json.dump(list_config, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Table '{table_name}' deleted successfully from database '{db_name}'.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Table '{table_name}' does not exist in database '{db_name}'.{Style.RESET_ALL}")

@app.command()
def delete_database(db_name: str):
    """ Deletes a database. \n\nRequirements: - db_name: The name of the database to delete. Use Case: - To remove an existing database from the system. """
    db_path = os.path.join(DB_DIR, db_name)
    
    if os.path.exists(db_path):
        for table_name in os.listdir(db_path):
            table_path = os.path.join(db_path, table_name)
            if os.path.isdir(table_path):
                for filename in os.listdir(table_path):
                    file_path = os.path.join(table_path, filename)
                    os.remove(file_path)
                os.rmdir(table_path)
        
        os.rmdir(db_path)
        
        config_path = os.path.join(DB_DIR, 'db_config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        config['databases'].remove(db_name)
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=2)
        
        typer.echo(f"{Fore.GREEN}Database '{db_name}' deleted successfully.{Style.RESET_ALL}")
    else:
        typer.echo(f"{Fore.RED}Database '{db_name}' does not exist.{Style.RESET_ALL}")

@app.command(help="Change the token stored in token.txt.")
def change_token(new_token: str):
    """
    Changes the token stored in token.txt.
    
    Requirements:
    - new_token: The new token to store.
    
    Use Case:
    - To update the token used for communicating with the server.
    """
    with open('main/token.txt', 'w') as file:
        file.write(new_token)
    typer.echo(f"{Fore.GREEN}Token changed successfully.{Style.RESET_ALL}")


@app.command()
def main():
    typer.echo(f"{Fore.YELLOW}Available Commands:{Style.RESET_ALL}")
    typer.echo(f"{Fore.CYAN}1. List Databases")
    typer.echo(f"2. List Tables in Database")
    typer.echo(f"3. View Table Data")
    typer.echo(f"4. View Table Schema")
    typer.echo(f"5. Create Database")
    typer.echo(f"6. Create Table")
    typer.echo(f"7. Insert Data")
    typer.echo(f"8. Set Table Schema")
    typer.echo(f"9. Rename Table")
    typer.echo(f"10. Rename Database")
    typer.echo(f"11. Delete Table")
    typer.echo(f"12. Delete Database")
    typer.echo(f"13. Exit{Style.RESET_ALL}")

if __name__ == "__main__":
    app()
