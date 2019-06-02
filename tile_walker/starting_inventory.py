import yaml

inventory = {}

with open("inventory.yaml", 'r') as stream:
    try:
        starting_inventory = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

