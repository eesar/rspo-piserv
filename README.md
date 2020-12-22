# rspo-piserv
Raspberry-Pi 433 MHz Remote Switched Power Outlet Local Web Frontend


## Introduction

This Web Frontend for RSPO is developed and tested on a Raspberry-Pi 3B.
The complete web frontend is using python3 with flask and bootstrap.
And inspired by the article [Raspberry Pi mit Python, Flask und Bootstrap kontrollieren](https://www.linux-magazin.de/ausgaben/2015/01/flask/) from the german *Linux Magazin*.
The basic setup for testing flask and bootstrap should also work for any Linux system.
The initial code was developed on a WSL2 before transmitting and fine tuning on raspbian.


## How To, as Short as Possible


## Bill of Material

* [Raspberry Pi 3B](https://www.amazon.de/UCreate-Raspberry-Pi-Desktop-Starter/dp/B07BNPZVR7)
* [rspo-send](https://github.com/eesar/rspo-send) installation with predefined commands
* [rspo-piserv](https://github.com/eesar/rspo-serv)


### Prep the Pi

```bash
# update raspbian
$ sudo apt-get update
$ sudo apt-get upgrade

# install everything for the web frontend
$ sudo apt-get install python3-flask
$ sudo apt-get install python3-pip
$ pip3 install flask-bootstrap

# finally checkout the rspo-piserv github repository
$ cd
$ git clone https://github.com/eesar/rspo-piserv.git
```


### Modify the Setup

Open the python script ```rspo-piserve.py``` and modify the ```g_rspo_switches```
dictionary to fit your rspo-send defined commands.

As well as the ```turnon```, ```turnoff``` and ```__main__``` function,
***if*** your ```rspo-send``` does not follow the example from
[rspo-send](https://github.com/eesar/rspo-send).


### Run the Webserver

### For Testing

```bash
$ python3 rspo-piserv/rspo-piserv.py
```

### As a Service on Raspbian

There is a helpful disrciption for this from [emxsys](https://gist.github.com/emxsys) on this
[gist](https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f) post.
And some more about service can be found on raspbian
[systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md) documentation.

```bash
$ cd /lib/systemd/system/
$ sudo ln -s /home/pi/rspo-piserv/rspo-piserv.service
$ sudo systemctl start rspo-piserv.service
$ sudo systemctl check rspo-piserv.service
```

To start the service on boot up
```bash
$ sudo systemctl enable rspo-piserv.service
```

For some more info if the status is ```failed```.
```bash
$ sudo journalctl -f -u rspo-piserv.service
$ sudo journalctl -xfe -u rspo-piserv.service
```


### Open the Web Frontend

If e.g. running in WSL2 [localhost:8080](//localhost:8080)

When running on raspberry [raspberrypi:8080](//raspberrypi:8080)
