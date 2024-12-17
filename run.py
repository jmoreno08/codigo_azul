# -*- coding: utf-8 -*-
from debugger.debug import Debug
import os
import sys
import subprocess

__name__ = "Caller"
__author__ = "Juanez"
__license__ = "Pimedica S.A."
__credits__ = ["Pimedica", "OCTA", "Juanez"]
__email__ = "juangarcia@pimedica.com"
__version__ = 3.0

os.environ['DISPLAY'] = ':0'
PATH = os.path.dirname(os.path.abspath(__file__))
debug = Debug(__name__, __version__)

# from updater.update import Update
# updater = Update(__name__, __version__, debug, PATH)
# updater.dependencies()
# if updater.update():
#     debug.put("RESTARTING", "normal")
#     subprocess.call(sys.executable + " " + PATH + "/run.py", shell=True)
#     exit()
# del updater

from source.main import main

main(debug, PATH)
