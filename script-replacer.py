import configparser
import argparse

def replace_values(config_file, replacements):

    config = configparser.ConfigParser()
    config.read(config_file)

    changes_made = False

    for section in config.sections():
        for key, new_value in replacements.items():
            if key in config[section]:
                old_value = config[section][key]
                config[section][key] = new_value
                print(f"Replaced [{section}] {key}: {old_value} -> {new_value}")
                changes_made = True

    if changes_made:
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        print(f"Changes saved to {config_file}")
    else:
        print("No changes were made.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace key:value pairs in a config file.")
    parser.add_argument('config_file', type=str, help="Path to the config file")
    parser.add_argument('-k', '--key', action='append', required=True, help="Key to replace")
    parser.add_argument('-v', '--value', action='append', required=True, help="New value for the key")

    args = parser.parse_args()

    if len(args.key) != len(args.value):
        raise ValueError("The number of keys must match the number of values.")

    config_file = args.config_file
    replacements = dict(zip(args.key, args.value))

    for key in replacements:
        if replacements[key] == '':
            replacements[key] = input(f"Enter new value for {key}: ")

    replace_values(config_file, replacements)
