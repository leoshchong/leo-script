from leo_cli.leo import cert_config_file
import requests
import time
import click


class Cosmos:

    def __init__(self, cert=None, key=None, region="eu-west-1"):
        import configparser
        config = configparser.ConfigParser()
        config.read(cert_config_file())
        self.cert = config.get("Authentication", "Cert")
        self.key = config.get("Authentication", "Key")
        self.email_address = config.get("Authentication", "EmailAddress").lower()
        self.region = region

    def cosmos_get_request_body(self, url):
        import json
        response = json.loads(
            requests.get(
                f"https://cosmos.api.bbci.co.uk/v1{url}",
                cert=(self.cert, self.key)
            ).text
        )
        return response

    def cosmos_post_request(self, url, body):
        return requests.post(
            f"https://cosmos.api.bbci.co.uk/v1{url}",
            cert=(self.cert, self.key),
            json=body
        )

    def get_instances(self, service, environment):
        instances_response = self.cosmos_get_request_body(
            f"/services/{service}/{environment}/main_stack/instances"
        )

        running_instances = instances_response["instances"]

        if not isinstance(running_instances, list):
            print(running_instances)
            return None

        return running_instances

    def check_logged_in(self, service, environment, instance_id):
        response = self.cosmos_get_request_body(f"/services/{service}/{environment}/logins")
        for login in response["logins"]:
            if (
                login["instance_id"] == instance_id
                and login["status"] == "current"
                and login["created_by"]["email_address"].lower() == self.email_address
            ):
                return True
        return False

    def permit_ssh_access(self, service, environment, instance):
        if isinstance(instance, str) and instance.isdigit():
            instance = int(instance)

        if not isinstance(instance, int):
            raise Exception("Invalid instance number: not an integer")

        instance_number = instance
        if instance < 0:
            raise Exception(f"Invalid instance number: {instance}")

        running_instances = self.get_instances(service, environment)
        click.echo(f"Total number of instances {len(running_instances)}")
        instance_id = running_instances[instance]["id"]
        click.echo("Found instance " + instance_id)
        if self.check_logged_in(service, environment, instance_id):
            click.echo("Found existing login.")
            return running_instances[instance]["private_ip_address"]

        data = {"instance_id": instance_id}
        click.echo("Existing login not found, getting login from cosmos..")
        response = self.cosmos_post_request(f"/services/{service}/{environment}/logins", data)
        if response.status_code != 201:
            click.echo(response.text)
            raise Exception("Get Login from cosmos unsuccessful")

        time.sleep(5)
        for i in range(10):
            if self.check_logged_in(service, environment, instance_id):
                break
            time.sleep(1)

        running_instances = self.get_instances(service, environment)
        for running_instance in running_instances:
            if running_instance["id"] == instance_id:
                return running_instance["private_ip_address"]

        raise Exception(f"Instance {instance_id} not found")

    def ssh(self, service, environment, instance):
        import subprocess
        ip_address = self.permit_ssh_access(service, environment, instance)
        click.echo(f"Running: /usr/bin/ssh {ip_address},eu-west-1")
        subprocess.call(["/usr/bin/ssh", f"{ip_address},eu-west-1"])
