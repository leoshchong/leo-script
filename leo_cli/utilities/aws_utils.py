def write_aws_credentials(access_key_id, secret_access_key, session_token, region):
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


def sts_get_caller_identity():
    import boto3
    sts_client = boto3.client('sts')
    response = sts_client.get_caller_identity()
    return response['Account'], response['UserId'], response['Arn']