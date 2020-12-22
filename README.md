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


### Open the Web Frontend

If e.g. running in WSL2 [localhost:8080](//localhost:8080)

When running on raspberry [raspberrypi:8080](//raspberrypi:8080)
