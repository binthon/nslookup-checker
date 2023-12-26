from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import re
import subprocess
import platform
import os

def extract_base_url(url):
    cleaned_url = re.sub(r'https?://', '', url)
    match = re.match(r'([^/]+)', cleaned_url)
    return match.group(1) if match else None

driver = webdriver.Firefox()
driver.get("https://google.com")

visited_base_urls = set()
output_file = "domains.txt"

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
    system_name = platform.system().lower()
    if system_name == "windows":
        subprocess.run("urlInfo.bat", check=True)
    elif system_name in ["linux", "darwin"]:
        os.chmod("./urlInfo.sh", 0o755) 
        subprocess.run("./urlInfo.sh", shell=True, check=True)
