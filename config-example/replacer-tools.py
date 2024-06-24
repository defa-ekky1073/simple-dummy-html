import argparse
import re
import os

def replace_nested_key(data, key_path, new_value):
    """Replaces the value of a nested key in a dictionary."""
    keys = key_path.split(".")
    current_level = data
    for i, key in enumerate(keys):
        if i == len(keys) - 1:  # Last key, replace value
            if key in current_level:
                current_level[key] = new_value
        elif key in current_level:
            current_level = current_level[key]
        else:
            return  # Key not found
        f.write(re.sub(pattern, replacement, file_content))

def process_yaml_file(file_path, key_path, new_value):
    """Loads, modifies, and saves a YAML file."""
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    replace_nested_key(data, key_path, new_value)

    with open(file_path, 'w') as f:
        yaml.dump(data, f, indent=2)


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
        for root, _, files in os.walk(adir):
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    process_yaml_file(file_path, key, value)

    print("Key-value replacement complete!")