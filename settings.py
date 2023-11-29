import yaml

def load_settings():
    """
    Load the settings from the settings.yml file in the root of the novel dir
    """
    settings = {}
    with open('./settings.yml', 'r') as settings_file:
        settings = yaml.safe_load(settings_file)
    
    return settings



