# Function to validate IP address
function is_valid_ip() {
    local ip=$1
    local IFS=.
    local -a octets=($ip)

    if [ ${#octets[@]} -ne 4 ]; then
        return 1
    fi

    for octet in "${octets[@]}"; do
        if ! [[ $octet =~ ^[0-9]+$ ]]; then
            return 1
        fi
        if [ $octet -lt 0 ] || [ $octet -gt 255 ]; then
            return 1
        fi
    done

    return 0
}

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Please provide an IP address or domain name."
    exit 1
fi

INPUT=$1
echo "Input parameter: $INPUT"

# Validate if the input is an IP address
if is_valid_ip "$INPUT"; then
    echo "Looking up details for IP address $INPUT"
    nslookup -debug $INPUT
else
    # Lookup DNS records for the domain name
    for TYPE in A AAAA MX TXT NS CNAME; do
        echo "Looking up $TYPE records for $INPUT"
        nslookup -type=$TYPE $INPUT
        echo
    done
fi