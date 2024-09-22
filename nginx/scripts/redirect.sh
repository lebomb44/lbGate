#!/bin/bash

echo "Content-Type: text/html"
echo ""

/bin/rm /dev/shm/_redirect_*
redirect_name=${SCRIPT_NAME//\//_}
if [ "$redirect_name" != "_redirect_none" ]; then
  /usr/bin/touch /dev/shm/$redirect_name
fi

#echo $redirect_name
#env

echo '<html><head>'
echo '<meta http-equiv="refresh" content="0;URL=http://'${SERVER_NAME}'">';
echo '</head></html>'

