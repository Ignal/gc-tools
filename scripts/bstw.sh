#/bin/bash

REPLY=

while [ 1 ]; do
    echo "Bitte gewuenschtes Wort eingeben: "
    read
    if [ -z "$REPLY" ]; then
        break
    fi
    bstw $REPLY
    echo
done
