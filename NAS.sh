#!/usr/bin/python3
import os

from bkFile import bkFile
c=bkFile("/opt/danieleRSINK/NAS.json")
os.chdir(c._dirBASE)

if c.initOK:
    print("Inizializzazione  ok")
    c.backuppaRSYNK()
else:
    print("Inizializzazione NON ok");
print("finito ho")
