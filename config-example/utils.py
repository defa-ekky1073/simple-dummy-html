# libraries
import os
import yaml

# function to read yaml files
def load_yaml_files(directory):
  yaml_files = []
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith('.yaml') or file.endswith('.yml'):
        path = os.path.join(root, file)
        yaml_files.append(path)
  return yaml_files

def read_yaml_contents(files):
  yaml_contents = {}
  for file in files:
    with open(file, 'r') as f:
      try:
        content = yaml.safe_load(f)
        yaml_contents[file] = content
      except:
        print('Something went wrong')
  return yaml_contents

def update_value(obj, key, new_value):
  if isinstance(obj, dict):
    for k, v in obj.items():
      if k == key:
        obj[k] = new_value
      elif isinstance(v, (dict, list)):
        update_value(v, key, new_value)
  elif isinstance(obj, list):
    for item in obj:
      update_value(item, key, new_value)
  return obj

def replace_key_value(file, contents, key, value):
  updated_value = update_value(contents, key, value)
  with open(file, 'w') as f:
    yaml.safe_dump(updated_value, f)
  