FROM python:3.8

COPY . /

RUN chmod +x /entrypoint.sh
RUN pip install -r /requirements.txt

CMD python deploy_to_rancher.py --rancher_access_key=$ENV1 --rancher_secret_key="${rancher_secret_key}" --rancher_workload_url_api="${rancher_workload_url_api}" --rancher_namespace="${rancher_namespace}" --rancher_service_name="${rancher_service_name}" --rancher_docker_image="${rancher_docker_image}"

ENTRYPOINT [ "/entrypoint.sh" ]
