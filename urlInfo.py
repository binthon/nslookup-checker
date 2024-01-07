import json
import subprocess
import datetime
import os

def load_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def run_tracert(domain, results_file):
    timeout_count = 0
    max_consecutive_timeouts = 3

    with open(results_file, "a") as file:
        file.write(f"Tracert for {domain} on date {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        process = subprocess.Popen(["tracert", domain], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)

        for line in iter(process.stdout.readline, ''):
            file.write(line)
            if "Request timed out" in line:
                timeout_count += 1
                if timeout_count >= max_consecutive_timeouts:
                    file.write("More than 3 'Request timed out' line, does tracert for next domain.\n")
                    break
            else:
                timeout_count = 0

def tracertResult():
    json_file = "domains.json"
    results_file = "tracert_result.txt"
    data = load_from_json(json_file)
    domains = data.get('domains', [])

    file_exists = os.path.exists(results_file)

    if not file_exists or data.get('last_url') not in domains:
        data['last_url'] = domains[0] if domains else None
        save_to_json(json_file, data)

    last_url = data.get('last_url')
    start_processing = False if file_exists else True

    for domain in domains:
        if domain == last_url and file_exists:
            start_processing = True
            continue

        if start_processing:
            run_tracert(domain, results_file)
            data['last_url'] = domain
            save_to_json(json_file, data)

if __name__ == "__main__":
    tracertResult()

