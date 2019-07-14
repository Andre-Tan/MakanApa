from yaml import safe_load


def get_config(config_filename):
    """
    Load a YAML config file from disk
    :param config_filename:
    :return: dictionary
    """
    try:
        with open(config_filename, "r") as handle:
            config = safe_load(handle)
    except Exception as e:
        print("Error raised during config setup: {}".format(e))
        exit(1)

    return config

class Config(object):
    SECRET_KEY = "you-will-never-guess"