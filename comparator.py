from flask import Flask, render_template
import json
import os
import re

app = Flask(__name__)

def extract_ips_from_tracert(tracert_text):
    pattern = r'(\b[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})\b) \[(\d{1,3}(?:\.\d{1,3}){3})\]|\b(\d{1,3}(?:\.\d{1,3}){3})\b'
    matches = re.findall(pattern, tracert_text)
    results = []
    for match in matches:
        domain, ip, ip_without_domain = match
        if domain:
            entry = f"{ip} [{domain}]"
        else:
            entry = ip_without_domain
        results.append(entry)
    return results

def add_ip_to_domains(tracert_results):
    ips_by_domain = {}
    for domain, tracert_texts in tracert_results.items():
        ordered_ips = []
        for tracert_text in tracert_texts:
            ips = extract_ips_from_tracert(tracert_text)
            for ip in ips[6:]:  
                if ip not in ordered_ips:
                    ordered_ips.append(ip)
        ips_by_domain[domain] = ordered_ips
    return ips_by_domain

def load_tracert_results(filename):
    with open(filename, 'r') as file:
        content = file.read()

    tracert_results = {}
    tracert_block = []
    recording = False
    current_domain = ''

    for line in content.split('\n'):
        if line.startswith('Tracert for '):
            current_domain = line.split(' ')[2]
            if current_domain not in tracert_results:
                tracert_results[current_domain] = []
            recording = True
            tracert_block = [line]
        elif line.startswith('Trace complete.') and recording:
            tracert_block.append(line)
            tracert_results[current_domain].append('\n'.join(tracert_block))
            recording = False
        elif recording:
            tracert_block.append(line)

    return tracert_results

@app.route('/')
def show_domains():
    with open('domains.json', 'r') as file:
        data = json.load(file)

    unique_domains = set(data['domains'])

    tracert_file = 'tracert_result.txt'
    if os.path.exists(tracert_file):
        tracert_results = load_tracert_results(tracert_file)
        ips_by_domain = add_ip_to_domains(tracert_results)
        data['IP'] = ips_by_domain
        with open('domains.json', 'w') as file:
            json.dump(data, file, indent=4)
    else:
        tracert_results = {domain: "Brak wyników trasowania dla tej domeny." for domain in unique_domains}

    return render_template('index.html', domains=unique_domains, tracert_results=tracert_results, data=data)

if __name__ == '__main__':
    app.run(debug=True)
    