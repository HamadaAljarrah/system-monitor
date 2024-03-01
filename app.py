from kubernetes import client, config
import json
from datetime import datetime
import pymongo
import time
import sched
import os
# Ersätt med din MongoDB-anslutningsinformation

MONGO_HOST = 'cluster0.hjzgptm.mongodb.net'
MONGO_PORT = 27017
MONGO_DB = 'CloudSaver'
MONGO_COLLECTION = 'pod-usage'
# MongoDB connection string
MONGO_CONNECTION_STRING = 'mongodb+srv://paulartin:12345679@cluster0.hjzgptm.mongodb.net/CloudSaver'

# MongoDB client and collection initialization
mongo_client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = mongo_client.get_database()  # Specify your database name
collection = db.get_collection("pod-usage")  # Specify your collection name

# MongoDB client and collection initialization
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

resource_name = os.environ.get('RESOURCE_NAME')

# Load Kubernetes configuration
config.load_incluster_config()
# Create Kubernetes client
api_instance = client.CoreV1Api()
cust = client.CustomObjectsApi()

def print_all_namespaces(api_instance, scheduler):
    scheduler.enter(60, 1, print_all_namespaces, (api_instance, scheduler))
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
    #print(nodes_metrics_list)
    for pod_metrics in pod_metrics_list['items']:
        pod_name = pod_metrics['metadata']['name']
        namespace = pod_metrics['metadata']['namespace']
        pod_info = api_instance.read_namespaced_pod(pod_name, namespace)
        node_name = pod_info.spec.node_name
        #print(pod_info)

        # Checking for existing data
        existing_data = collection.find_one({"pod_name": pod_name, "namespace": namespace})

        for container in pod_metrics['containers']:
            container_name = container['name']
            cpu_usage = container['usage']['cpu']
            memory_usage = container['usage']['memory']
            timestamp = time.time()

            # Retrieving node specifications
            node_info = api_instance.read_node(node_name)
            #print("\n")
            #print(node_info)
            print("PAUL")
            cpu_usage_str = cpu_usage.rstrip("n")  # Remove trailing "n"
            try:
                cpu_usage_int = int(cpu_usage_str)  # Convert to integer using try-except for error handling
            except ValueError:
                # Handle potential errors (e.g., invalid format)
                print(f"Error: Could not convert CPU usage '{cpu_usage_str}' to integer")
                cpu_usage_int = 0  # Assign a default value or handle the error differently

            available_cpu_cores = node_info.status.allocatable['cpu']
            print(available_cpu_cores)
            # Calculating CPU percentage
            available_cpu_nanocores = int(available_cpu_cores) * 1_000_000_000

            # Calculating CPU percentage (using nanocores)
            cpu_percentage = (cpu_usage_int / available_cpu_nanocores) * 100
            pod_labels = pod_info.metadata.labels if pod_info.metadata.labels else {}

            #print(cpu_percentage)
            data = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "timestamp": timestamp,
                "cpu_percentage": cpu_percentage,
                "energy_consumption": "10"
            }

            print("Namespace:", namespace)
            print("Pod:", pod_name)
            print("Usage:", data)

            if not existing_data:
                # Create new document with additional data
                collection.insert_one({"resource_name": resource_name, "pod_name": pod_name, "namespace": namespace, "custom_name": pod_name, "usage": [data], "labels": pod_labels})
            else:
                collection.update_one({"pod_name": pod_name, "namespace": namespace}, {"$push": {"usage": data}})


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, print_all_namespaces, (api_instance, my_scheduler))
my_scheduler.run()
if __name__ == "__main__":
    print("start")
