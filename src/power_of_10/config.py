import yaml


def get_config(file_name:str) -> dict[dict[str,str]]:
    """Load app config from a given yaml file.
    >>> config = get_config("config.yml")

    :param str file_name: Name of file.
    :returns: Dictionary of athlete IDs
    :rtype: dict[dict[str,str]]
    """
    with open(file_name, "r") as config_file:
        return yaml.safe_load(config_file.read())