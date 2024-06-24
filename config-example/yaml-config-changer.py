import os
import yaml

import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# Required positional argument
# parser.add_argument('pos_arg', type=int,
#                     help='A required integer positional argument')

# Optional positional argument
# parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                     help='An optional integer positional argument')

# Optional argument
parser.add_argument('--key', type=str,
                    help='Key target argument')

parser.add_argument('--value', type=str,
                    help='Value replace argument')

parser.add_argument('--file_path', type=str,
                    help='File path argument')

# Switch
# parser.add_argument('--switch', action='store_true',
#                     help='A boolean switch')

args = parser.parse_args()

key = args.key
value = args.value
file_path = args.file_path
print ('argument list', args.file_path)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# rel_path = "2091/data.txt"
abs_file_path = os.path.join(script_dir, file_path)
print ('file path', abs_file_path)


with open(abs_file_path, 'r') as f:
    data = yaml.safe_load(f)

data['database'][key] = value

with open(file_path, 'w') as fileOutput:
    yaml.dump(data, fileOutput)
