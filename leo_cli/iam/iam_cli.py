import click

from leo_cli.configure import profile, set_profile
from leo_cli.iam.iam import Iam
import leo_cli.utilities.aws_utils as aws_utils

DEFAULT_ENV = 'int'
ENVS = ['int', 'test', 'stage', 'live']


@click.group(help='IAM Role utilities')
def iam():
    pass


@iam.command(help='Assume AWS role')
@click.option('--role-arn', prompt=True, default=profile.get('role_arn', 'default-role'), help='AWS Role Name')
@click.option('--session-name', prompt=True, default=profile.get('session_name', 'default-session'), help='AWS Session Name')
def assume(role_arn, session_name):
    try:
        assume_obj = Iam(region="eu-west-1")
        assume_obj.assume_role(role_arn, session_name)
        click.echo(f"Successfully assumed {role_arn}.")

        # Print the account, user ID, and ARN.
        account, user_id, arn = aws_utils.sts_get_caller_identity()
        click.echo(f"Assumed Role Details:\nAccount: {account}\nUser ID: {user_id}\nARN: {arn}")

    except Exception as ex:
        click.echo(f"Failed to assume AWS role. {str(ex)}")
    finally:
        set_profile(name='role_arn', value=role_arn)
        set_profile(name='session_name', value=session_name)

@iam.command(help='Get current AWS identity')
def whoami():
    try:
        account, user_id, arn = aws_utils.sts_get_caller_identity()
        click.echo(f"Current AWS Identity:\nAccount: {account}\nUser ID: {user_id}\nARN: {arn}")
    except Exception as ex:
        click.echo(f"Failed to retrieve AWS identity. {str(ex)}")