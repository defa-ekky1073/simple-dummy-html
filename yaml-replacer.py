import yaml
import os
import argparse

def yaml_replacer_argParser():
    parser = argparse.ArgumentParser(
        prog='Yaml Replacer',
        description='Replace YAML configurations'
    )

    parser.add_argument("--key", "-k", help="Key parameter to replace", required=True)
    parser.add_argument("--value", "-v", help="Value to replace parameter", required=True)
    parser.add_argument("--dir", "-d", help="Parent directory path", required=True)
    return parser.parse_args()

def get_all_file_in_directory(dirpath):
    filepath = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                path = os.path.join(root, file)
                filepath.append(path)
    return filepath

def update_yaml_data(data, key, value):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                data[k] = value
            else:
                update_yaml_data(v, key, value)
    elif isinstance(data, list):
        for item in data:
            update_yaml_data(item, key, value)

def update_yaml_file(filepath, key, value):
    try:
        with open(filepath, 'r') as stream:
            data = yaml.safe_load(stream)
        
        update_yaml_data(data, key, value)
        
        with open(filepath, 'w') as stream:
            yaml.dump(data, stream, default_flow_style=False, sort_keys=False)
            print(f"Updated '{key}' in {filepath}")
    
    except (yaml.YAMLError, IOError) as exc:
        print(f"Error processing {filepath}: {exc}")

def update_yaml_with_specified_path(filepath, child, value):
    for file in filepath:
        try:
            with open(file, 'r') as stream:
                data = yaml.safe_load(stream)
            try:
                current = data
                for key in child[:-1]:
                    current = current.setdefault(key, {})
                    print(key)
                if child[-1] in current:
                    print("replacing on: " + file)
                    current[child[-1]] = args.value
                    with open(file, 'w') as stream:
                        yaml.dump(data, stream, default_flow_style=False, sort_keys=False)
            except:
                continue
        except yaml.YAMLError as exc:
            print(exc)

def main():
    args = yaml_replacer_argParser()
    dirPath = args.dir
    filepath = get_all_file_in_directory(dirPath)

    if "." in args.key:
        child = child = args.key.split(".")
        update_yaml_with_specified_path(filepath, child, args.value)
    else:
        for file in filepath:
            update_yaml_file(file, args.key, args.value)

if __name__ == "__main__":
    main()