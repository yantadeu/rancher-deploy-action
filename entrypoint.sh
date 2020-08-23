#!/bin/bash

set -e
rancher_access_key=$1
rancher_secret_key=$2
rancher_workload_url_api=$3
rancher_namespace=$4
rancher_service_name=$5
rancher_docker_image=$6

if [ -z "${rancher_access_key}" ]; then
    echo "You must specify the rancher access key."
    exit 1
fi

if [ -z "${rancher_secret_key}" ]; then
    echo "You must specify the rancher secret key."
    exit 1
fi

if [ -z "${rancher_workload_url_api}" ]; then
    echo "You must specify the rancher url api workload."
    exit 1
fi

if [ -z "${rancher_namespace}" ]; then
    echo "You must specify the rancher namespace."
    exit 1
fi

if [ -z "${rancher_service_name}" ]; then
    echo "You must specify the service name to deploy/redeploy."
    exit 1
fi

if [ -z "${rancher_docker_image}" ]; then
    echo "You must specify the docker image."
    exit 1
fi

python --version

pip install click
pip install requests

python deploy_to_rancher.py -a "${rancher_access_key}" -b "${rancher_secret_key}" -c "${rancher_workload_url_api}" -d "${rancher_namespace}" -e "${rancher_service_name}" -f "${rancher_docker_image}"

exit 0