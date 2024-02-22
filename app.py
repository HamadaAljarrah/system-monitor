from kubernetes import client, config
import subprocess
# Load Kubernetes configuration from default location
#config.load_kube_config()

# Create Kubernetes client
#api_instance = client.CoreV1Api()


def get_all_namespaces():
    try:
        # Execute the kubectl command to get namespaces
        result = subprocess.check_output(['kubectl', 'get', 'namespaces'])
        # Convert the output to a string and split it into lines
        namespaces = result.decode('utf-8').split('\n')
        # Print each namespace
        for namespace in namespaces[1:]:  # Skip the header line
            if namespace:  # Skip empty lines
                print("Namespace:", namespace.split()[0])
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve namespaces: {e}")

"""def print_all_namespaces():
    # Get all namespaces in the Kubernetes cluster
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            print("TEST:", namespace.metadata.name)
    except Exception as e:
        print(f"Failed to retrieve namespaces: {str(e)}")
        """

if __name__ == "__main__":
    get_all_namespaces()
