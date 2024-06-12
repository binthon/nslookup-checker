# Purposes of the Application 
Apliaction is designed to collect the internet domain that a user walks through and then collects information about that domain. The traceroute and nslookup commands are executed, and the data from these commands is visualised in the web application.

# Technologies used

## Backend 
The backend of the application is written using Python along with the Selenium library.  I also created bat and bash scripts to operate on the traceroute/tracert and nslookup commands. The domain data is stored in a json file.

## Frontend
To interact with the user, I used the Flask tool, which is responsible for creating the web application and retrieving data from a json file.

# How to Use
1. Download the code from GitHub
    ```bash
    git@github.com:binthon/nslookup-checker.git
    ```
2. Use pip to install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Launch the app
    ```bash
    python check-domain.py
    ```
4. Open the app in a browser
    ```bash
    localhost:5000
    ```

# Docker
My goal is to implement the application in such a way that it can be run as a container. This implementation is not ready yet.

1. Download XLaunch app to open multiple windows and set "Disable access control" option during installation.

   [Link to download XLaunch](https://sourceforge.net/projects/vcxsrv/)

   XLanuch is needed to open the browser from a container on the host.

3. Download Docker Engine:

   [Windows](https://docs.docker.com/desktop/install/windows-install/) | [Linux](https://docs.docker.com/desktop/install/linux-install/)

4. Create an image using Dockerfile
    ```bash
    docker build -t {yourImageName} .
    ```
5. Run the container
    ```bash
    docker run -it -p 5000:5000 -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app {yourImageName}
    ```

GUI examples

