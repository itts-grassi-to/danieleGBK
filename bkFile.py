# *************************************************************************
## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

# from danieleRSINK import tbk
import os
import ast
import subprocess
from datetime import datetime


CURRDIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True

class bkFile():
    #def __init__(self, ch, bks, cd):
    def _printa(self, s):
        if DEBUG:
            print(s)
    def __init__(self):
        self._path_fconf = os.path.join(CURRDIR, 'danieleBK.conf')
        self._path_fpar = os.path.join(CURRDIR, 'comunica.conf')
        self._path_flog = os.path.join(CURRDIR, 'comunica.conf')
        self._bks, self._altro = self.__get_impostazioni()
        # self.__inizializza_backup()
        #self.initOK = True
        # self._flog = open(self._fileLOG, "w")
    def _esegui(self):
        self._flog.write("Inizio processo di backup")
        if self.__inizializza_paths():
            self.__backuppa()

    def __inizializza_paths(self):
        if self._remotoDA:
            self._flog.write("\nMonto directory da backuppare: " + self._dirDA)
            mntDA = self._dirBASE + "/" + self._mntDA
            if not self.__isMount(self._dirDA):
                r = subprocess.run(["sshfs", self._dirDA, mntDA],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: " + r.stderr.decode("utf-8"), True)
                    self.initOK = False
                    return False
                self._flog.write("\nDirectory montata")
            else:
                self._flog.write("\nDirectory GIA montata")
            self._dirDA = mntDA
        if self._remotoTO:
            self._flog.write("\nMonto directory dei backup: " + self._dirBK)
            mntTO = self._dirBASE + "/" + self._mntTO
            if not self.__isMount(self._dirBK):
                r = subprocess.run(["sshfs", self._dirBK, mntTO], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: " + r.stderr.decode("utf-8"), True)
                    self.initOK = False
                    return False
                self._flog.write("\nDirectory montata")
            else:
                self._flog.write("\nDirectory GIA montata")
            self._dirBK = mntTO

            self._latestDIR = self._dirBK + "/" + "latestDIR"+self._mntTO
        self._flog.write("\nFine inizializzazione processo")
        return True
    def __get_impostazioni(self):
        with open(self._path_fconf, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
        # d=MainW.get_impostazioni(self.fconf)
        return d['bks'], d['altro']
    def __inizializza_backup(self, ch):
        data = self._bks[ch]
        if DEBUG:
            self._printa(data)
        self._remotoDA = data['dirDA']["remoto"]
        self._remotoTO = data['dirTO']["remoto"]
        self._dirBASE = CURRDIR
        self._dirDA = data['dirDA']["da"]
        self._dirBK = data['dirTO']["to"]
        self._mntDA = data['dirDA']["mnt"]
        self._mntTO =  data['dirTO']["mnt"]
        self._nome = ch
        self._flog = open(self._path_flog + "/" + self._nome + ".log", "w")
        self._do = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        self._latestDIR = self._dirBK + "/" + "latestDIR"
        self._nomeStatoFile = "stf.bin"
        self.__nomeTAR = self._do + "-" + self._nome + ".tar.gz"
    def __isMount(self, sub):
        r = subprocess.run(["df"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return sub in str(r.stdout)
    def __log(self, msg, mail):
        self._flog.write(msg)
        self._flog.close()
        if mail and not DEBUG:
            dummy = 0
            os.system("mail -s  '" + self._nome + "' server.backup@itisgrassi.edu.it < " + self._fileLOG)

    def __backuppa(self):
        self._flog.write("\n*********Inizio il processo di backup************")
        self._flog.write("\nUso come base: " + self._latestDIR)
        attr = '-auv --link-dest "' + self._latestDIR + '" --exclude=".cache" '
        dirBK = self._dirBK + "/" + self._do + "-" + self._nome
        rsync = "rsync " + attr + "\n\t" + self._dirDA + "/\n\t" + dirBK + " > " + self._fileLOG
        self._flog.write("\n" + rsync)
        r = os.system("rsync " + attr + self._dirDA + "/ " + dirBK + " > " + self._fileLOG)
            # "rsync " + attr + self._dirDA + "/ " + self._dirBK + "/" + self._do + "-" + self._nome + " > " + self._fileLOG)
        # r=subprocess.run(["rsync",attr+self._dirDA+"/ "+ self._dirBK+"/"+self._do+"-"+self._nome],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # if r.stderr:
        #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
        # self.initOK=False
        #    return
        self._flog.close()
        self._flog = f = open(self._fileLOG, "a")
        self._flog.write("\nRimuovuo: " + self._latestDIR)
        r = os.system("rm -rf " + self._latestDIR)
        self._flog.write("\nNuova base: " + self._dirBK + "/" + self._do + "-" + self._nome)
        self._flog.write("\nCreo link: ln -s " + self._dirBK + "/" + self._do + "-" + self._nome + " " + self._latestDIR)
        r = os.system("ln -s " + self._dirBK + "/" + self._do + "-" + self._nome + " " + self._latestDIR)

        self.__log("\nPROCESSO ESEGUITO CON SUCESSO\n\n", True)
        self._flog.close()

# c=bkFile('chDef')
# c._esegui()
