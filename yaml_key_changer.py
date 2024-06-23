import yaml

with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)

data['database']['host'] = '127.0.0.1'
# del data['devices']['deviceA']

with open('config.yaml', 'w') as fileOutput:
    yaml.dump(data, fileOutput)