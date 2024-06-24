import argparse
import os
import yaml

def search_key(data, key_path, new_value):
    keys = key_path.split(".")
    current_level = data
    for i, key in enumerate(keys):
        if i == len(keys) - 1:  # Last key, replace value
            if key in current_level:
                current_level[key] = new_value
                return True  # Key found and value replaced
        elif key in current_level:
            current_level = current_level[key]
        else:
            return False  # Key not found
    return False  # In case the loop completes without finding the key

def process_yaml_file(file_path, key_path, new_value):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    key_found = search_key(data, key_path, new_value)
    print(f"Searching for '{key_path}' in {file_path}")
    
    if key_found:
        print(f"Key '{key_path}' found and value replaced.")
        with open(file_path, 'w') as f:
            yaml.dump(data, f, indent=2)
    else:
        print(f"Key '{key_path}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Key-value pair replacer for YAML files.")
    parser.add_argument("--key", "-k", type=str, help="The key to search for.")
    parser.add_argument("--value", "-v", type=str, help="The value to replace with.")
    parser.add_argument("--dir", "-d", type=str, default=".", 
                        help="Directory to process (default: current directory)")
    args = parser.parse_args()

    if args.key and args.value:
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    process_yaml_file(file_path, args.key, args.value)
    else:
        key = input("Enter the key: ")
        value = input("Enter the value: ")
        dir = input("Enter the directory to process (default: current directory): ") or "."
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    process_yaml_file(file_path, key, value)

    print("Key-value replacement complete!")