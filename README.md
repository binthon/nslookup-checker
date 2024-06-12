docker run -it --network host -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app -e DISPLAY=host.docker.internal:0.0 nslookup
setx DISPLAY 127.0.0.1:0.0
sudo apt-get install x11-xserver-utils
docker run -it --network host -e DISPLAY=host.docker.internal:0.0 -v C:\Users\Jakub\Desktop\nslookup\nslookup-checker:/app nslookup
