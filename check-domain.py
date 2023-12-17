from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import re
import subprocess
import platform
import os

driver = webdriver.Firefox()  
driver.get("https://www.google.pl")

visited_base_urls = []  

def extract_base_url(url):
    match = re.match(r'(https?://[^/]+)', url)
    return match.group(1) if match else None

def is_new_base_url(base_url, history):
    return base_url not in history
    
def checkSystem(url):
    
    system_name = platform.system().lower()

    if system_name == "windows":
        script_path = "urlInfo.bat"
        subprocess.run([script_path, url])
    elif system_name == "darwin":
      
        script_path = "urlInfo.sh"
        os.chmod(script_path, 0o755)
        subprocess.run([script_path, url])
    else:
       
        script_path = "urlInfo.sh"
        os.chmod(script_path, 0o755)
        subprocess.run([script_path, url])

try:
    while True:
        current_url = driver.current_url
        current_base_url = extract_base_url(current_url)

        if current_base_url and is_new_base_url(current_base_url, visited_base_urls):
            visited_base_urls.append(current_base_url)
            
            checkSystem(current_base_url)
            
        time.sleep(2)
except WebDriverException:
    driver.quit()
