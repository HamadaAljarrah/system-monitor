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
    scheduler.enter(60, 1, print_all_namespaces, (api_instance, scheduler,))
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
        namespace = pod_metrics['metadata']['namespace']
        # Kontrollera om dokumentet redan finns
        existing_data = collection.find_one({"pod_name": pod_name, "namespace": namespace})

        for container in pod_metrics['containers']:
            container_name = container['name']
            cpu_usage = container['usage']['cpu']
            memory_usage = container['usage']['memory']
            timestamp = time.time()
            data = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "timestamp": timestamp
            }
            print("Namespace:", namespace)
            print("Pod:", pod_name)
            print("Usage:", data) 
            if not existing_data:
                # Skapa ny post med pod_name som initialvärde för custom_name
                collection.insert_one({"resource_name": resource_name, "pod_name": pod_name, "namespace": namespace, "custom_name": pod_name, "usage": [data]})
            else:
                # Kontrollera om custom_name redan är satt
                custom_name = existing_data.get("custom_name", None)
                resource_name_col = existing_data.get("resource_name", None)
                if not custom_name:
                    # Använd pod_name om custom_name inte är satt
                    collection.update_one({"pod_name": pod_name}, {"$set": {"custom_name": pod_name}})
                if not resource_name_col:
                    # Använd pod_name om custom_name inte är satt
                    collection.update_one({"pod_name": pod_name}, {"$set": {"resource_name": resource_name}})
                # Uppdatera befintlig post, lämna custom_name oförändrat
                collection.update_one({"pod_name": pod_name}, {"namespace": namespace}, {"$push": {"usage": data}})

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, print_all_namespaces, (api_instance, my_scheduler,))
my_scheduler.run()
if __name__ == "__main__":
    print("start")
