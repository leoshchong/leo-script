import click

from leo_cli.configure import profile, set_profile
from leo_cli.gobbc.gobbc import Gobbc
from leo_cli.configure import AWS_CONFIG

DEFAULT_ENV = 'live'
ENVS = ['int', 'test', 'stage', 'live']
PROJECTS = ['scv', 'analysis']


@click.group(help='Gobbc utilities')
def gobbc():
    pass


@gobbc.command(help='Refresh AWS credentials')
@click.option('--env', prompt=True, default=profile.get('env', 'live'), type=click.Choice(ENVS), help='Environment')
@click.option('--project', prompt=True, default=profile.get('project', 'scv'), type=click.Choice(list(AWS_CONFIG.keys())), help='Environment')
def refresh(env, project):
    try:

        gobbc_api = Gobbc(env=env, project=project)
        gobbc_api.refresh_wormhole_credentials()
        click.echo(f"Successfully refreshed {env} {project} AWS credentials.")
    except Exception as ex:
        click.echo(f"Failed to refresh AWS credentials. {str(ex)}")
    finally:
        set_profile(name='env', value=env)
        set_profile(name='project', value=project)
