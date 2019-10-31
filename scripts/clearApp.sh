#!/bin/bash

compose_file='/ciab/docker/compose/compose.yml'

stopContainer(){
  docker stop $(docker ps -q)
}

removeContainer(){
  docker rm $(docker ps -aq)
  rm -rf /ciab/data/*
}

startContainer(){
  docker-compose -f ${compose_file} up -d
}

stopContainer
removeContainer
startContainer
