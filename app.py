from flask import Flask, request, abort

import json

import subprocess

app = Flask(__name__)

# server password SECRET
pwd = '1910'

@app.route("/data", methods=['POST'])
def data():
    data = json.loads(request.data, strict=False)
    print("data received '{}'".format(str(data)))
    if data == 'Status':
        # sent data with curl to heroku app
        cpuPercentage = subprocess.getoutput("mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12\"%\" }'")
        cpuTemp = subprocess.getoutput('echo {} | sudo -S {}'.format(pwd, 'tlp-stat -t | grep temp | awk \'{print $4}\''))
        gpuTemp = subprocess.getoutput('nvidia-smi | grep N/A | awk \'$3 ~ /[1-9.]+/ {print $3}\'')
        storagePercent = subprocess.getoutput('df --output=pcent / | awk -F "%" "NR==2{print $1}"')
        print('\nCPU percentage : {}\nCPU temperature : {} C\nGPU Temperature : {}\nStorage Percentage : used{}\n'.format(cpuPercentage, cpuTemp, gpuTemp, storagePercent))
        
    return data

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  
