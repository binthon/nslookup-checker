import json
import subprocess
import datetime
import os
import platform

def load_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def run_tracert(domain, results_file):
    timeout_count = 0
    max_consecutive_timeouts = 3
    system_name = platform.system().lower()

    if system_name == 'windows':
        command = ["tracert", domain]
    else:
        command = ["traceroute", domain]

    with open(results_file, "a") as file:
        file.write(f"Tracert for {domain} on date {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=False)

        for line in iter(process.stdout.readline, ''):
            file.write(line)
            if "Request timed out" in line or "* * *" in line:
                timeout_count += 1
                if timeout_count >= max_consecutive_timeouts:
                    file.write("More than 3 'Request timed out' lines, moving to next domain.\n")
                    file.write("Trace complete.\n")
                    break
            else:
                timeout_count = 0

def tracert_domains():
    json_file = "domains.json"
    results_file = "tracert_result.txt"
    data = load_from_json(json_file)

    last_url_info = data.get('last_url', {"domain": None, "occurrence": None})
    last_domain = last_url_info.get("domain")
    last_occurrence = last_url_info.get("occurrence")
    order = data.get('order', [])
    start_processing = False

    if not os.path.exists(results_file) or os.path.getsize(results_file) == 0:
        start_processing = True

    domain_counter = {}

    for domain in order:
        domain_counter[domain] = domain_counter.get(domain, 0) + 1

        if not start_processing:
            if domain == last_domain and domain_counter[domain] == last_occurrence:
                start_processing = True
                continue

        if start_processing:
            run_tracert(domain, results_file)
            data['last_url'] = {"domain": domain, "occurrence": domain_counter[domain]}
            save_to_json(json_file, data)

if __name__ == "__main__":
    tracert_domains()
    subprocess.run(["python", "comparator.py"])
