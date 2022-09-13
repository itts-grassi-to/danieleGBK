#*************************************************************************
## CREATO DA ORTU prof. DANIELE
## daniele.ortu@itisgrassi.edu.it

import json

from datetime import date
from datetime import datetime
from os import listdir
from os import remove
from os.path import isfile, join
from os import walk
import subprocess

class tbk:
	
    def __init__(self,fConf):
		#print("costruttore")
        data = json.load(open(fConf))
        #print(data)
        #self._remoto=json.loads(data["remoto"])
        self._remoto=data["remoto"]
        #self._remotoFrom=remoto["from"]
        #self._remotoTO=remoto["to"]
        self._dirBASE=data["dirBASE"]
        self._dirDA=data["dirDA"]
        self._dirBK=data["dirBK"]
        self._tmp=data["dirTMP"]
        self._nome=data["nomeFileBK"]
        self._maxBK=data["maxBK"]
        self._fileLOG=data["dirBASE"]+"/"+data["nomeFileBK"]+".log"
        #self._do=str(date.today())
        self._do=datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        self._latestDIR=self._dirBK+"/"+data["latestDIR"]
        self._nomeStatoFile="stf.bin"
    def isMount(self,sub):
        r=subprocess.run(["df"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return sub in str(r.stdout)
    def stampaConf(self):
        print(self._da)
        print(self._dirBK)
        print(self._tmp)
        print(self._nome)
        print(self._maxBK)
    def getDataOggi(self):
        return self.__do
    def __costruisciNome(self,pt,d,nome):
        return pt+"/"+d+"-"+nome
    def generaFileTest(self,d,n):
        for i in range(n):
            open(self.__costruisciNome()+str(i),'a').close()
            #curr_date_temp = date.strptime(self.__do, "%y-%m-%a")
            #new_date = curr_date_temp + datetime.timedelta(days=5)
            #print(new_date)
    def _getListaBackup(self):
        l=[ f for f in listdir(self._dirBK) if isfile(join(self._dirBK , f))]
        return self.__filtraLista(l)
    def __filtraLista(self,l):
        l=[f for f in l if f[len(self._do)+1:len(self._do)+1+len(self._nome)]==self._nome ]
        #print("2022-07-17-bkDaniele0"[len(self.__do):len(self.__do)+1+len(self.__nome)])
        return l
    def _rimuoviVecchi(self):
        l=self._getListaBackup()
        l.sort()
        n=len(l)-self._maxBK
        #print(n)
        r=""
        if n>0:
            for i in range(n):
                #print(self._dirBK+"/"+l[i])
                remove(self._dirBK+"/"+l[i])
                r+="\nHo rimosso: "+str(l[i])
        return r
    def __getListaDaBackuppare(self,dirpath):
        f=[]
        dirname=[]
        filenames=[]
        lf=[]
        #print(dirpath)
        for(dp,dirname,filenames) in walk(dirpath):
            #print(dirpath)
            f.extend(filenames)
            break
        #lf=[]
        if filenames:
            filenames.sort()
            for f in filenames:
                lf.append(dp+"/"+f)
        if dirname:
            dirname.sort()
            for d in dirname:
                d=dp+"/"+d 
                #print(d)
                lf.extend(self.__getListaDaBackuppare(d) )
        #print(lf)  
        return lf
    def getStatoUltimoSalvataggio(self):
        lstBK=self.__getListaBackup()
        lstBK.reverse()
        
    def backuppa(self):
        lf=self.__getListaDaBackuppare(self.__da)
        print(lf)

#c=tbk("./infoschool.json")
#print(c.isMount("root@172.16.200.200:/home/interbase"))

