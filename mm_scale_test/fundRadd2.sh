#!/bin/bash
source ../coinlist
source Radd.txt
count=0
rpcport=60000

if [ -z ${1+x} ]
then 
    echo
    echo "Usage: ./fundRadd2.sh <amount>"
    echo
    exit
fi

amount=$1

echo "TXids=(" > TXids
echo "rpcports=(" > rpcports

while [ "x${coinlist[count]}" != "x" ]
do
  all=${coinlist[count]}
  name=${all%% *}
  if [ "$name" != "" ]
    then
     TXid=$(~/komodo/src/komodo-cli -ac_name=$name sendtoaddress $Radd $amount)
     echo "$TXid....$rpcport"
     echo "'$rpcport'" >> rpcports
     rpcport=$(( rpcport +2 ))
     echo "'$TXid'" >> TXids
    fi
  count=$(( $count +1 ))
done

echo "amount=$(($amount * 100000000))" > amount.txt
echo ")" >> TXids
echo ")" >> rpcports
