from kubernetes import client, config
# Load Kubernetes configuration from default location
kube_config_path = '/root/.kube/config/client.config'


# Load Kubernetes configuration from the specified file
config.load_incluster_config()
# Create Kubernetes client
api_instance = client.CoreV1Api()

"""def print_config_file():
    config_file_path = "/root/.kube/config/client.config"
    try:
        with open(config_file_path, "r") as config_file:
            config_content = config_file.read()
            print(config_content)
    except FileNotFoundError:
        print(f"Config file not found at: {config_file_path}")"""

def print_all_namespaces():
    # Get all namespaces in the Kubernetes cluster
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            print("TEST:", namespace.metadata.name)
    except Exception as e:
        print(f"Failed to retrieve namespaces: {str(e)}")

if __name__ == "__main__":
    #print_config_file()
    print_all_namespaces()
