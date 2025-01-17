import winreg as reg

def add_registry_key(path, key_name, value_name, value_data):
    try:
        # Open the registry key or create it if it doesn't exist
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, path)
        
        # Add a value to the key
        reg.SetValueEx(key, value_name, 0, reg.REG_SZ, value_data)
        
        # Close the key
        reg.CloseKey(key)
        print(f"Successfully added '{value_name}' with data '{value_data}' to {path}\\{key_name}")
    except Exception as e:
        print(f"Error editing the registry: {e}")

def delete_registry_key(path):
    try:
        reg.DeleteKey(reg.HKEY_CURRENT_USER, path)
        print(f"Successfully deleted the registry key at {path}")
    except FileNotFoundError:
        print(f"Registry key at {path} not found.")
    except Exception as e:
        print(f"Error deleting the registry key: {e}")

# Example usage
if __name__ == "__main__":
    # Path to where you want to add the key
    reg_path = r"Software\MyCustomApp"

    # Delete key if it exists so no copies will appear
    delete_registry_key(reg_path)
    
    # Key name (just for logging purposes here)
    key_name = "PDF_Editor"

    # Value name and data to add
    value_name = "MySetting"
    value_data = "CustomValue"

    # Add the registry key and value
    add_registry_key(reg_path, key_name, value_name, value_data)
