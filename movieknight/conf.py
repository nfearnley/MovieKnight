import toml

from pathlib import Path

import appdirs


class ConfigException(Exception):
    pass


def getDataDir():
    appname = "MovieKnight"
    appauthor = "TiltedZed"
    datadir = Path(appdirs.user_data_dir(appname, appauthor))
    return datadir


confpath = getDataDir() / "movieknight.conf"


try:
    configDict = toml.load(confpath)
except FileNotFoundError as e:
    raise ConfigException(f"Configuration file not found: {e.filename}")


authtoken = configDict.get("discord", {}).get("authtoken")
if not authtoken:
    raise ConfigException("Missing authtoken [discord.authtoken]")
