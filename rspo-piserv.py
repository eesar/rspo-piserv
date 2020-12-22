# -*- coding: utf-8 -*-
'''Flask file for Raspberry Pi'''

import platform
import datetime
import os
import subprocess
import socket

from flask import render_template, redirect, request
from flask import Flask
from flask_bootstrap import Bootstrap

APP = Flask(__name__)
Bootstrap(APP)


# --------------------------------------------------------------------------------------------------
# adjust to your rspo-send setup
# --------------------------------------------------------------------------------------------------
# rspo switch name and there status after starting the service False == OFF, True == ON
d_rspo_switches = {
    "siebträger"    : False,
    "badradio"      : False,
    "stereo"        : False,
    "subwoofer"     : False
}
# eesar 22.12.2020: python 3.5 of raspbian 8 (strech) does not keep the order of the keys.
#   This is is really annoing, because after each restart of rspo-piserv the order switches could
#   be different. With pyhton 3.6 this is not the case anymore.
l_rspo_switches = [
    "siebträger",
    "badradio",
    "stereo",
    "subwoofer"
]
# --------------------------------------------------------------------------------------------------


@APP.route('/')
@APP.route('/index.html')
def mainhtml():
    global d_rspo_switches
    return render_template('index.html', d_rspo_switches=d_rspo_switches, \
                                         l_rspo_switches=l_rspo_switches )

@APP.route('/stats.html')
def stats():
    user = os.environ['USER']
    space = os.statvfs('/home/'+user)
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    line = subprocess.check_output(['vcgencmd','measure_temp']).rstrip()
    temp = line.decode().split("=")[1]
    line = subprocess.check_output(['vcgencmd','measure_volts']).rstrip()
    volts = line.decode().split("=")[1]
    line = subprocess.check_output(['vcgencmd','measure_clock', 'arm']).rstrip()
    clock = line.decode().split("=")[1]
    line = subprocess.check_output(['grep','PRETTY_NAME', '/etc/os-release']).rstrip()
    osname = line.decode().split('"')[1]
    l_stats = {
        "arch" : platform.machine(),
        "clock" : int(clock)/1000/1000,
        "freespace" : round((space.f_frsize * space.f_bavail)/1024/1024/1024,1),
        "node" : platform.node(),
        "osname" : osname,
        "system" : platform.system(),
        "temp" : temp,
        "today" : datetime.date.today(),
        "uptime" : str(datetime.timedelta(seconds=round(uptime_seconds))),
        "user" : user,
        "volts" : volts
    }

    return render_template('stats.html', stats=l_stats)


@APP.route('/turnon', methods=['POST'])
def turnon():
    global d_rspo_switches
    name = request.form.get('rspo')
    d_rspo_switches[name] = True 
    print("rspo ", name, " on") # used for testing in WSL2
    subprocess.run(["/home/pi/bin/rspo", name , "on"])
    return render_template('index.html', d_rspo_switches=d_rspo_switches, \
                                         l_rspo_switches=l_rspo_switches )


@APP.route('/turnoff', methods=['POST'])
def turnoff():
    global d_rspo_switches
    name = request.form.get('rspo')
    d_rspo_switches[name] = False
    print("rspo ", name, " off") # used for testing in WSL2
    subprocess.run(["/home/pi/bin/rspo", name , "off"])
    return render_template('index.html', d_rspo_switches=d_rspo_switches, \
                                         l_rspo_switches=l_rspo_switches )


if __name__ == "__main__":
    for rspo in d_rspo_switches:
        if d_rspo_switches[rspo]:
            print(rspo, "turn on")
            subprocess.run(["/home/pi/bin/rspo", rspo , "on"])
        else:
            print(rspo, "turn off")
            subprocess.run(["/home/pi/bin/rspo", rspo , "off"])
    APP.run(host='0.0.0.0', port=8080, debug=False)
