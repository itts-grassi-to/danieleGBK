## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it
import sys
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
        l = sys.argv[0].split("/")
        self.__nomePS = l[len(l)-1].split(".")[0]
        self.__fpar = open(self._path_fpar, "rb")
        self.__leggiVariabiliComunicazione(self.__fpar)

    def __settaVariabiliComunicazione(self, path_fpar, fine, impo):
        fpar = open(path_fpar, "wb")
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
    def esegui(self):
        # st = True
        stesso_minuto = {}
        # print(self.__nomePS)
        #if self._is_running(self.__nomePS):
        #    print("motore_backup - esegui: Processo attivo")
        #    return
        self.__settaVariabiliComunicazione(self._path_fpar, "0", "0")
        print("AVVIO il motore.. brum brum")
        while self.__thFine == 0:
            if self.__impoIni == 1:
                print("restart**********************")
                self.__settaVariabiliComunicazione(NOME_FPAR, str(self.__thFine), "0")
                self._bks, self._altro = self._get_impostazioni()

            for ch in self._bks:
                if ch not in stesso_minuto:
                    stesso_minuto[ch] = ""
                if self._bks[ch]['attivo']:
                    x = datetime.now()
                    # self._printa(datetime.now())
                    # print(ch, "-----", self._bks[ch]['attivo'], "--------------", stesso_minuto[ch] == str(x)[14:16])
                    if self.__startBK(x, self._bks[ch]['cron']):
                        # print(str(x)[14:16])
                        # print("thread_function: seleziono backup")
                        # print("thread_function: stesso_minuto["+ch+"]= "+ stesso_minuto[ch])
                        if self._bks[ch]['attivo'] and stesso_minuto[ch] != str(x)[14:16] :
                            stesso_minuto[ch] = str(x)[14:16]
                            # self._bks[ch]['attivo']=False
                            # print("thread_function: backuppo : " + ch)
                            bf = bkFile()
                            threading.Thread(target=self._esegui, args=(ch, )).start()
                # print("CH: "+ch, self._bks[ch]['attivo'])
            # print("************************leggo variabili")
            self.__leggiVariabiliComunicazione(self.__fpar)
            time.sleep(2)
        self.__fpar.close()
        print("SPENGO il motore.. put put")
# m=MotoreBackup()
# m.esegui()