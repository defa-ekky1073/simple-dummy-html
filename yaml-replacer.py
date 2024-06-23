import yaml
import sys
import argparse

filepath = [
    "config-example/apps/web.yaml", 
    "config-example/dbs/db_prod.yaml",
    "config-example/dbs/db_stg.yaml",
    "config-example/services/auth_service.yaml",
    "config-example/services/payment_service.yaml",
    "config-example/tools/log.yaml",
    "config-example/tools/monitoring.yaml",
]

def yaml_replacer_argParser():
    parser = argparse.ArgumentParser(
        prog='Yaml Replacer',
        description='replace yaml configurations'
    )

    parser.add_argument("--key", "-k", help="key parameter seperated by '.'", required=True)
    parser.add_argument("--value", "-v", help="value to replace parameter", required=True)
    return parser.parse_args()

def main(filepath):
    args = yaml_replacer_argParser()
    
    child = args.key.split(".")

    for file in filepath:
        try:
            with open(file, 'r') as stream:
                data = yaml.safe_load(stream)
            try:
                current = data
                for key in child[:-1]:
                    current = current.setdefault(key, {})
                if child[-1] in current:
                    current[child[-1]] = args.value
                    with open(file, 'w') as stream:
                        try:
                            yaml.dump(data, stream, default_flow_style=False, sort_keys=False)
                        except yaml.YAMLError as exc:
                            print(exc)
            except:
                continue
        except yaml.YAMLError as exc:
            print(exc)

main(filepath)
