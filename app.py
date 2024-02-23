from kubernetes import client, config
import json

# Load Kubernetes configuration
config.load_incluster_config()
# Create Kubernetes client
api_instance = client.MetricsV1Api()

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
    pods = api_instance.list_namespaced_pod(namespace)
    for pod in pods.items:
        pod_name = pod.metadata.name
        pod_namespace = pod.metadata.namespace

        # Get pod metrics
        metrics = api_instance.list_namespaced_pod_metric(namespace=pod_namespace)
        for item in metrics.items:
            if item.metadata.name == pod_name:
                cpu_usage = item.containers[0].usage["cpu"]
                memory_usage = item.containers[0].usage["memory"]
                print(f"Pod: {pod_name}, Namespace: {pod_namespace}, CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}")

if __name__ == "__main__":
    try:
        # Print resource usage for all namespaces
        print_all_namespaces(api_instance)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
