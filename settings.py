from yaml import safe_load

with open("settings.yaml") as f:
    settings = safe_load(f)
