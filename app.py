from kubernetes import client, config
import json
from datetime import datetime
import pymongo
from apscheduler.schedulers.background import BackgroundScheduler

# Ersätt med din MongoDB-anslutningsinformation

MONGO_HOST = 'cluster0.hjzgptm.mongodb.net'
MONGO_PORT = 27017
MONGO_DB = 'CloudSaver'
MONGO_COLLECTION = 'pod-usage'
# MongoDB connection string
MONGO_CONNECTION_STRING = 'mongodb+srv://paulartin:12345679@cluster0.hjzgptm.mongodb.net/CloudSaver'

# MongoDB client and collection initialization
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client.get_database()  # Specify your database name
collection = db.get_collection("pod-usage")  # Specify your collection name

# MongoDB client and collection initialization
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
# Load Kubernetes configuration
config.load_incluster_config()
# Create Kubernetes client
api_instance = client.CoreV1Api()
cust = client.CustomObjectsApi()

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
            timestamp = datetime.utcnow()
            data = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "timestamp": timestamp
            }

            if not existing_data:
                # Skapa ny lista med första datapunkten
                collection.insert_one({"pod_name": pod_name, "namespace": namespace, "usage": [data]})
            else:
                # Uppdatera listan med nya datapunkter
                collection.update_one({"pod_name": pod_name, "namespace": namespace}, {"$push": {"usage": data}})

if __name__ == "__main__":
    try:
        # Initial data collection (optional)
        #print_all_namespaces(api_instance)

        # Start schemaläggare
        scheduler = BackgroundScheduler()
        scheduler.add_job(print_all_namespaces, 'interval', seconds=60)
        scheduler.start()

        # Huvudprogrammet kan köras här, eller så kan det avslutas
        # beroende på din arkitektur.
    except Exception as e:
        print(f"An error occurred: {str(e)}")
