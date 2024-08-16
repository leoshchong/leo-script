import click

from leo_cli.configure import profile, set_profile, COSMOS_SERVICE
from leo_cli.cosmos.cosmos import Cosmos

DEFAULT_ENV = 'live'
ENVS = ['int', 'test', 'stage', 'live', 'dns']


@click.group(help='Cosmos utilities')
def cosmos():
    pass


@cosmos.command(help='SSH into EC2 instances')
@click.option('--env', prompt=True, default=profile.get('env', 'live'), type=click.Choice(ENVS), help='Environment')
@click.option('--service', prompt="Services: (" + ", ".join(map(str, COSMOS_SERVICE)) + ")", default=profile.get('service', "federated-id"),
              help='Cosmos service')
@click.option('--instance', prompt=True, default=profile.get('instance', 0), help='Instance')
def ssh(env, service, instance):
    try:
        click.echo(f"Starting SSH..")
        cosmos_api = Cosmos()
        cosmos_api.ssh(service, env, instance)

    except Exception as ex:
        click.echo(f"Failed to Cosmos SSH. {str(ex)}")
    finally:
        set_profile(name='env', value=env)
        set_profile(name='service', value=service)
        set_profile(name='instance', value=instance)
