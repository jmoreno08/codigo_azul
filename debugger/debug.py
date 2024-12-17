# -*- coding: utf-8 -*-
import io
import os
import time
from datetime import datetime

__name__ = "Debugger"
__author__ = "Juanez"
__license__ = "Pimedica S.A."
__credits__ = ["Pimedica S.A.", "OCTA"]
__email__ = "juangarcia@pimedica.net"
__version__ = 2.3

class styles:
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CSELECTED = '\33[7m'
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CCYAN = '\33[36m'
    CWHITE = '\33[37m'
    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CCYANBG = '\33[46m'
    CWHITEBG = '\33[47m'
    STYLES = ("NORMAL", "WARNING", "ERROR", "SUCCESS")

    @staticmethod
    def customize(t, message, style=0):
        date = datetime.fromtimestamp(t)
        line = styles.CBLUE + "{}".format(date.strftime("%Y-%m-%d")) + styles.CEND
        line += styles.CVIOLET + " {}".format(date.strftime("%H:%M:%S")) + styles.CEND
        line += styles.CITALIC + styles.CCYAN + "({}) ".format(t) + styles.CEND + styles.CEND
        if style==0:
            line += styles.CWHITE + "[" + styles.STYLES[style]+ "]" + styles.CEND + ": "
            line += styles.CWHITE + message + styles.CEND
        elif style==1:
            line += styles.CYELLOWBG + "[" + styles.STYLES[style]+ "]" + styles.CEND + ": "
            line += styles.CYELLOW + message + styles.CEND
        elif style==2:
            line += styles.CREDBG + "[" + styles.STYLES[style] + "]" + styles.CEND + ": "
            line += styles.CRED + message + styles.CEND
        elif style==3:
            line += styles.CGREENBG + "[" + styles.STYLES[style] + "]" + styles.CEND + ": "
            line += styles.CGREEN + message + styles.CEND
        return line
    
    @staticmethod
    def linealize(t, message, style=0):
        date = datetime.fromtimestamp(t)
        line = "{}".format(date.strftime("%Y-%m-%d"))
        line += " {}".format(date.strftime("%H:%M:%S"))
        line += "({}) [".format(t)
        line += styles.STYLES[style] + "]: "
        line += message
        return line

PATH = os.path.dirname(os.path.abspath(__file__))

class Debug(object):
    def __init__(self, name, version, filename="debug"):
        self.file = os.path.join(PATH, filename)
        if not os.path.exists(self.file):
            f = open(self.file, "w")
            f.close()
        self.put("INITIALIZING {}'S DEBUGGER. VERSION {}".format(name, version), "success")
        self.put("DEBUGGER VERSION {} SUCCESSFULLY INITIALIZED".format(__version__), "success")

    def save(self, message):
        with open(self.file, "a") as f:
            f.write("{}\n".format(message))

    def put(self, message, style="normal"):
        t = int(time.time())
        message = message.upper() + "."
        style = styles.STYLES.index(style.upper())
        self.save(styles.linealize(t, message, style))
        line = styles.customize(t, message, style)
        print(line)
        return line