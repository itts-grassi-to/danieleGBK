#*************************************************************************
## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

from danieleRSINK import tbk
import os
import subprocess
import glob

class bkFile(tbk):
    def __init__(self,fConf):
        super().__init__(fConf)
        self.initOK=True
        #self.__f=f
        self.__nomeTAR=""
        self.__flog=f = open(self._fileLOG, "w")
        self.__flog.write("Inizio processo di backup")
        if self._dirDA["remoto"]:
            self.__flog.write("Monto directory da backuppare: "+self._dirDA["da"])
            if not self.isMount(self._dirDA["da"]):
                r=subprocess.run(["sshfs",self._dirDA["da"],self._dirBASE+"/"+self._dirDA["mnt"]],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
                    self.initOK=False
                    return 
                self.__flog.write("\nDirectory montata")
            else:
                self.__flog.write("\nDirectory GIA montata")
            self._dirDA=self._dirBASE+"/"+self._dirDA["mnt"]
        if self._remoto["to"]:
            self.__flog.write("\nMonto directory dei backup: "+self._dirBK)
            if not self.isMount(self._dirBK):
                r=subprocess.run(["sshfs",self._dirBK,self._dirBASE+"/mntBK"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                if r.stderr:
                    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
                    self.initOK=False
                    return
                self.__flog.write("\nDirectory montata")
            else:
                self.__flog.write("\nDirectory GIA montata")
            self._dirBK=self._dirBASE+"/mntBK"
        self.__flog.write("Fine inizializzazione processo")
    def __preparaFile(self):
        self.__nomeTAR=self._do+"-"+self._nome+".tar.gz"
    def __log(self,msg,mail):
        self.__flog.write(msg)
        self.__flog.close()
        if mail:
            dummy=0
            os.system("mail -s  '"+self._nome+"' server.backup@itisgrassi.edu.it < "+self._fileLOG) 
   
    def backuppaRSYNK(self):
        self.__flog.write("\n*********Inizio il processo di backup************")
        #print("*************************************"+self._do)
        self.__flog.write("\nUso come base: "+self._latestDIR)
        attr='-auv --link-dest "'+self._latestDIR+'" --exclude=".cache" '
        r=os.system("rsync "+attr+self._dirDA+"/ "+ self._dirBK+"/"+self._do+"-"+self._nome +" > "+self._fileLOG)
        #r=subprocess.run(["rsync",attr+self._dirDA+"/ "+ self._dirBK+"/"+self._do+"-"+self._nome],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #if r.stderr:
        #    self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
            #self.initOK=False
        #    return
        self.__flog.write("\nRimuovuo: "+self._latestDIR)
        r=os.system("rm -rf "+self._latestDIR)
        #print("\n"+r)
        self.__flog.write("\nNuova base: "+self._dirBK+"/"+self._do+"-"+self._nome)
        r=os.system("ln -s "+self._dirBK+"/"+self._do+"-"+self._nome+" "+self._latestDIR)
        #print("\n"+r)
        
        self.__log("\nPROCESSO ESEGUITO CON SUCESSO\n\n",True)
    def backuppa(self):
        #f = open(self._fileLOG, "a")
        #***********************************************************************
        self.__flog.write("\nCopio il file "+self._dirDA+"/"+self.__f+" in "+self._tmp+"/")
        print("\nCopio il file "+self._dirDA+"/"+self.__f+" in "+self._tmp+"/")
        #if self._remoto["from"]:
        #    r=subprocess.run(["scp",self._dirDA+"/"+self.__f,self._tmp+"/"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #else:
        r=subprocess.run(["cp",self._dirDA+"/"+self.__f,self._tmp+"/"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #print(r.stderr)
        if r.stderr:
            self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
            return
        self.__flog.write("\nFile "+self._dirDA+"/"+self.__f+" copiato")
        #***********************************************************************
        ls=self._getListaBackup()
        if len(ls)!=0:
            ls.reverse()
            print("da fare: controllare data")
            #return
        #***********************************************************************
        self.__flog.write("\nCambio directory: "+self._tmp)
        r=os.chdir(self._tmp)
        if r:
            self.__log("\nERRORE: cambio direcotry",True)
            return
        self.__flog.write("\nDirectory cambiata")
        #***********************************************************************        
        self.__flog.write("\nComprimo "+self.__nomeTAR)
        print("\nComprimo "+self.__nomeTAR)
        self.__preparaFile()
        r=subprocess.run(["tar","zfc",self.__nomeTAR,self.__f],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if r.stderr:
            self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
            return
        self.__flog.write("\nFile compresso")
        #***********************************************************************        
        #self.__preparaFile()
        self.__flog.write("\nCopio file "+self.__nomeTAR+" in "+self._dirBK)
        print("\nCopio file "+self.__nomeTAR+" in "+self._dirBK)
        #if self._remoto["to"]:
        #    r=subprocess.run(["scp",self.__nomeTAR,self._dirBK+"/"+self.__nomeTAR],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #else:
        r=subprocess.run(["cp",self.__nomeTAR,self._dirBK+"/"+self.__nomeTAR],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if r.stderr:
            self.__log("\nERRORE: "+r.stderr.decode("utf-8"),True)
            return
        self.__flog.write("\nFile copiato")
        
        self.__flog.write("\nPulisco "+self._tmp)
        for i in glob.glob(os.path.join(self._tmp,'*')):
            if os.path.isdir(i):
                shutil.rmtree(path)
            else:
                os.remove(i)
        self.__flog.write("\nDirectory ripulita")

        self.__flog.write("\nElimina vecchi")
        r=self._rimuoviVecchi()
        self.__flog.write(r)
        self.__log("\nPROCESSO ESEGUITO CON SUCESSO",True)
        self.__flog.close()
        
        
#c=bkFile("infoschool.json","AXIOSDATABASE.FDB")
#c=bkFile("infoschool.json","pipi.txt")
#if c.initOK:
#    c.backuppa()
