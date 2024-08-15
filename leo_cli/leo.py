from pathlib import Path

import click
from leo_cli.vostok.vostok_cli import vostok
from leo_cli.gobbc.gobbc_cli import gobbc

APP_VERSION = '0.0.1'


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    click.echo('Hello World!')
    pass


@cli.command(help='Version details')
def version():
    click.echo(APP_VERSION)


@cli.command(help='Initial Setup')
@click.option('--key', prompt=True, help='Dev Private Key Path')
@click.option('--cert', prompt=True, help='Dev Cert Path')
def setup(key, cert):
    with open(cert_config_file(), 'w') as fsetup:
        fsetup.write("[Authentication]\n")
        fsetup.write(f"Cert={cert}\n")
        fsetup.write(f"Key={key}\n")
    with open(Path.home().joinpath(".aws").joinpath("config"), 'w') as fconfig:
        fconfig.write("[default]\n")
        fconfig.write(f"region = eu-west-1\n")


def cert_config_file():
    return Path.home().joinpath(".leo-cli")


cli.add_command(vostok)
cli.add_command(gobbc)

if __name__ == '__main__':
    cli()
