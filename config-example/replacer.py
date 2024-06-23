# libraries
import argparse
import os
from utils import load_yaml_files, read_yaml_contents, replace_key_value

# get input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key')
parser.add_argument('-v', '--value')
args = parser.parse_args()
args_key = args.key
args_value = args.value

working_dir = os.getcwd()

files = load_yaml_files(working_dir)
contents = read_yaml_contents(files)

try:
  for file, content in contents.items():
    replace_key_value(file, content, args_key, args_value)
    print(f'Successfully update key `{args_key}` to `{args_value}` value')
except:
  print('Failed to replace file')