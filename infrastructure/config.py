import configparser
import os

#environment = os.environ.get("ENVIRONMENT", "TEST")
_config = configparser.ConfigParser()
_config.read(os.path.dirname(__file__) + "/../config/config.ini")


def get_key(env, key):
    env_value = os.environ.get(key)
    if env_value:
        return env_value
    else:
        return _config[env][key]