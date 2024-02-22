from kubernetes import client, config
# Load Kubernetes configuration from default location
kube_config_path = '/root/.kube/config/client.config'
kube_config = '''apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://10.1.1.6:16443
  name: microk8s-cluster
contexts:
- context:
    cluster: microk8s-cluster
    user: admin
  name: microk8s
current-context: microk8s
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: DATA+OMITTED
    client-key-data: DATA+OMITTED'''

# Load Kubernetes configuration from the specified file
config.load_kube_config(kube_config)
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
