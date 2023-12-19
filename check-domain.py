from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import re
import subprocess
import platform
import os
import threading
import queue

driver = webdriver.Firefox()
driver.get("https://www.amazon.com")

visited_base_urls = set()
urls_queue = queue.Queue()

def extract_base_url(url):
    cleaned_url = re.sub(r'https?://', '', url)
    match = re.match(r'([^/]+)', cleaned_url)
    return match.group(1) if match else None

def checkSystem(url):
    system_name = platform.system().lower()
    if system_name == "windows":
        script_path = "urlInfo.bat"
    else:
        script_path = "urlInfo.sh"
        os.chmod(script_path, 0o755)
    subprocess.run([script_path, url], check=True)

def process_urls():
    while True:
        url = urls_queue.get()
        if url is None:
            break
        checkSystem(url)
        urls_queue.task_done()

# Start processing thread
threading.Thread(target=process_urls, daemon=True).start()

try:
    while True:
        current_url = driver.current_url
        current_base_url = extract_base_url(current_url)

        if current_base_url and current_base_url not in visited_base_urls:
            visited_base_urls.add(current_base_url)
            urls_queue.put(current_base_url)

        time.sleep(2)
except WebDriverException:
    driver.quit()
finally:
    urls_queue.put(None)  # Signal the processing thread to exit.