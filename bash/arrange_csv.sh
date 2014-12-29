#/bin/sh

TMP=.$$.bla

awk '
BEGIN {
    FS="#"
}

function coord (prefix, val)
{
    deg = substr(val, 1, 3)
    min = substr(val, 4, 2)
    mil = substr(val, 6)
    ret = sprintf("%c %s° %s.%s", prefix, deg, min, mil)
    return ret
}

function lon (val)
{
    if (val < 0) {
        prefix = "W"
        val = -val;
    } else {
        prefix = "E"
    }
    val = sprintf("%08d", val, 0)
    return coord(prefix, val)
}


function lat (val)
{
    if (val < 0) {
        prefix = "S"
        val = -val;
    } else {
        prefix = "N"
    }
    val = sprintf("%08d", val)
    return coord(prefix, val)
}


NR > 2 {
    if ($1 == "\"head\"") {
        print toupper(substr($2, 2, length($2) - 2)) ":"
        insert = 0
    } else {
        if ($1 != "" && $9 == "") {
            print "GC-Code:   " $1
            print "Name:      " $2
            print "Groesse:   " $3
            print "Position:  " lat($4) "  " lon($5)
            if ($6 != "") {
                print "Hint:      " $6
            }
            print "Lage:      " $7
            if ($8 != "") {
                print "Rätsel:    " $8
            }
            print ""
            insert = 1
        } else {
            if (insert) {
                print ""
                print ""
                insert = 0
            }
        }
    }
}' > $TMP

PRINT=0
if [ $# -gt 0 ]; then
    if [ $1 = "-p" ]; then
        PRINT=1
    fi
fi

if [ $PRINT = 1 ]; then
    iconv -f utf-8 -t latin1 < $TMP | a2ps
else
    cat $TMP
fi

rm -f $TMP
