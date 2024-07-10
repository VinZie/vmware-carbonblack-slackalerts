# Carbon Black Cloud to Slack Alerting

This project is a Python script that monitors alerts from Carbon Black Cloud (CBC) and sends notifications to a specified Slack channel.

## Features
- Sends a notification to Slack when the script starts, indicating that alerting has been enabled.
- Periodically checks for new alerts from CBC.
- Sends alert details to a specified Slack channel.

## Prerequisites
- Python 3.x
- Slack Webhook URL
- Carbon Black Cloud API ID and Secret
- `screen` utility for running the script in the background (optional)

## Installation

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install required Python packages**
    ```bash
    pip install requests
    ```

## Configuration

1. **Carbon Black Cloud API Configuration**
    - Obtain your Carbon Black Cloud API ID and API Secret.
    - Replace the placeholders in the script with your actual API credentials:
        ```python
        CBC_API_ID = "YOUR_API_ID"  # Replace with your API ID
        CBC_API_SECRET = "YOUR_API_SECRET"  # Replace with your API secret
        CBC_API_KEY = f"{CBC_API_SECRET}/{CBC_API_ID}"  # Construct the API key
        ```

2. **Slack Webhook Configuration**
    - Obtain your Slack Webhook URL.
    - Replace the placeholder in the script with your actual Webhook URL:
        ```python
        SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL"  # Replace with your Slack Webhook URL
        ```

3. **Optional Request Body Configuration**
    - Customize the request body to filter alerts based on your criteria:
        ```python
        REQUEST_BODY = {
            "criteria": {
                "minimum_severity": 1,  # Example minimum severity level
                "category": ["THREAT"],
                "last_update_time": {
                    "range": "-1d"  # Last 1 day
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
        ```

## Usage

1. **Running the Script**
    - To start the script and begin monitoring alerts, simply run:
        ```bash
        python cbc_to_slack.py
        ```

2. **Running the Script in the Background Using `screen`**
    - Install `screen` (if not already installed):
        ```bash
        sudo apt-get update
        sudo apt-get install screen
        ```
    - Create a new screen session:
        ```bash
        screen -S cbc_alerting
        ```
    - Run your Python script in the screen session:
        ```bash
        python /path/to/your/cbc_to_slack.py
        ```
    - Detach from the screen session (so the script continues to run in the background):
        - Press `Ctrl+A` then `D`
    - Reattach to the screen session (if you need to check on the script):
        ```bash
        screen -r cbc_alerting
        ```
    - Terminate the screen session (when you're done and want to stop the script):
        - Reattach to the screen session using `screen -r cbc_alerting`
        - Press `Ctrl+C` to stop the script
        - Type `exit` to close the screen session

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.
