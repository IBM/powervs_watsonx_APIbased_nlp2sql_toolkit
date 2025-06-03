#!/bin/bash

# Path to config file
CONFIG_FILE="config.ini"

# Function to read value by section and key
function get_config_value() {
    local section=$1
    local key=$2
    grep -A1 "^\[$section\]" "$CONFIG_FILE" | grep "^$key" | sed 's/^[^=]*= *//'
}

# Example usage
API_KEY=$(get_config_value "apikey" "api_key")

# RHEL may handle line endings or file encodings slightly differently (e.g., carriage returns from Windows-style .ini files or dos2unix issues).
# So remove any leading or trailing newline or carriage returns
API_KEY=$(grep 'api_key' config.ini | cut -d'=' -f2- | tr -d '\r\n[:space:]')


#API_KEY=$API_KEY_ENV
curl -X POST 'https://iam.cloud.ibm.com/identity/token' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey='$API_KEY


