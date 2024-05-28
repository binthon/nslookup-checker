docker run -it -v path\to\project:/app -p 5000:5000 -e DISPLAY=host.docker.internal:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix nslookup_app
setx DISPLAY 127.0.0.1:0.0
sudo apt-get install x11-xserver-utils
