#!/bin/bash

CONTAINER="compose_mysql_1"
BKP_DIR="/ciab/bkp"
BKP_SCRIPT="/tmp/bkpRestoreDB_full.sh"
LOG_FILE="/ciab/logs/restore/restore.log"

while true
do
  DATE=$(date "+%d/%m/%Y - %H:%M:%S")
  echo "[INFO] - ${DATE} - Inicando processo de restore do Banco de Dados" >> ${LOG_FILE}
  BKP_FILE=$(ls -lath ${BKP_DIR} | grep dump_ciab | awk '{print $9}' | head -n 1)
  if [[ ! -z ${BKP_FILE} ]]
  then
  echo "[INFO] - ${DATE} - Arquivo de backup localizado (${BKP_FILE})" >> ${LOG_FILE}
    docker exec ${CONTAINER} ${BKP_SCRIPT} restore >> ${LOG_FILE}
    if [[ $? -eq 0 ]] 
    then
     echo "[INFO] - ${DATE} - Excluindo arquivo restaurado (${BKP_FILE})" >> ${LOG_FILE}
      rm -rvf ${BKP_DIR}/${BKP_FILE} >> ${LOG_FILE}
    fi
  fi
  echo "[INFO] - ${DATE} - Fim da execução do Backup" >> ${LOG_FILE}
  echo "####################################################################################" >> ${LOG_FILE}
  echo >> ${LOG_FILE}
  sleep 130
done
