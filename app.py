from kubernetes import client, config
import json

def get_namespace_pod_metrics(namespace, api_instance):
    try:
        # Get pod metrics from the metrics API
        pod_metrics = api_instance.list_namespaced_pod_metric(namespace).items
        
        # Extract resource usage information for each pod
        pod_metrics_info = {}
        for pod_metric in pod_metrics:
            pod_name = pod_metric.metadata.name
            cpu_usage = pod_metric.containers[0].usage["cpu"]
            memory_usage = pod_metric.containers[0].usage["memory"]
            pod_metrics_info[pod_name] = {"CPU Usage": cpu_usage, "Memory Usage": memory_usage}
        
        return pod_metrics_info
    except Exception as e:
        return f"Failed to retrieve pod metrics for namespace {namespace}: {str(e)}"


def get_namespace_resource_usage(namespace, api_instance):
    try:
        # Get namespace resource usage
        namespace_metrics = get_namespace_pod_metrics(namespace, api_instance)
        
        cpu_total_usage = 0
        memory_total_usage = 0

        # Calculate total CPU and memory usage
        for metric in namespace_metrics.items:
            cpu_total_usage += float(metric.containers[0].usage['cpu'].rstrip('n')) if 'cpu' in metric.containers[0].usage else 0
            memory_total_usage += int(metric.containers[0].usage['memory'].rstrip('Ki')) if 'memory' in metric.containers[0].usage else 0

        
        return {
            "Namespace": namespace,
            "CPU Usage": cpu_total_usage,
            "Memory Usage": memory_total_usage
        }
    except Exception as e:
        return f"Failed to retrieve resource usage for namespace {namespace}: {str(e)}"

def print_all_namespaces(api_instance):
    try:
        # Get all namespaces in the Kubernetes cluster
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            namespace_name = namespace.metadata.name
            print(f"Namespace: {namespace_name}")
            resource_usage = get_namespace_resource_usage(namespace_name, api_instance)
            if isinstance(resource_usage, dict):
                print(json.dumps(resource_usage, indent=4))
            else:
                print(resource_usage)
            print("\n")
    except Exception as e:
        print(f"Failed to retrieve namespaces: {str(e)}")

if __name__ == "__main__":
    try:
        # Load Kubernetes configuration
        config.load_incluster_config()
        # Create Kubernetes client
        api_instance = client.CoreV1Api()
        # Print resource usage for all namespaces
        print_all_namespaces(api_instance)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
