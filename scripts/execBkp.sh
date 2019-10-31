#!/bin/bash

DATE=$(date "+%d/%m/%Y - %H:%M:%S")
CONTAINER="compose_mysql_1"
BKP_SCRIPT="/tmp/bkpRestoreDB_full.sh"
BKP_DIR="/ciab/bkp"
STANDBY_SERVER="192.168.0.102"
LOG_FILE="/ciab/logs/bkp/bkp.log"

echo "[INFO] - ${DATE} - Inicando processo de backup do Banco de Dados" >> ${LOG_FILE}
docker exec ${CONTAINER} ${BKP_SCRIPT} bkp >> ${LOG_FILE}
if [[ $? -eq 0 ]]
then
  BKP_FILE=$(ls -lath ${BKP_DIR} | grep dump_ciab | awk '{print $9}' | head -n 1)
  echo "[INFO] - ${DATE} - Arquivo de backup localizado (${BKP_FILE})" >> ${LOG_FILE}
  echo "[INFO] - ${DATE} - Inicando transferencia do arquivo para o servidor StandBy" >> ${LOG_FILE}
  scp ${BKP_DIR}/${BKP_FILE} ${STANDBY_SERVER}:${BKP_DIR} >> ${LOG_FILE}
  echo "[INFO] - ${DATE} - Movendo arquivo de backup para diretorio ${BKP_DIR}/processed" >> ${LOG_FILE}
  mv -v ${BKP_DIR}/${BKP_FILE} ${BKP_DIR}/processed >> ${LOG_FILE}
fi
echo "[INFO] - ${DATE} - Fim da execução do Backup" >> ${LOG_FILE}
echo "####################################################################################" >> ${LOG_FILE}
echo >> ${LOG_FILE}
