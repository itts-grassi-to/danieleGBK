#!/usr/bin/python3
import os
CURRDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRDIR)

from motore_backup import MotoreBackup
m=MotoreBackup()
m.esegui()