from flask import Flask, request, abort, jsonify

import json

import sys

import subprocess

sys.path.insert(1, '../PP-01')

from bill import *

app = Flask(__name__)

def getStatus():
    subprocess.call('echo {} | sudo -S {}'.format(pwd, 'echo root'), shell=True)
    cpuPercentage = subprocess.getoutput("mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12\"%\" }'")
    cpuTemp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -t | grep temp | awk \'{print $4}\''))
    gpuTemp = subprocess.getoutput('nvidia-smi | grep N/A | awk \'$3 ~ /[1-9.]+/ {print $3}\'')
    storagePercent = subprocess.getoutput('df --output=pcent / | awk -F "%" "NR==2{print $1}"')
    batteryStatus = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -b | grep status | awk \'{print $3 $4}\''))
    return cpuPercentage, cpuTemp, gpuTemp, storagePercent, batteryStatus

def formatStatus(status):
    fstatus = {
            'cpu': '{}'.format(status[0].split('%')[0]),
            'cpuTemp': '{}'.format(status[1]),
            'gpuTemp': '{}'.format(status[2]),
            'storage': '{}'.format(status[3].split('%')[0]),
            'batStatus': '{}'.format(status[4])
        }
    
    return fstatus
    


# server password SECRET
pwd = '1910'

webhook = 'https://nyxserverbot.herokuapp.com'
datawebhook = webhook + '/data'

def sendData(data, webhook=datawebhook):
    subprocess.call("curl -X POST -H 'Content-type: application/text' --data '\"{}\"' {}".format(data, webhook), shell=True)

@app.route("/data", methods=['POST'])
def data():
    data = json.loads(request.data, strict=False)
    print("data received '{}'".format(str(data)))
    if data == 'Status':
        subprocess.call('echo {} | sudo -S {}'.format(pwd, 'echo root'), shell=True)
        # sent data with curl to heroku app
        cpuPercentage = subprocess.getoutput("mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12\"%\" }'")
        cpuTemp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -t | grep temp | awk \'{print $4}\''))
        gpuTemp = subprocess.getoutput('nvidia-smi | grep N/A | awk \'$3 ~ /[1-9.]+/ {print $3}\'')
        storagePercent = subprocess.getoutput('df --output=pcent / | awk -F "%" "NR==2{print $1}"')
        batteryStatus = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -b | grep status | awk \'{print $3}\''))
        status = 'CPU percentage : {}\nCPU temperature : {} C\nGPU Temperature : {}\nStorage Percentage : used{}\nBattery Status : {}\n'.format(cpuPercentage, cpuTemp, gpuTemp, storagePercent, batteryStatus)
        sendData(status)

    elif data == 'reboot':
        print(data)
        subprocess.call('reboot', shell=True)

    elif data == 'tunnelrestart':
        print(data)
        subprocess.call('python3 ngrokserverstart.py', shell=True)

    elif data == 'killSSH':
        print(data)
        subprocess.call("pkill -f 'ssh'", shell=True)
    
    elif data == 'killTCP':
        print(data)
        subprocess.call("pkill -f 'tcp'", shell=True)

    elif data == 'killall':
        subprocess.call("killall ngrok", shell=True)
        print(data)
    
    elif data == 'shutdown':
        subprocess.call('echo {} | sudo -S {}'.format(pwd, 'shutdown -h now'), shell=True)

    return data

@app.route("/status", methods=['GET'])
def status():
    return jsonify(formatStatus(getStatus()))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  
