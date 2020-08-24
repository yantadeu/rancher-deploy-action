import getopt
import os
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
        self.rancher_deployment_path = '/deployment:' + self.rancher_namespace + ':' + self.service_name
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


def deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                      rancher_service_name, rancher_docker_image):
    deployment = DeployRancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                               rancher_service_name, rancher_docker_image)
    deployment.deploy()


if __name__ == '__main__':
    rancher_access_key = os.getenv('INPUT_RANCHER_ACCESS_KEY')
    print(rancher_access_key)
    rancher_secret_key = os.getenv('INPUT_RANCHER_SECRET_KEY')
    rancher_workload_url_api = os.getenv('INPUT_RANCHER_WORKLOAD_URL_API')
    rancher_namespace = os.getenv('INPUT_RANCHER_NAMESPACE')
    rancher_service_name = os.getenv('INPUT_SERVICE_NAME')
    rancher_docker_image = os.getenv('INPUT_DOCKER_IMAGE')
    try:

        deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                          rancher_service_name, rancher_docker_image)

    except getopt.GetoptError:
        print('usage: deploy_to_rancher.py <first_operand> <second_operand> '
              '<third_operand> <fourth_operand> <fifth_operand> <sixth_operand>')
        sys.exit(1)
