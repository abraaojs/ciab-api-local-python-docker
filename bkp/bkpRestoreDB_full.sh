#!/bin/bash

DB_NAME="ciab"
DB_USER="root"
DB_PASS="root"
DATE=$(date "+%d%m%Y_%H%M")
LOG_DATE=$(date "+%d/%m/%Y - %H:%M:%S")
BKP_FOLDER="/tmp"
DST_BKP_FILE="${BKP_FOLDER}/dump_ciab_${DATE}.sql"
SRC_BKP_FILE=$(ls -lhat /tmp | grep dump_ciab | awk '{print $9}' | head -n 1)
MYSQL_CONF_FOLDER="/etc/mysql/conf.d"
MYSQLDUMP_FILE="${MYSQL_CONF_FOLDER}/mysqldump.cnf"
MYSQL_FILE="${MYSQL_CONF_FOLDER}/mysql.cnf"

checkMysqlCnf() {
  for cnf in ${MYSQLDUMP_FILE} ${MYSQL_FILE}
  do
    grep -i "password=root" ${cnf} > /dev/null

    if [[ $? -eq 1 ]]
    then
      echo "password=root" >> ${cnf}
    fi
  done
}

checkBkpFile() {
  if [[ ! -f ${DST_BKP_FILE} ]]
  then
    echo "[ERROR] - ${LOG_DATE} - Arquivo de backup nao localizado !!"
  fi
}

execBkp() {
  mysqldump -u ${DB_USER} --databases ${DB_NAME} > ${DST_BKP_FILE}
  if [[ $? -eq 1 ]]
  then
    echo "[ERROR] - ${LOG_DATE} - Erro ao executar o backup !!"
  else
    echo "[INFO] - ${LOG_DATE} - Backup executado com sucesso !!"
  fi
}

execRestore() {
  mysql -u ${DB_USER} ${DB_NAME} < ${BKP_FOLDER}/${SRC_BKP_FILE}
  if [[ $? -eq 1 ]]
  then
    echo "[ERROR] - ${LOG_DATE} - Erro ao executar o restore !!"
  else
    echo "[INFO] - ${LOG_DATE} - Restore executado com sucesso !!"
  fi


}

case $1 in
  bkp)
    echo "[INFO] - ${LOG_DATE} - Ajustando arquivos de configuração !!"
    checkMysqlCnf
    echo "[INFO] - ${LOG_DATE} - Iniciando Backup Full do Banco !!"
    execBkp
    checkBkpFile
  ;;
  restore)
    echo "[INFO] - ${LOG_DATE} - Ajustando arquivos de configuração !!"
    checkMysqlCnf
    echo "[INFO] - ${LOG_DATE} - Iniciando Restore Full do Banco !!"
    execRestore
  ;;
esac
