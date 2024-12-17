# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import socket

__name__ = "Updater"
__author__ = "Juanez"
__license__ = "Pimedica S.A."
__credits__ = ["Pimedica S.A.", "OCTA"]
__email__ = "juangarcia@pimedica.net"
__version__ = 1.2

PATH = os.path.dirname(os.path.abspath(__file__))

class Update(object):
    def __init__(self, name, version, debug, destination):
        self.name = name
        self.version = version
        self.debug = debug
        self.destination = destination
        f = open(os.path.join(PATH, "config"))
        self.file = f.readline()
        f.close()
        self.debug.put("UPDATER SUCCESSFULLY INITIALIZED", "success")

    def dependencies(self):
        self.debug.put("LOOKING FOR DEPENDENCIES", "normal")
        file = os.path.join(self.destination, "requirements.txt")
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", file])

    def connection(self):
        self.debug.put("VERIFYING INTERNET CONNECTION", "normal")
        try:
            socket.gethostbyname('google.com')
            c = socket.create_connection(('google.com', 80), 1)
            c.close()
        except socket.gaierror:
            self.debug.put("DNS ERROR", "error")
            return False
        except socket.error:
            self.debug.put("CONNECTION ERROR", "error")
            return False
        return True

    def update(self):
        self.debug.put("LOOKING FOR A NEWER VERSION", "normal")
        file = os.path.join(PATH, "version.txt")
        if self.connection():
            if os.path.exists(file):
                os.remove(file)
            if not self.download(self.file, file):
                return False
            f = open(file)
            l = f.readlines()
            f.close()
            version, file = self.version, None
            for f in l:
                f = f[:-1].split(",")
                if f[0]==self.name:
                    if float(f[1]) > version:
                        version = float(f[1])
                        file = f[2]
            if version > self.version and file is not None:
                self.debug.put("THERE IS A NEW VERSION", "normal")
                self.new = version
                destination = os.path.join(self.destination, "{}_V{}.zip".format(self.name, self.new))
                self.debug.put("INSTALLING VERSION (V_{})".format(self.new), "normal")
                if self.download(file, destination, True):
                    self.debug.put("NEW VERSION SUCCESSFULLY INSTALLED", "success")
                    return True
        return False

    def download(self, file, destination, unzip=False):
        if not os.path.exists(destination):
            try:
                from google_drive_downloader import GoogleDriveDownloader as gd
                gd.download_file_from_google_drive(file_id=file, dest_path=destination, unzip=unzip)
            except Exception as err:
                self.debug.put("ERROR DOWNLOADING FILE {}. {}".format(file,err), "error")
                return False
        return True
