from kubernetes import client, config

# Load Kubernetes configuration from default location
config.load_kube_config()

# Create Kubernetes client
api_instance = client.CoreV1Api()

def print_all_namespaces():
    # Get all namespaces in the Kubernetes cluster
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            print("TEST:", namespace.metadata.name)
    except Exception as e:
        print(f"Failed to retrieve namespaces: {str(e)}")

if __name__ == "__main__":
    print_all_namespaces()
