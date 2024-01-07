from flask import Flask, render_template
import json
import os

app = Flask(__name__)

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
    else:
        tracert_results = {domain: "Brak wyników trasowania dla tej domeny." for domain in unique_domains}

    return render_template('index.html', domains=unique_domains, tracert_results=tracert_results)


if __name__ == '__main__':
    app.run(debug=True)