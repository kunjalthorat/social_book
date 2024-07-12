import json

# Create a dictionary with username and password
payload = {
    "username": "your_username",
    "password": "your_password"
}

# Convert the dictionary to JSON format
json_payload = json.dumps(payload)

# Print the JSON payload
print(json_payload)
