from kubernetes import client, config
import json

def get_namespace_resource_usage(namespace, api_instance):
    # Get resource usage (CPU and memory) for a given namespace.
    try:
        # Get namespace resource usage
        namespace_metrics = api_instance.list_namespaced_pod(namespace)
        
        cpu_total_usage = 0
        memory_total_usage = 0

        # Calculate total CPU and memory usage
        for pod in namespace_metrics.items:
            for container in pod.spec.containers:
                if 'usage' in container:
                    cpu_total_usage += container.usage['cpu'] if 'cpu' in container.usage else 0
                    memory_total_usage += container.usage['memory'] if 'memory' in container.usage else 0
        
        return {
            "Namespace": namespace,
            "CPU Usage": cpu_total_usage,
            "Memory Usage": memory_total_usage
        }
    except Exception as e:
        return f"Failed to retrieve resource usage for namespace {namespace}: {str(e)}"

def print_all_namespaces(api_instance):
    # Get all namespaces in the Kubernetes cluster
    try:
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
