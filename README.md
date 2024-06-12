# Purposes of the Application 
Apliaction is designed to collect the internet domain that a user walks through and then collects information about that domain. The traceroute and nslookup commands are executed, and the data from these commands is visualised in the web application.
# Technologies used
# Backend 
The backend of the application is written using Python along with the Selenium library.  I also created bat and bash scripts to operate on the traceroute/tracert and nslookup commands The domain data is stored in a json file.
# Frontend
To interact with the user, I used the Flask tool, which is responsible for creating the web application and retrieving data from a json file.
# How Use
1. Download code form github
```bash
  git@github.com:binthon/nslookup-checker.git
```
2. Use pip to install dependencies
```bash
  pip install -r requirements.txt
```
3. Launch app
```bash
  python check-domain.py
```
4. Open app in webiste
```bash
  localhost:5000
```

# Docker
My goal is to implement the application in such a way that it can be run as a container
1. Download XLaunch app to can open multiple window and set "Disable access controlę option during installation. 

Link to download XLanuch: https://sourceforge.net/projects/vcxsrv/
2. Download Docker Engine
  Windows: https://docs.docker.com/desktop/install/windows-install/\n
  Linux: https://docs.docker.com/desktop/install/linux-install/\n
3. Create images using Dockerfile
```bash
  docker build -t {yourImageName} .
```
4. Run container
```bash
  docker run -it --network host -e DISPLAY=host.docker.internal:0.0 -v your\path\to\projects:/app nslookup
```
