echo $#
if [ $# -eq 0 ];then
  echo "devi inserire il path dell'applicazione"
  exit
fi
cd $1
python3 gmain.py&