import json
import platform
import os
import re
import subprocess
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def extract_base_url(url):
    cleaned_url = re.sub(r'https?://', '', url)
    match = re.match(r'([^/]+)', cleaned_url)
    return match.group(1) if match else None

def setup_driver():
    system_name = platform.system().lower()
    if system_name == "windows":
        driver = webdriver.Firefox()
    elif system_name in ["linux", "darwin"]:
        opts = Options()
        opts.binary_location = '/usr/local/bin/firefox'
        service = Service(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=opts)
    else:
        raise Exception("Unsupported operating system.")
    
    driver.get("https://www.google.com") 
    return driver


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def create_empty_json_if_not_exists(filename):
    if not os.path.exists(filename):
        data = {
            "last_url": "",
            "domains": []
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        os.chmod(filename, 0o744)

def load_from_json(filename):
    create_empty_json_if_not_exists(filename)
    with open(filename, 'r') as file:
        return json.load(file)

def checker():
    json_file = "domains.json"
    data = load_from_json(json_file)
    visited_domains = data['domains']

    driver = setup_driver()
    try:
        while True:
            current_url = driver.current_url
            current_base_domain = extract_base_url(current_url)

            if current_base_domain and current_base_domain not in visited_domains and current_base_domain != "about:blank":
                visited_domains.append(current_base_domain)
                data['domains'] = visited_domains
                save_to_json(json_file, data)
    except WebDriverException:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    while True: 
        choice = input("Do you want to directly run app? (YES/NO): ").strip().lower()
        if choice == 'yes':
            if os.path.exists('domains.json'):
                print("Tracert for domain")
                subprocess.run(["python", "comparator.py"])
                break
            else:
                print("First, web scraping will be done.")
                checker()   
                print("Tracert for domain")
                subprocess.run(["python", "comparator.py"])
                break  
        elif choice == 'no':
            print("Database doesn't exist. First, web scraping will be done.")
            checker()
            print("Tracert for domain")
            subprocess.run(["python", "comparator.py"])
            break  
        else:
            print("Type 'yes' or 'no'.")

