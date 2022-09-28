## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

# import ast
# import os
import threading
import datetime
import time

from bkFile import *


class MotoreBackup(bkFile):
    def __init__(self):

        super().__init__()
        # print(self._path_fpar)
        self.__settaVariabiliComunicazione(self._path_fpar, "0", "0")
        self.__fpar = open(self._path_fpar, "rb")
        self.__leggiVariabiliComunicazione(self.__fpar)
    def __settaVariabiliComunicazione(self, fpar, fine, impo):
        fpar = open(fpar, "wb")
        fpar.write((fine+impo).encode("utf-8"))
        fpar.close()

    def __leggiVariabiliComunicazione(self, fpar):
        fpar.seek(0, 0)
        tmp = fpar.read(2)
        self.__thFine = tmp[0] - 48
        self.__impoIni = tmp[1] - 48
        # print(tmp,self.__thFine,self.__impoIni)

    def set_restart_impostazioni(self):
        self.__impoIni = 1
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
    def thread_backup(self,bf, ch, bks):
        print("Inizio backup "+ch)
        bf.backuppaRSYNK()
        # time.sleep(60)
        #print("backup finito**********************************************")
        bks[ch]['attivo'] = True
        print("Finisco backup "+ch)
    def esegui(self):
        # st = True
        stesso_minuto = {}
        while self.__thFine == 0:
            if self.__impoIni == 1:
                print("restart**********************")
                self.__impoIni = False
                bks, altro = self.__get_impostazioni(self._fconf)

            for ch in self._bks:
                if ch not in stesso_minuto:
                    stesso_minuto[ch] = ""
                if self._bks[ch]['attivo']:
                    x = datetime.now()
                    print(datetime.now())
                    # print(ch, "-----", bks[ch]['attivo'], "--------------", self.__startBK(x, bks[ch]['cron']))
                    if self.__startBK(x, self._bks[ch]['cron']):
                        # print(str(x)[14:16])
                        # print("thread_function: seleziono backup")
                        # print("thread_function: stesso_minuto["+ch+"]= "+ stesso_minuto[ch])
                        if bks[ch]['attivo'] and stesso_minuto[ch] != str(x)[14:16] :
                            stesso_minuto[ch] = str(x)[14:16]
                            bks[ch]['attivo']=False
                            # print("thread_function: backuppo : " + ch)
                            bf = bkFile(ch, bks, CURRDIR)
                            #bf.backuppaRSYNK()
                            threading.Thread(target=self.thread_backup, args=(bf, ch, bks,)).start()
                            #bks[ch]['attivo'] = True

            time.sleep(2)
            self.__leggiVariabiliComunicazione(self.__fpar)
        self.__fpar.close()
        print("FINE: thread_function")
m=MotoreBackup()
m.esegui()