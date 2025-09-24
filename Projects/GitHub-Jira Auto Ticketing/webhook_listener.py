from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# === Jira Config ===
JIRA_EMAIL = "venkyy82@gmail.com"
JIRA_API_TOKEN = "xxxx"
JIRA_PROJECT_KEY = "SCRUM"
JIRA_BASE_URL = "https://venkyy82.atlassian.net"

# === Webhook Endpoint ===
@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()

    # Check if it's a comment creation event
    if data.get("action") == "created" and "comment" in data:
        comment_body = data["comment"]["body"]
        issue_title = data["issue"]["title"]
        issue_url = data["issue"]["html_url"]

        # ✅ Only match exact "/jira" comment
        if comment_body.strip().lower() == "/jira":
            summary = f"[GitHub Issue] {issue_title}"
            description = f"Imported from GitHub Issue:\n{issue_url}"
            created = create_jira_ticket(summary, description)

            if created:
                return jsonify({"message": "Jira ticket created"}), 201
            else:
                return jsonify({"message": "Failed to create Jira ticket"}), 500

    return jsonify({"message": "No action taken"}), 200


# === Create Jira Ticket ===
def create_jira_ticket(summary, description):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 201:
        print("Jira ticket created:", response.json()["key"])
        return True
    else:
        print("Failed to create Jira ticket:", response.text)
        return False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
