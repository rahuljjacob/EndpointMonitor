import requests
import time

BASE_URL = "http://localhost:8000"

# List of GET endpoints
GET_ENDPOINTS = [
    "/ping",
    "/status",
    "/version",
    "/error",
    "/users/1",      # valid
    "/users/0",      # should trigger error
    "/users/-5",     # should trigger error
]

# POST endpoints with payloads
POST_ENDPOINTS = [
    {
        "endpoint": "/submit",
        "payloads": [
            {"content": "Short title"},         # Error (title too short)
            {"title": "Valid Title", "content": "Looks good"}  # Valid
        ]
    }
]

DELAY = 2  # seconds between each full round of requests


def call_endpoints_forever():
    while True:
        # Hit all GET endpoints
        for endpoint in GET_ENDPOINTS:
            url = f"{BASE_URL}{endpoint}"
            try:
                response = requests.get(url)
                print(f"[{response.status_code}] GET {endpoint}")
                print(response.text)
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Failed to GET {endpoint}: {e}")
            print("-" * 50)

        # Hit all POST endpoints with both good and bad payloads
        for item in POST_ENDPOINTS:
            for payload in item["payloads"]:
                url = f"{BASE_URL}{item['endpoint']}"
                try:
                    response = requests.post(url, json=payload)
                    print(f"[{response.status_code}] POST {item['endpoint']} with payload: {payload}")
                    print(response.text)
                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] Failed to POST {item['endpoint']}: {e}")
                print("-" * 50)

        time.sleep(DELAY)


if __name__ == "__main__":
    try:
        call_endpoints_forever()
    except KeyboardInterrupt:
        print("\nStopped by user.")