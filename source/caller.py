import requests
import os
import json
import threading
import datetime

__name__ = "Caller"
__author__ = "Juanez"
__license__ = "Pimedica"
__credits__ = ["Pimedica", "OCTA", "Juanez"]
__email__ = "juangarcia@pimedica.com"
__version__ = 3.0

URL1 = "http://{IP}:8081/locations/integration/get_last_call"
URL2 =  "http://{IP}:8081/locations/integration/688563877235/get_records/start_date={CURRENT_DATA}&end_date={CURRENT_DATA}&active=true"
URL3 =  "http://{IP}:8081/locations/integration/998106382534/get_records/start_date={CURRENT_DATA}&end_date={CURRENT_DATA}&active=true"




class Caller(object):
    def __init__(self, debug, path):
        self.debug = debug
        self.path = path
        self.data = os.path.join(self.path, "data")
        self.sound = os.path.join(self.data, "sound")
        self.buttons = {}
        self.ips = []
        self.buffer = []
        f = open(os.path.join(self.data, "ips"))
        self.ips = f.readlines()
        f.close()
        f = open(os.path.join(self.data, "buttons"))
        self.buttons = json.load(f)
        f.close()
        self.subprocess = threading.Thread(target=self.checker)
        self.debug.put("CALLER SUCCESSFULLY INITIALITED", "success")
    
    def checker(self):

        def process(w):

            #print(w)
            if w[1].upper() == "CALL" and w[2] in self.buttons and w[3] in self.buttons[str(w[2])] and w[2] not in self.buffer:
                self.buffer.append(w[2])
        
        def convert(person):

            event = person[len(person)-1]         
        
            record=event['Record']
            message = event['Message']
            event_message = message[len(message)-1]        
            requester = record['requester']
            requester_key = record['requester_key']
            type_key = event_message['type'] # send_message=call  cancel_record=cancel
            requester_name = record['requester_name']
            start_time = record['start_time']

            if(type_key == 'cancel_record'):
                type_key ="cancel"
            if(type_key == 'send_message'):
                type_key ="call"

            request = ['button',type_key,requester,requester_key,requester_name,start_time]

            return request

        self.debug.put("VERIFIER SUCCESSFULLY INITIALITED", "success")
        while True:
            print('-----Activating-----')
            for ip in self.ips:
                try:
                    ip = ip.strip("\n")
                    
                    Current_Date = datetime.date.today().strftime('%Y-%m-%d')

                    

                    if len(ip) > 0:
                        
                        if(ip) == "192.168.5.30" :

                            r = requests.get(URL2.format(IP=ip,CURRENT_DATA=Current_Date, timeout=5))
                            w = r.json()
                            w=convert(w)
                            print(ip,w,r.status_code)

                        elif(ip) == "192.168.5.15":

                            r = requests.get(URL3.format(IP=ip,CURRENT_DATA=Current_Date, timeout=5))
                            w = r.json()
                            w=convert(w)
                            print(ip,w,r.status_code)

                        else:
                            r = requests.get(URL1.format(IP=ip), timeout=5)
                            w = r.text.split(";")
                            print(ip,w,r.status_code)                                          
                            #r = "button;call;6c211;2;boton 1;2019-04-08 15:36"
                            #w = r.split(";")

                        process(w)
                        
                except Exception as err:

                    self.debug.put("ERROR GETTING DATA FROM IP {}: {}").format(ip, err)

    def run(self):
        self.subprocess.start()
        while True:
            for buffer in self.buffer:
                f = os.path.join(self.sound, buffer)
                self.debug.put("PLAYING {} AT {}".format(f, self.buttons[buffer]['l']), "normal")
                os.system("vlc {} --play-and-exit".format(f))
                self.buffer.remove(buffer)
