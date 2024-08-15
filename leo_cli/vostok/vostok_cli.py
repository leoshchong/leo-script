import click

from leo_cli.configure import profile, set_profile

DEFAULT_ENV = 'live'
ENVS = ['int', 'test', 'stage', 'live', 'dns']
PROJECTS = ['comments', 'moderation']


@click.group(help='Vostok utilities')
def vostok():
    pass


@vostok.command(help='Refresh AWS credentials')
@click.option('--env', prompt=True, default=profile.get('env', 'live'), type=click.Choice(ENVS), help='Environment')
@click.option('--project', prompt=True, default=profile.get('project', 'comments'), type=click.Choice(PROJECTS), help='Environment')
def refresh(env, project):
    try:
        from leo_cli.vostok.vostok import Vostok
        vostok_api = Vostok(env=env, project=project)
        vostok_api.refresh_wormhole_credentials()
        click.echo(f"Successfully refreshed {env} {project} AWS credentials.")
    except Exception as ex:
        click.echo(f"Failed to refresh AWS credentials. {str(ex)}")
    finally:
        set_profile(name='env', value=env)
        set_profile(name='project', value=project)
