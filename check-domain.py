from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import re
import subprocess
import platform
import os


def extract_base_url(url):
    cleaned_url = re.sub(r'https?://', '', url)
    match = re.match(r'([^/]+)', cleaned_url)
    return match.group(1) if match else None

system_name = platform.system().lower()
if system_name == "windows":
    driver = webdriver.Firefox()
    driver.get("https://google.com")
    output_file = "domains.txt"
elif system_name in ["linux", "darwin"]:
    opts = Options()
    opts.binary_location = '/usr/local/bin/firefox'
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=opts)
    driver.get("https://google.com")
    output_file = "domains.txt"
   
if not os.path.exists(output_file):
    with open(output_file, "w") as file:
        pass
os.chmod(output_file, 0o744)

visited_base_urls = set()
 

try:
    with open(output_file, "w") as file: 
        while True:
            current_url = driver.current_url
            current_base_url = extract_base_url(current_url)

            if current_base_url and current_base_url not in visited_base_urls:
                visited_base_urls.add(current_base_url)
                file.write(current_base_url + "\n")

            time.sleep(2)
except WebDriverException:
    pass
finally:
    driver.quit()
    if system_name == "windows":
        subprocess.run("urlInfo-test.bat", check=False)
    elif system_name in ["linux", "darwin"]:
        subprocess.run("./urlInfo.sh", shell=True, check=True)
