<h1>Purposes of the Application</h1>
Apliaction is designed to collect the internet domain that a user walks through and then collects information about that domain. The traceroute and nslookup commands are executed, and the data from these commands is visualised in the web application.
<h1>Technologies used</h1>
<h4>Backend</h4>
The backend of the application is written using Python along with the Selenium library.  I also created bat and bash scripts to operate on the traceroute/tracert and nslookup commands The domain data is stored in a json file.
<h4>Frontend</h4>
To interact with the user, I used the Flask tool, which is responsible for creating the web application and retrieving data from a json file.
<h1>How Use</h1>
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

<h1> Docker
 docker run -it --network host -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app -e DISPLAY=host.docker.internal:0.0 nslookup
setx DISPLAY 127.0.0.1:0.0
sudo apt-get install x11-xserver-utils
2. docker run -it --network host -e DISPLAY=host.docker.internal:0.0 -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app nslookup
