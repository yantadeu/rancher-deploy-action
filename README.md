# Action to deploy image in Rancher using Rancher API

## Inputs

### `rancher_access_key`

**Required** API Access key created in Rancher.

### `rancher_secret_key`

**Required** API Secret key created in Rancher.

### `rancher_workload_url_api`

**Required** API Url of your rancher project workload.

### `rancher_namespace`

**Required** Your namespace project . Default `"default"`.

### `service_name`

**Required** NAME OF YOUR SERVICE ON RANCHER CLUSTER WHAT YOU WANT DEPLOY.

### `docker_image`

**Required** URL TO YOUR DOCKER IMAGE (Ex: AWS or DOCKER REGISTRY).

## Outputs

### `http response`

Response code to

## Example usage

uses: actions/rancher-deploy-action@v1
with:
  rancher_access_key: 'XXXXXXX',
  rancher_secret_key: 'XXXXXXX',
  rancher_workload_url_api: 'https://rancher.YOUR-DOMAIN.COM/v3/project/PROJECT_ID/workloads',
  rancher_namespace: 'default',
  service_name: 'NAME OF YOUR SERVICE ON RANCHER CLUSTER',
  docker_image: 'URL TO YOUR DOCKER IMAGE (Ex: AWS or DOCKER REGISTRY)'