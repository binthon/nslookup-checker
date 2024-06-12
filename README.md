<h1>Purposes of the Application</h1>
Apliaction is designed to collect the internet domain that a user walks through and then collects information about that domain. The traceroute and nslookup commands are executed, and the data from these commands is visualised in the web application.


1. docker run -it --network host -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app -e DISPLAY=host.docker.internal:0.0 nslookup
setx DISPLAY 127.0.0.1:0.0
sudo apt-get install x11-xserver-utils
2. docker run -it --network host -e DISPLAY=host.docker.internal:0.0 -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app nslookup
