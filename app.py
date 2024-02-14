from kubernetes import client, config

from flask import Flask

# Create a Flask app instance
app = Flask(__name__)
# Load Kubernetes configuration from default location
#config.load_kube_config()

# Create Kubernetes client
#api_instance = client.CoreV1Api()
"""
def get_namespace_resource_usage(namespace):
    #Get resource usage (CPU and memory) for a given namespace.
    try:
        # Get namespace resource usage
        namespace_metrics = api_instance.list_namespaced_pod(namespace)
        
        cpu_total_usage = 0
        memory_total_usage = 0

        # Calculate total CPU and memory usage
        for pod in namespace_metrics.items:
            for container in pod.spec.containers:
                cpu_total_usage += container.usage['cpu']
                memory_total_usage += container.usage['memory']
        
        return {
            "Namespace": namespace,
            "CPU Usage": cpu_total_usage,
            "Memory Usage": memory_total_usage
        }
    except Exception as e:
        return f"Failed to retrieve resource usage: {str(e)}"
"""

@app.route('/namespace-usage/<namespace>')
def namespace_usage(namespace):
    """Endpoint to get resource usage (CPU and memory) for a given namespace."""
    print("TEST2")
    #usage_info = get_namespace_resource_usage(namespace)
    return "Hello"

if __name__ == "__main__":
    print("TEEST1")
    app.run(host='0.0.0.0', port=8080, debug=False)
