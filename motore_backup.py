## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import ast
# import logging
import threading

import time


class MotoreBackup:
    def __init__(self, fconf):
        self.thFine=False
        self.bks, self.altro, self.cron = self.__get_impostazioni(fconf)

        for ch in self.bks:
            if self.bks[ch]['attivo']:
                # print(self.bks[ch])
                x = threading.Thread(target=self.thread_function, args=(self.bks[ch], 2))
                x.start()

    def __get_impostazioni(self, f):
        with open(f, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
            return d['bks'], d['altro'], d['cron']

    def thread_function(self, name, t):
        while not self.thFine:
            print(str(name['titolo']))
            time.sleep(t)
        print( "FINE: "+str(name['titolo']))
