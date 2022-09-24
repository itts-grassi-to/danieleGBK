## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import ast
# import logging
import threading
import datetime
import time

from bkFile import bkFile


# from gmain import *

class MotoreBackup(bkFile):
    def __init__(self):
        # self.fconf = fconf
        self.thFine = False
        self.__impoIni = True
        self.fconf = "./danieleBK.conf"
        threading.Thread(target=self.thread_function, args=(self.fconf,)).start()

    def set_restart_impostazioni(self):
        self.__impoIni = True

    def __get_impostazioni(self, f):
        with open(f, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
        # d=MainW.get_impostazioni(self.fconf)
        return d['bks'], d['altro']

    def __startBK(self, dnow, cron):
        if cron['minuto'] != "*":
            if int(dnow.strftime("%M")) != int(cron['minuto']):
                return False
        if cron['ora'] != "*":
            if int(dnow.strftime("%H")) != int(cron['ora']):
                return False
        if cron['giorno'] != "*":
            if int(dnow.strftime("%d")) != int(cron['giorno']):
                return False
        if cron['mese'] != "*":
            if int(dnow.strftime("%m")) !=int(cron['mese']):
                return False
        if cron['settimana'] != "*":
            if not (int(dnow.strftime("%w")) in cron['settimana']):
                return False

        return True
        # print("Ora: " + dnow.strftime("%H"))
        # print("Mese: " + dnow.strftime("%m"))
        # print("Giorno: " + dnow.strftime("%d"))
        # print("Mese: " + dnow.strftime("%m"))
        # print("Settimana: " + dnow.strftime("%w"))
    def thread_backup(self,bf, ch, bks):
        print("Inizio backup "+ch)
        bf.backuppaRSYNK()
        # time.sleep(60)
        #print("backup finito**********************************************")
        bks[ch]['attivo'] = True
        print("Finisco backup "+ch)

    # bks[ch]['attivo'] = True
    def thread_function(self, fconf):
        st = True
        stesso_minuto = {}
        while not self.thFine:
            if self.__impoIni:
                print("restart**********************")
                self.__impoIni = False
                bks, altro = self.__get_impostazioni(fconf)

            for ch in bks:
                if ch not in stesso_minuto:
                    stesso_minuto[ch] = ""
                if bks[ch]['attivo']:
                    x = datetime.datetime.now()
                    # print(ch, "-----", bks[ch]['attivo'], "--------------", self.__startBK(x, bks[ch]['cron']))
                    if self.__startBK(x, bks[ch]['cron']):
                        # print(str(x)[14:16])
                        # print("thread_function: seleziono backup")
                        # print("thread_function: stesso_minuto["+ch+"]= "+ stesso_minuto[ch])
                        if bks[ch]['attivo'] and stesso_minuto[ch] != str(x)[14:16] :
                            stesso_minuto[ch] = str(x)[14:16]
                            bks[ch]['attivo']=False
                            # print("thread_function: backuppo : " + ch)
                            bf = bkFile(ch, bks)
                            #bf.backuppaRSYNK()
                            threading.Thread(target=self.thread_backup, args=(bf, ch, bks,)).start()
                            #bks[ch]['attivo'] = True

            time.sleep(2)

        print("FINE: thread_function")
