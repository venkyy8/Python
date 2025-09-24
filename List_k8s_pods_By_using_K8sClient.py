#install kubernetes client library 
# pip install kubernetes


from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Replace with the namespace you want to query
NAMESPACE = 'default'

def list_pods(namespace):
    try:
        # Load kubeconfig (for local development)
        config.load_kube_config()

        # Use CoreV1 API
        v1 = client.CoreV1Api()

        print(f"📦 Listing pods in namespace: {namespace}")
        pods = v1.list_namespaced_pod(namespace)

        if not pods.items:
            print("⚠️ No pods found.")
        else:
            for pod in pods.items:
                print(f"🔹 Pod Name: {pod.metadata.name} | Status: {pod.status.phase}")
    
    except ApiException as e:
        print(f"❌ Kubernetes API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    list_pods(NAMESPACE)
