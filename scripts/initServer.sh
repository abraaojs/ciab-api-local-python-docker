#!/bin/bash

CON="eth0"
IP_SERVER="192.168.0.101/24"
IP_BKP="192.168.0.102/24"
EXEC_RESTORE="/ciab/scripts/execRestore.sh"
MOTD="/etc/motd"
EXEC_BKP="/ciab/scripts/execBkp.sh"
CRONTAB="/etc/crontab"

activate() {
  ps aux | grep ${EXEC_RESTORE} | grep -v grep | awk '{print $2}' | xargs kill -9
  nmcli c m ${CON} ipv4.address ${IP_SERVER}
  nmcli c d ${CON}
  nmcli c u ${CON}

echo > ${MOTD}
echo >> ${MOTD}
echo "################################################################" >> ${MOTD}
echo "#                                                              #" >> ${MOTD}
echo "#                       SERVIDOR ATIVADO                       #" >> ${MOTD}
echo "#                                                              #" >> ${MOTD}
echo "################################################################" >> ${MOTD}

echo "*/2  *  *  *  * root  ${EXEC_BKP}" >> ${CRONTAB}
}

deactivate() {
  nmcli c m ${CON} ipv4.address ${IP_BKP}
  nmcli c d ${CON}
  nmcli c u ${CON}
  ${EXEC_RESTORE} &

echo > ${MOTD}
echo >> ${MOTD}
echo "################################################################" >> ${MOTD}
echo "#                                                              #" >> ${MOTD}
echo "#                    SERVIDOR DESATIVADO                       #" >> ${MOTD}
echo "#                                                              #" >> ${MOTD}
echo "################################################################" >> ${MOTD}

  grep ${EXEC_BKP} ${CRONTAB}
  if [[ $? -eq 0 ]]
  then
    sed -i "$ d" ${CRONTAB}
  fi
}

$1
