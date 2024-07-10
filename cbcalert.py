import requests
import json
import time

# Configuration
CBC_BASE_URL = "https://api.yourcarbonblackcloud.com"
ORG_KEY = "YOUR_ORG_KEY"  # Replace with your organization key
CBC_API_URL = f"{CBC_BASE_URL}/appservices/v6/orgs/{ORG_KEY}/alerts"
CBC_API_ID = "YOUR_API_ID"  # Replace with your API ID
CBC_API_SECRET = "YOUR_API_SECRET"  # Replace with your API secret
CBC_API_KEY = f"{CBC_API_SECRET}/{CBC_API_ID}"  # Construct the API key
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
SLACK_STARTUP_MESSAGE = "CBC to Slack alerting has been enabled. This channel is now receiving alerts from Kelvin-UbuntuVM."

# Request body (e.g., for filtering alerts)
REQUEST_BODY = {
    "criteria": {
        "minimum_severity": 1,  # Example minimum severity level
        "category": ["THREAT"],
        "last_update_time": {
            "range": "-2m"  # Last 2 minutes
        }
    },
    "rows": 10,  # Number of alerts to fetch
    "sort": [
        {
            "field": "last_update_time",
            "order": "desc"
        }
    ]
}

# Function to send a startup notification to Slack
def send_startup_message():
    message = {
        "text": SLACK_STARTUP_MESSAGE
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Error sending startup message to Slack: {response.status_code} - {response.text}")

# Function to get alerts from Carbon Black Cloud
def get_cbc_alerts():
    headers = {
        'X-Auth-Token': CBC_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(CBC_API_URL, headers=headers, json=REQUEST_BODY)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Error fetching alerts: {response.status_code} - {response.text}")
        return []

# Function to send a Slack message
def send_slack_message(alert):
    severity_colors = {
        1: "#808080",  # Gray for low severity
        2: "#FFA500",  # Orange for medium severity
        3: "#FF4500",  # Red-Orange for high severity
        4: "#FF0000",  # Red for critical severity
        5: "#8B0000"   # Dark Red for highest severity
    }
    color = severity_colors.get(alert.get('severity'), "#808080")  # Default to gray if severity not found
    message = {
        "attachments": [
            {
                "color": color,
                "title": f"Alert ID: {alert.get('id')}",
                "fields": [
                    {
                        "title": "Description",
                        "value": alert.get('description', 'No description available'),
                        "short": False
                    },
                    {
                        "title": "Severity",
                        "value": alert.get('severity', 'N/A'),
                        "short": True
                    },
                    {
                        "title": "Category",
                        "value": ', '.join(alert.get('category', ['N/A'])),
                        "short": True
                    },
                    {
                        "title": "Created At",
                        "value": alert.get('create_time', 'N/A'),
                        "short": True
                    },
                    {
                        "title": "Last Updated",
                        "value": alert.get('last_update_time', 'N/A'),
                        "short": True
                    },
                    {
                        "title": "Device Name",
                        "value": alert.get('device_name', 'N/A'),
                        "short": True
                    },
                    {
                        "title": "Blocked Application",
                        "value": alert.get('threat_cause_process_name', 'N/A'),
                        "short": True
                    },
                    {
                        "title": "Status",
                        "value": alert.get('state', 'N/A'),
                        "short": True
                    }
                ]
            }
        ]
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Error sending to Slack: {response.status_code} - {response.text}")

# Main function to process alerts and update their status
def main():
    send_startup_message()  # Send the startup message
    processed_alerts = {}
    while True:
        print("Checking for new alerts...")  # Print message to console
        alerts = get_cbc_alerts()
        for alert in alerts:
            alert_id = alert.get('id')
            if alert_id not in processed_alerts or processed_alerts[alert_id] != alert.get('state'):
                send_slack_message(alert)
                processed_alerts[alert_id] = alert.get('state')
        time.sleep(60)  # Check for new alerts every 60 seconds

if __name__ == "__main__":
    main()
