#!/usr/bin/bash
echo $#
if [ $# -eq 0 ];then
  echo "devi inserire il path dell'applicazione"
  exit
fi
R=`ps -e`
if [[ "$R" == *"engineBK"* ]]; then
  echo "PROCESSO AVVIATO!"
  exit
fi
cd $1
./engineBK.sh&
disown -ah