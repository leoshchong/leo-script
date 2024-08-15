VOSTOK_CONFIG = {
    "scv": {
        "aws": {
            "int": "977228593394",
            "test": "977228593394",
            "stage": "977228593394",
            "live": "347875564198",
            "dns": "511603603783"
        }
    }
}


class Vostok:

    def __init__(self, env, project, cert=None, key=None, region="eu-west-1"):
        self.project = VOSTOK_CONFIG[project]
        self.aws_account = self.project["aws"][env]
        import configparser
        from pathlib import Path
        credentials = configparser.ConfigParser()
        credentials.read(Path.home().joinpath(".leo-cli"))
        self.cert = credentials.get("Authentication", "Cert")
        self.key = credentials.get("Authentication", "Key")
        self.region = region
        self.access_key_id = None
        self.secret_access_key = None
        self.session_token = None

    def refresh_wormhole_credentials(self):
        import json
        import requests
        credentials = json.loads(
            requests.get(
                f"https://wormhole.api.bbci.co.uk/account/{self.aws_account}/credentials",
                cert=(self.cert, self.key)
            ).text
        )
        self.write_aws_credentials(
            access_key_id=credentials["accessKeyId"],
            secret_access_key=credentials["secretAccessKey"],
            session_token=credentials["sessionToken"],
            region=self.region,
        )
        self.access_key_id = credentials["accessKeyId"]
        self.secret_access_key = credentials["secretAccessKey"]
        self.session_token = credentials["sessionToken"]

    def write_aws_credentials(self, access_key_id, secret_access_key, session_token, region):
        import os
        aws_dir = f"{os.path.expanduser('~')}/.aws"
        if not os.path.exists(aws_dir):
            os.makedirs(aws_dir)
        credentials_file = f"{aws_dir}/credentials"
        with open(credentials_file, "w") as fp:
            fp.write(
                f"[default]\nregion = {region}\naws_access_key_id = {access_key_id}\naws_secret_access_key = {secret_access_key}"
                f"\naws_session_token = {session_token}\n".strip()
            )
