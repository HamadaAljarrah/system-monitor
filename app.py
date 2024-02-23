from kubernetes import client, config
import json

# Load Kubernetes configuration
config.load_incluster_config()
# Create Kubernetes client
api_instance = client.CoreV1Api()
cust = client.CustomObjectsApi()

def print_all_namespaces(api_instance):
    # Get all namespaces in the Kubernetes cluster
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            print(f"Namespace: {namespace_name}")
            get_pod_metrics(namespace_name)
            print("\n")
    except Exception as e:
        print(f"Failed to retrieve namespaces: {str(e)}")

def get_pod_metrics(namespace):
    pod_metrics_list = cust.list_namespaced_custom_object('metrics.k8s.io', 'v1beta1', namespace, 'pods')
    for pod_metrics in pod_metrics_list['items']:
        pod_name = pod_metrics['metadata']['name']
        for container in pod_metrics['containers']:
            container_name = container['name']
            cpu_usage = container['usage']['cpu']
            memory_usage = container['usage']['memory']
            print(f"Pod: {pod_name}, Container: {container_name}, CPU: {cpu_usage}, Memory: {memory_usage}")

if __name__ == "__main__":
    try:
        # Print resource usage for all namespaces
        print_all_namespaces(api_instance)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
