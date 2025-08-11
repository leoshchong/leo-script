import leo_cli.utilities.aws_utils as aws_utils

class Iam:

    def __init__(self, region="eu-west-1"):
        self.region = region


    def assume_role(self, role_arn, session_name):
        import subprocess
        assume_command = f"aws sts assume-role --role-arn {role_arn} --role-session-name {session_name}"
        output = subprocess.check_output(assume_command, shell=True, encoding="utf-8")
        print(output)
        import json
        credentials = json.loads(output)["Credentials"]

        # set the AWS credentials
        aws_utils.write_aws_credentials(
            access_key_id=credentials["AccessKeyId"],
            secret_access_key=credentials["SecretAccessKey"],
            session_token=credentials["SessionToken"],
            region=self.region
        )



