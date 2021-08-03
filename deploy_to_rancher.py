import os
import sys
import requests
from requests.api import request


class DeployRancher:
    def __init__(self, rancher_access_key, rancher_secret_key, rancher_url_api,
                 rancher_service_name, rancher_docker_image):
        self.access_key = rancher_access_key
        self.secret_key = rancher_secret_key
        self.rancher_url_api = rancher_url_api
        self.service_name = rancher_service_name
        self.docker_image = rancher_docker_image
        self.rancher_deployment_path = ''
        self.rancher_namespace = ''
        self.rancher_workload_url_api = ''

    def get_rancher(self):
        return requests.get('{}/projects'.format(self.rancher_url_api), auth=(self.access_key, self.secret_key))

    def deploy(self):
        rp = self.get_rancher()
        projects = rp.json()
        for p in projects['data']:
            w_url = '{}/projects/{}/workloads'.format(self.rancher_url_api, p['id'])
            rw = requests.get(w_url, auth=(self.access_key, self.secret_key))
            workload = rw.json()
            for w in workload['data']:
                if w['name'] == self.service_name:
                    self.rancher_workload_url_api = w_url
                    self.rancher_deployment_path = w['links']['self']
                    self.rancher_namespace = w['namespaceId']
                    break
            if self.rancher_deployment_path != '':
                break

        rget = requests.get(self.rancher_deployment_path,
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

            requests.put(self.rancher_deployment_path + '?action=redeploy',
                         json=response, auth=(self.access_key, self.secret_key))
        print(f"\033[0;32m Deploy complete!{ rget }")
        sys.exit(0)


def deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                      rancher_service_name, rancher_docker_image):
    deployment = DeployRancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                               rancher_service_name, rancher_docker_image)
    deployment.deploy()
    return deployment


if __name__ == '__main__':
    rancher_access_key = 'token-n123'
    rancher_secret_key = 'hjnjnh5rbwwjp55l96crhtgfp7h7psgmhbfftfb4jvc8bmwp7l6zl8'
    rancher_url_api = 'https://rancher.d3.do/v3'
    rancher_service_name = 'd3-site-content'
    rancher_docker_image = '929907635541.dkr.ecr.us-east-1.amazonaws.com/d3-site-content:f3f87b6103593e676dca7188b39eb881fd047ea3'
    rancher_docker_image_latest = '929907635541.dkr.ecr.us-east-1.amazonaws.com/d3-site-content:f3f87b6103593e676dca7188b39eb881fd047ea3'
    
    try:
        deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                            rancher_service_name, rancher_docker_image)
        
        if rancher_docker_image_latest != None and rancher_docker_image_latest != "":
            deploy_in_rancher(rancher_access_key, rancher_secret_key, rancher_url_api, 
                                rancher_service_name, rancher_docker_image_latest)
              
    except KeyError as a:
        request_error = DeployRancher(rancher_access_key, rancher_secret_key, rancher_url_api,
                            rancher_service_name, rancher_docker_image)
        print(f"""
              \033[1;31m Error ocurred in request of {a}!
               Response --> {request_error.get_rancher().json()} \033[0;0m
                """)
        sys.exit(1)
        
        
 