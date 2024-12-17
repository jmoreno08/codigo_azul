# -*- coding: utf-8 -*-
from source.caller import Caller
from source.generator import Generator

__name__ = "Caller"
__author__ = "Juanez"
__license__ = "Pimedica"
__credits__ = ["Pimedica", "OCTA", "Juanez"]
__email__ = "juangarcia@pimedica.com"
__version__ = 3.0

def main(debug, path):
    while True:
        try:
            generator = Generator(debug, path)
            generator.generate()
            caller = Caller(debug, path)
            caller.run()
        except Exception as err:
            debug.put("ERROR EXECUTING {}".format(__name__), "error")
            debug.put("{}".format(err), "error")

