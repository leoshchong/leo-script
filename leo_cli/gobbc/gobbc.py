from leo_cli.configure import AWS_CONFIG
import leo_cli.utilities.aws_utils as aws_utils

class Gobbc:

    def __init__(self, env, project, cert=None, key=None, duration="1h", region="eu-west-1"):
        self.project = AWS_CONFIG[project]
        self.aws_account = self.project[env]
        self.region = region
        self.access_key_id = None
        self.secret_access_key = None
        self.session_token = None
        self.duration = duration

    def refresh_wormhole_credentials(self):
        import subprocess
        gobbc_command = f"gobbc aws-credentials -account {self.aws_account} -noNewShell -mfa -duration {self.duration}"
        output = subprocess.check_output(gobbc_command, shell=True, encoding="utf-8")
        credentials = {}
        for line in output.strip().split("\n"):
            line = line.replace("export", "").strip()
            key, value = line.split("=", 1)
            credentials[key] = value

        aws_utils.write_aws_credentials(
            access_key_id=credentials["AWS_ACCESS_KEY_ID"],
            secret_access_key=credentials["AWS_SECRET_ACCESS_KEY"],
            session_token=credentials["AWS_SESSION_TOKEN"],
            region=self.region,
        )
        self.access_key_id = credentials["AWS_ACCESS_KEY_ID"]
        self.secret_access_key = credentials["AWS_SECRET_ACCESS_KEY"]
        self.session_token = credentials["AWS_SESSION_TOKEN"]
        return self.aws_account

