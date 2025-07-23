#!/usr/bin/env bash

set -ef

cli_help() {
  cli_name=${0##*/}
  echo "
$cli_name
CDC-MANAGER entrypoint cli
Usage: $cli_name [command] [queues]
Commands:
  
  
  web       deploy web
  migrate   deploy migrate
  *         Help
"
  exit 1
}

case "$1" in
  
  
  web)
    uwsgi --ini ./uwsgi.ini --enable-threads --single-interpreter --gevent 100
    ;;
  migrate)
    flask db upgrade
    ;;
  *)
    cli_help
    ;;
esac