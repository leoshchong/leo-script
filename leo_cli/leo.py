from pathlib import Path
from leo_cli.configure import cert_config_file
import click
from leo_cli.vostok.vostok_cli import vostok
from leo_cli.gobbc.gobbc_cli import gobbc
from leo_cli.cosmos.cosmos_cli import cosmos

APP_VERSION = '0.0.3'


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    pass


@cli.command(help='Version details')
def version():
    click.echo(APP_VERSION)


def read_setup(key):
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read(cert_config_file())
        return config.get("Authentication", key)
    except:
        return ""


@cli.command(help='Initial Setup')
@click.option('--key', prompt=True, default=read_setup("Key"), help='Dev Private Key Path')
@click.option('--cert', prompt=True, default=read_setup("Cert"), help='Dev Cert Path')
@click.option('--email', prompt=True, default=read_setup("EmailAddress"), help='BBC Email Address')
def setup(key, cert, email):
    with open(cert_config_file(), 'w') as fsetup:
        fsetup.write("[Authentication]\n")
        fsetup.write(f"Cert={cert}\n")
        fsetup.write(f"Key={key}\n")
        fsetup.write(f"EmailAddress={email}\n")
    with open(Path.home().joinpath(".aws").joinpath("config"), 'w') as fconfig:
        fconfig.write("[default]\n")
        fconfig.write(f"region = eu-west-1\n")


cli.add_command(vostok)
cli.add_command(gobbc)
cli.add_command(cosmos)

if __name__ == '__main__':
    cli()
