import click

from configure import profile

DEFAULT_ENV = 'live'
ENVS = ['int', 'test', 'stage', 'live']
PROJECTS = ['comments', 'moderation', 'analysis']


@click.group(help='Gobbc utilities')
def gobbc():
    pass


@gobbc.command(help='Refresh AWS credentials')
@click.option('--env', prompt=True, default=profile.get('env', 'live'), type=click.Choice(ENVS), help='Environment')
@click.option('--project', prompt=True, default=profile.get('project', 'comments'), type=click.Choice(PROJECTS), help='Environment')
def refresh(env, project):
    try:
        from gobbc.gobbc import Gobbc
        gobbc_api = Gobbc(env=env, project=project)
        gobbc_api.refresh_wormhole_credentials()
        click.echo(f"Successfully refreshed {env} {project} AWS credentials.")
    except Exception as ex:
        click.echo(f"Failed to refresh AWS credentials. {str(ex)}")
    finally:
        from configure import set_profile
        set_profile(name='env', value=env)
        set_profile(name='project', value=project)
