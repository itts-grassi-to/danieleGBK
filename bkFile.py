# *************************************************************************
## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

# from danieleRSINK import tbk
import os
import subprocess
from datetime import datetime


# import glob


class bkFile():
    def __init__(self, ch, bks,cd):
        # super().__init__(fConf)
        # print("bkFile.__init__ : " + str(bks))

        # print(self._dirBASE)
        self.__inizializza_backup(ch, bks,cd)

        self.initOK = True
        # self.__f=f
        # self.__nomeTAR = ""
        self._flog = f = open(self._fileLOG, "w")
        self._flog.write("Inizio processo di backup")
        if self._remotoDA:
            self._flog.write("\nMonto directory da backuppare: " + self._dirDA)
            if not self.isMount(self._dirDA):
                r = subprocess.run(["sshfs", self._dirDA, self._dirBASE + "/" + self._mntDA],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: " + r.stderr.decode("utf-8"), True)
                    self.initOK = False
                    return
                self._flog.write("\nDirectory montata")
            else:
                self._flog.write("\nDirectory GIA montata")
            self._dirDA = self._dirBASE + "/" + self._mntDA
        if self._remotoTO:
            self._flog.write("\nMonto directory dei backup: " + self._dirBK)
            if not self.isMount(self._dirBK):
                r = subprocess.run(["sshfs", self._dirBK, self._dirBASE + "/" + self._mntTO], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: " + r.stderr.decode("utf-8"), True)
                    self.initOK = False
                    return
                self._flog.write("\nDirectory montata")
            else:
                self._flog.write("\nDirectory GIA montata")
            self._dirBK = self._dirBASE + "/" + self._mntTO

            self._latestDIR = self._dirBK + "/" + "latestDIR"+self._mntTO
        self._flog.write("\nFine inizializzazione processo")

    def __inizializza_backup(self, ch, bks,cd):
        data = bks[ch]
        print(data)
        self._remotoDA = data['dirDA']["remoto"]
        self._remotoTO = data['dirTO']["remoto"]
        self._dirBASE = cd
        self._dirDA = data['dirDA']["da"]
        self._dirBK = data['dirTO']["to"]
        self._mntDA = data['dirDA']["mnt"]
        self._mntTO =  data['dirTO']["mnt"]
        # self._tmp = data["dirTMP"]
        self._nome = ch
        # self._maxBK = data["maxBK"]
        self._fileLOG = self._dirBASE + "/" + self._nome + ".log"
        # self._do=str(date.today())
        self._do = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        self._latestDIR = self._dirBK + "/" + "latestDIR"
        self._nomeStatoFile = "stf.bin"
        self.__nomeTAR = self._do + "-" + self._nome + ".tar.gz"

    # def __preparaFile(self):
    #    self.__nomeTAR = self._do + "-" + self._nome + ".tar.gz"
    def isMount(self, sub):
        r = subprocess.run(["df"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return sub in str(r.stdout)

    def __log(self, msg, mail):
        self._flog.write(msg)
        self._flog.close()
        if mail:
            dummy = 0
            os.system("mail -s  '" + self._nome + "' server.backup@itisgrassi.edu.it < " + self._fileLOG)

    def backuppaRSYNK(self):
        self._flog.write("\n*********Inizio il processo di backup************")
        # print("*************************************"+self._do)
        self._flog.write("\nUso come base: " + self._latestDIR)
        attr = '-auv --link-dest "' + self._latestDIR + '" --exclude=".cache" '
        self._flog.write(
            "rsync " + attr + "\n\t" + self._dirDA + "/\n\t" + self._dirBK + "/" + self._do + "-" + self._nome + " > " + self._fileLOG)
        r = os.system(
            "rsync " + attr + self._dirDA + "/ " + self._dirBK + "/" + self._do + "-" + self._nome + " > " + self._fileLOG)
        # r=subprocess.run(["rsync",attr+self._dirDA+"/ "+ self._dirBK+"/"+self._do+"-"+self._nome],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # if r.stderr:
        #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
        # self.initOK=False
        #    return
        self._flog.close()
        self._flog = f = open(self._fileLOG, "a")
        self._flog.write("\nRimuovuo: " + self._latestDIR)
        r = os.system("rm -rf " + self._latestDIR)
        # print("\n"+r)
        self._flog.write("\nNuova base: " + self._dirBK + "/" + self._do + "-" + self._nome)
        self._flog.write("\nCreo link: ln -s " + self._dirBK + "/" + self._do + "-" + self._nome + " " + self._latestDIR)
        r = os.system("ln -s " + self._dirBK + "/" + self._do + "-" + self._nome + " " + self._latestDIR)
        # print("\n"+r)

        self.__log("\nPROCESSO ESEGUITO CON SUCESSO\n\n", True)
    # def backuppa(self):
    # f = open(self._fileLOG, "a")
    # ***********************************************************************
    # self.__flog.write("\nCopio il file "+self._dirDA+"/"+self.__f+" in "+self._tmp+"/")
    # print("\nCopio il file "+self._dirDA+"/"+self.__f+" in "+self._tmp+"/")
    # if self._remoto["from"]:
    #    r=subprocess.run(["scp",self._dirDA+"/"+self.__f,self._tmp+"/"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # else:
    # r=subprocess.run(["cp",self._dirDA+"/"+self.__f,self._tmp+"/"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # print(r.stderr)
    # if r.stderr:
    #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
    #    return
    # self.__flog.write("\nFile "+self._dirDA+"/"+self.__f+" copiato")
    # ***********************************************************************
    # ls=self._getListaBackup()
    # if len(ls)!=0:
    #    ls.reverse()
    #    print("da fare: controllare data")
    # return
    # ***********************************************************************
    # self.__flog.write("\nCambio directory: "+self._tmp)
    # r=os.chdir(self._tmp)
    # if r:
    #    self.__log("\nERRORE: cambio direcotry",True)
    #    return
    # self.__flog.write("\nDirectory cambiata")
    # ***********************************************************************
    # self.__flog.write("\nComprimo "+self.__nomeTAR)
    # print("\nComprimo "+self.__nomeTAR)
    # self.__preparaFile()
    # r=subprocess.run(["tar","zfc",self.__nomeTAR,self.__f],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # if r.stderr:
    #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
    #    return
    # self.__flog.write("\nFile compresso")
    # ***********************************************************************
    # self.__preparaFile()
    # self.__flog.write("\nCopio file "+self.__nomeTAR+" in "+self._dirBK)
    # print("\nCopio file "+self.__nomeTAR+" in "+self._dirBK)
    # if self._remoto["to"]:
    #    r=subprocess.run(["scp",self.__nomeTAR,self._dirBK+"/"+self.__nomeTAR],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # else:
    # r=subprocess.run(["cp",self.__nomeTAR,self._dirBK+"/"+self.__nomeTAR],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # if r.stderr:
    #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
    #    return
    # self.__flog.write("\nFile copiato")

    # self.__flog.write("\nPulisco "+self._tmp)
    # for i in glob.glob(os.path.join(self._tmp,'*')):
    #    if os.path.isdir(i):
    #        shutil.rmtree(path)
    #    else:
    #        os.remove(i)
    # self.__flog.write("\nDirectory ripulita")

    # self.__flog.write("\nElimina vecchi")
    # r=self._rimuoviVecchi()
    # self.__flog.write(r)
    # self.__log("\nPROCESSO ESEGUITO CON SUCESSO",True)
    # self.__flog.close()

# c=bkFile("infoschool.json","AXIOSDATABASE.FDB")
# c=bkFile("infoschool.json","pipi.txt")
# if c.initOK:
#    c.backuppa()
