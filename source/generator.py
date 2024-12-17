import os
import json
from gtts import gTTS

__name__ = "Generator"
__author__ = "Juanez"
__license__ = "Pimedica"
__credits__ = ["Pimedica", "OCTA", "Juanez"]
__email__ = "juangarcia@pimedica.com"
__version__ = 3.0

class Generator(object):
    def __init__(self, debug, path):
        self.debug = debug
        self.path = path
        self.data = os.path.join(self.path, "data")
        self.sound = os.path.join(self.data, "sound")
        self.buttons = {}
        f = open(os.path.join(self.data, "buttons"))
        self.buttons = json.load(f)
        f.close()
        self.debug.put("GENERATOR SUCCESSFULLY INITIALITED", "success")

    def generate(self):
        for button in self.buttons:
            f = os.path.join(self.sound, button)
            if not os.path.exists(f):
                a = None
                if "1" in self.buttons[str(button)]:
                    a = self.buttons[str(button)]['1']
                elif "2" in self.buttons[str(button)]:
                    a = self.buttons[str(button)]['2']
                l = self.buttons[str(button)]['l']
                try:
                    msg = a + " EN " + l + ". EMERGENCIA"
                    tts = gTTS(text=msg, lang='es-US')
                    tts.save(f)
                    self.debug.put("GENERATED {} FILE".format(f), "success")
                except Exception as err:
                    self.debug.put("ERROR GENERATING {} FILE: {}".format(f, err), "error")
