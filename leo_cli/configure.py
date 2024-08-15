import click
from pathlib import Path

AWS_CONFIG = {
    "scv": {
        "int": "977228593394",
        "test": "977228593394",
        "stage": "977228593394",
        "live": "347875564198",
        "dns": "511603603783"
    },
    "uas": {
        "int": "153944352978",
        "test": "153944352978",
        "stage": "153944352978",
        "live": "267802866328",
        "dns": "511603603783"
    },
    "analysis": {
        "live": "160230170054"
    }
}


def app_dir():
    return click.get_app_dir(app_name='leo-cli')


def profile_path(app_dir):
    from os import path
    return path.join(app_dir, 'profile.ini')


def read_profile(app_dir):
    from configparser import ConfigParser
    path = profile_path(app_dir)
    parser = ConfigParser()
    parser.read([path])
    profile = {}
    for section in parser.sections():
        for name, value in parser.items(section):
            profile[name] = value
    return profile


def write_profile(app_dir, profile):
    import os
    from configparser import ConfigParser
    path = profile_path(app_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        parser = ConfigParser()
        section_name = 'profile'
        parser.add_section(section_name)
        for name, value in profile.items():
            parser.set(section=section_name, option=name, value=value)
        parser.write(f)


def set_profile(name, value):
    profile = read_profile(app_dir=app_dir())
    if name not in profile or profile[name] != str(value):
        profile[name] = str(value)
        write_profile(app_dir=app_dir(), profile=profile)


def cert_config_file():
    return Path.home().joinpath(".leo-cli")


profile = read_profile(app_dir=app_dir())
