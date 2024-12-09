import os
import json
import time

def load_table_config(db_name, table_name):
    config_path = os.path.join('DB', db_name, table_name, 'table_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            return json.load(file)
    return {}

def save_data(db_name, table_name, data, filename):
    table_dir = os.path.join('DB', db_name, table_name)
    if not os.path.exists(table_dir):
        os.makedirs(table_dir)
    file_path = os.path.join(table_dir, filename)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def process_and_save_data(data):
    config = data.get('config', {})
    db_name = config.get('db_name')
    table_name = config.get('table_name')
    
    if not db_name or not table_name:
        print("Invalid data received: Missing db_name or table_name in config")
        return

    # Load table configuration
    table_config = load_table_config(db_name, table_name)

    # Remove config key from data
    data.pop('config', None)

    # Apply table configuration (schema)
    if table_config:
        filtered_data = {key: value for key, value in data.items() if key in table_config}
    else:
        filtered_data = data

    save_data(db_name, table_name, filtered_data, f"{int(time.time())}.json")
