import sys
import click
import requests


class DeployRancher:
    def __init__(self, rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                 rancher_service_name, rancher_docker_image):
        self.access_key = rancher_access_key
        self.secret_key = rancher_secret_key
        self.rancher_workload_url_api = rancher_workload_url_api
        self.rancher_namespace = rancher_namespace
        self.service_name = rancher_service_name
        self.rancher_deployment_path = '/deployment:'+self.rancher_namespace+':' + self.service_name
        self.docker_image = rancher_docker_image

    def deploy(self):
        rget = requests.get(self.rancher_workload_url_api + self.rancher_deployment_path,
                            auth=(self.access_key, self.secret_key))
        response = rget.json()
        if 'status' in response and response['status'] == 404:
            config = {
                "containers": [{
                    "imagePullPolicy": "Always",
                    "image": self.docker_image,
                    "name": self.service_name,
                }],
                "namespaceId": self.rancher_namespace,
                "name": self.service_name
            }

            requests.post(self.rancher_workload_url_api,
                          json=config, auth=(self.access_key, self.secret_key))
        else:
            response['containers'][0]['image'] = self.docker_image

            requests.put(self.rancher_workload_url_api + self.rancher_deployment_path + '?action=redeploy',
                         json=response, auth=(self.access_key, self.secret_key))


@click.command()
@click.option('--deploy', default=0,
              help='deploy')
@click.option('--rancher_access_key', default=None,
              help='access key api')
@click.option('--rancher_secret_key', default=None,
              help='secret key api')
@click.option('--rancher_workload_url_api', default=None,
              help='url api workload')
@click.option('--rancher_namespace', default=None,
              help='name of namespace')
@click.option('--rancher_service_name', default=None,
              help='name of service')
@click.option('--rancher_docker_image', default=None,
              help='name of docker repo')
def deploy_in_rancher(deploy, rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                      rancher_service_name, rancher_docker_image):
    deployment = DeployRancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                               rancher_service_name, rancher_docker_image)
    deployment.deploy()


if __name__ == '__main__':
    try:
        deploy_in_rancher()
        sys.exit(0)
    except ValueError as e:
        print(e)
        sys.exit(1)
