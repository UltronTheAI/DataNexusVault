import os
import colorama
import platform
import subprocess

def check_folders():
    required_folders = [
        "DB",
        "SERVER",
        "SERVER/data",
        "SERVER/login"
    ]

    for folder in required_folders:
        if not os.path.exists(folder):
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED}{folder} folder does not exist.")
            os.makedirs(folder)
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}{folder} folder created.")
        else:
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}{folder} folder already exists.")

def check_files():
    required_files = {
        "SERVER/login/login.json": "{}"
    }

    for file, content in required_files.items():
        if not os.path.exists(file):
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED}{file} file does not exist.")
            with open(file, "w") as f:
                f.write(content)
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}{file} file created.")
        else:
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}{file} file already exists.")

def set_env_var(variable_name, variable_value):
    system = platform.system()

    if system == "Windows":
        set_env_var_windows(variable_name, variable_value)
    elif system in ["Linux", "Darwin"]:
        set_env_var_unix(variable_name, variable_value)
    else:
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED}Unsupported operating system: {colorama.Fore.YELLOW}{system}")

def set_env_var_windows(variable_name, variable_value):
    import winreg as reg
    try:
        reg_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, variable_name, 0, reg.REG_SZ, variable_value)
        reg.CloseKey(reg_key)
        # Broadcast the change to all running applications
        subprocess.run(['setx', variable_name, variable_value, '/M'], check=True)
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}Environment variable {colorama.Fore.YELLOW}{variable_name} {colorama.Fore.GREEN}set successfully.")
        # Set the variable in the current session
        os.environ[variable_name] = variable_value
    except WindowsError as e:
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED}Error setting environment variable: {colorama.Fore.YELLOW}{e}")

def set_env_var_unix(variable_name, variable_value):
    try:
        bash_profile_path = os.path.expanduser('~/.bash_profile')
        with open(bash_profile_path, 'a') as f:
            f.write(f'\nexport {variable_name}="{variable_value}"\n')
        # Source the file to apply changes immediately
        subprocess.run(['source', bash_profile_path], shell=True, check=True)
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN}Environment variable {colorama.Fore.YELLOW}{variable_name} {colorama.Fore.GREEN}set successfully.")
        # Set the variable in the current session
        os.environ[variable_name] = variable_value
    except Exception as e:
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED}Error setting environment variable: {colorama.Fore.YELLOW}{e}")

def is_env_var_available(variable_name):
    return os.environ.get(variable_name) is not None

def get_env_var(variable_name):
    return os.environ.get(variable_name)

# Usage
if __name__ == "__main__":
    colorama.init() 
    check_folders()
    check_files()
    print(colorama.Fore.RESET)
    # Get the current working directory
    current_working_directory = os.getcwd()

    if not is_env_var_available('DataNexusVault'):
        # Set the environment variable with the current working directory
        set_env_var('DataNexusVault', current_working_directory)
        if is_env_var_available('DataNexusVault'):
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN} Environment variable set.")
        else:
            print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.RED} Environment variable not set.")
    else:
        print(f"{colorama.Fore.YELLOW}LOADER: {colorama.Fore.GREEN} Environment variable already set.")
