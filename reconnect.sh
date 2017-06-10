#!/bin/bash
router=`ip route | awk '/default/ {print $3}'`
/bin/ping -q -c1 $router > /dev/null

if [ $? -eq  0 ]
then
  true
  # echo "Network OK"
else
  echo "Network down, fixing..."
  # ifdown --force wlan0
  # sleep 5
  /bin/kill -9 `pidof wpa_supplicant`
  /sbin/ifup --force wlan0
  /sbin/ip route add default via $router dev wlan0
  /bin/mount -a
  echo "wlan0 reconnected at `date`"
fi