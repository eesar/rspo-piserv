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
g_rspo_switches = {
    "siebträger"    : False,
    "badradio"      : False,
    "stereo"        : False,
    "subwoofer"     : False
}
# --------------------------------------------------------------------------------------------------


@APP.route('/')
@APP.route('/index.html')
def mainhtml():
    global g_rspo_switches
    return render_template('index.html', rspo_switches=g_rspo_switches)

@APP.route('/stats.html')
def stats():
    today = datetime.date.today()
    system = platform.system()
    node = platform.node()
    arch = platform.machine()
    user = os.environ['USER']
    space = os.statvfs('/home/'+user)
    freespace = round((space.f_frsize * space.f_bavail)/1024/1024/1024,1)
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime = str(datetime.timedelta(seconds=round(uptime_seconds)))

    return render_template('stats.html', today=today, system= \
                            system, node=node, arch=arch, user=user, \
                            freespace=freespace, uptime=uptime)


@APP.route('/turnon', methods=['POST'])
def turnon():
    global g_rspo_switches
    name = request.form.get('rspo')
    g_rspo_switches[name] = True
    print("rspo ", name, " on")
    return render_template('/index.html', rspo_switches=g_rspo_switches)


@APP.route('/turnoff', methods=['POST'])
def turnoff():
    global g_rspo_switches
    name = request.form.get('rspo')
    g_rspo_switches[name] = False
    print("rspo ", name, " off")
    return render_template('/index.html', rspo_switches=g_rspo_switches)


if __name__ == "__main__":
    for rspo in g_rspo_switches:
        if g_rspo_switches[rspo]:
            print(rspo, "turn on")
        else:
            print(rspo, "turn off")
    APP.run(host='0.0.0.0', port=8080, debug=False)
