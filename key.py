import yaml
path = (str)(input("Enter the path of the yaml file: "))
with open (path, 'r') as file:
    data = yaml.safe_load(file)
_data = data
isFinal = False
keyParentToChange = (str)(input("Enter the key parent you want to change: "))
keyToChange = (str)(input("Enter the key you want to change: "))

_data[keyParentToChange][keyToChange] = input("Enter the new value: ")

with open(path, 'w') as file:
    yaml.dump(_data, file)

