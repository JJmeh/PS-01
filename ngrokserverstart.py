import subprocess
from firebase import firebase

firebase = firebase.FirebaseApplication('https://nyxserver-bb04f.firebaseio.com')

name = 'GNsMoN2koZWZKG7r2vJD'

webhook = 'https://nyxserverbot.herokuapp.com'
datawebhook = webhook + '/data'
pwd = '1910'


def sendData(data, webhook=datawebhook):
    subprocess.call("curl -X POST -H 'Content-type: application/text' --data '\"{}\"' {}".format(data, webhook), shell=True)

def startNgrok(port, region, port_num, name):
    print('\nStarting Ngrok....')
    url = subprocess.getoutput('./ngrokstart.sh {} {} {} {}'.format(port, region, port_num, name)).split('/')[-1]
    print('\nStart finish, url : ')
    print(url)
    return url

def tcpSend(url):
    print("\nSending tcp url to firebase database")
    result = firebase.put('/url', name, {"url": "{}".format(url)})
    return 'send done.. {}'.format(result)

def sshSend(url):
    print('\nSending Url..')
    a = 'ap'
    c = url.split('.')[2]
    if c == 'jp':
        b = 'TCP'
    elif c == 'ap':
        b = 'SSH'
        print(c)
    else:
        return 'Error'
    sendData('The {} url is : {}'.format(b, url))

def ngStart(port, region, port_num, name): #kill ngrok process, start ngrok, send ngrok link | every 8 hour
    print('\nSending Ngrok link and starting it..')
    if name == 'tcp':
        print('sending with tcpSend method')
        tcpSend(startNgrok(port, region, port_num, name))
    elif name == 'ssh':
        print('sending with sshSend method')
        sshSend(startNgrok(port, region, port_num, name))
    else:
        return 'it fucking broke again...'
    print('\nDone..')

ngStart(22, 'ap', 4040, 'ssh')
ngStart(5000, 'jp', 4041, 'tcp')