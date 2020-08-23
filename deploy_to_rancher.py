import getopt
import sys
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


def deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                      rancher_service_name, rancher_docker_image):
    deployment = DeployRancher(rancher_access_key, rancher_secret_key, rancher_workload_url_api, rancher_namespace,
                               rancher_service_name, rancher_docker_image)
    deployment.deploy()


if __name__ == '__main__':
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'a:b:c:d:e:f:', ['foperand', 'soperand', 'toperand', 'fooperand','fioperand', 'sioperand'])
        print(opts)
        if len(opts) != 6:
            print('usage: deploy_to_rancher.py -a <first_operand> -b <second_operand> '
                  '-c <third_operand> -d <fourth_operand> -e <fifth_operand> -f <sixth_operand>')
            sys.exit(1)
        else:
            deploy_in_rancher(opts[0][1], opts[1][1], opts[2][1], opts[3][1], opts[4][1], opts[5][1])

    except getopt.GetoptError:
        print('usage: deploy_to_rancher.py -a <first_operand> -b <second_operand> '
              '-c <third_operand> -d <fourth_operand> -e <fifth_operand> -f <sixth_operand>')
        sys.exit(1)
