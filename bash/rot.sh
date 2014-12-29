#!/bin/bash

# liest Text aus /dev/stdin und rotiert ihn um $1 Zeichen

rotate() {
    local N=$1
    local STR=$2

    echo ${STR:$N}${STR:0:$N}
}

N=${1:-13}
LOWER=abcdefghijklmnopqrstuvwxyz
UPPER=ABCDEFGHIJKLMNOPQRSTUVWXYZ
ROT_LOWER=$(rotate $N $LOWER)
ROT_UPPER=$(rotate $N $UPPER)

tr ${LOWER}${UPPER} ${ROT_LOWER}${ROT_UPPER}
