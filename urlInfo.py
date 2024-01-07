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
                    file.write("Trace complete.\n")
                    break
            else:
                timeout_count = 0

def tracertResult(force_tracert=False):
    json_file = "domains.json"
    results_file = "tracert_result.txt"
    data = load_from_json(json_file)
    domains = data.get('domains', [])
    last_url = data.get('last_url')


    if last_url == domains[-1] and not force_tracert and os.path.exists(results_file):
        if os.path.getsize(results_file) != 0:
            return

    file_exists = os.path.exists(results_file)
    file_is_empty = not file_exists or os.path.getsize(results_file) == 0
    start_processing = True if file_is_empty or last_url not in domains else False

    for domain in domains:
        if not start_processing and domain == last_url:
            start_processing = True
            continue

        if start_processing:
            run_tracert(domain, results_file)
            data['last_url'] = domain
            save_to_json(json_file, data)
if __name__ == "__main__":
    tracertResult()
    subprocess.run(["python", "comparator.py"])
