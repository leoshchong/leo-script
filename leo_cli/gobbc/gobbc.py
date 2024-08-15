from leo_cli.configure import AWS_CONFIG


class Gobbc:

    def __init__(self, env, project, cert=None, key=None, region="eu-west-1"):
        self.project = AWS_CONFIG[project]
        self.aws_account = self.project[env]
        self.region = region
        self.access_key_id = None
        self.secret_access_key = None
        self.session_token = None

    def refresh_wormhole_credentials(self):
        import subprocess
        gobbc_command = f"gobbc aws-credentials -account {self.aws_account} -noNewShell -mfa"
        output = subprocess.check_output(gobbc_command, shell=True, encoding="utf-8")
        credentials = {}
        for line in output.strip().split("\n"):
            line = line.replace("export", "").strip()
            key, value = line.split("=", 1)
            credentials[key] = value

        self.write_aws_credentials(
            access_key_id=credentials["AWS_ACCESS_KEY_ID"],
            secret_access_key=credentials["AWS_SECRET_ACCESS_KEY"],
            session_token=credentials["AWS_SESSION_TOKEN"],
            region=self.region,
        )
        self.access_key_id = credentials["AWS_ACCESS_KEY_ID"]
        self.secret_access_key = credentials["AWS_SECRET_ACCESS_KEY"]
        self.session_token = credentials["AWS_SESSION_TOKEN"]

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
