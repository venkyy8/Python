#pyyaml is mainly used to read and write YAML files in Python.
#we can use it to parse Kubernetes YAML files, modify them, and write them back.
#multiple documents in a single YAML file using yaml.safe_load_all and yaml.dump_all.
#pyyaml is a powerful library for handling YAML files in Python, making it easy to work with configurations like those used in Kubernetes.


# By using this script, you can easily modify the number of replicas in a Kubernetes Deployment YAML file.
# It reads the YAML file, updates the replicas count, and saves the changes.
# Make sure to have PyYAML installed: pip install pyyaml
# Usage: python update_replicas.py
# Updates the replicas to new_replicas from existing number (5 in example)
# Saves the modified YAML back (overwrites original by default)
# Prints status messages for clarity



import yaml

def update_replicas(file_path, new_replicas, output_path=None):
    try:
        with open(file_path, 'r') as f:
            docs = list(yaml.safe_load_all(f))

        updated_docs = []
        for doc in docs:
            if doc.get('kind') == 'Deployment':
                print(f"Original replicas: {doc['spec'].get('replicas', 1)}")
                doc['spec']['replicas'] = new_replicas
                print(f"Updated replicas to: {new_replicas}")
            updated_docs.append(doc)

        # Write back to file or new file
        save_path = output_path if output_path else file_path
        with open(save_path, 'w') as f:
            yaml.dump_all(updated_docs, f, default_flow_style=False)

        print(f"✅ YAML saved to {save_path}")

    except Exception as e:
        print(f"❌ Error updating replicas: {e}")

if __name__ == "__main__":
    file_path = "/opt/deployment.yml"
    new_replicas = 5  # Change this number as you like
    update_replicas(file_path, new_replicas)
