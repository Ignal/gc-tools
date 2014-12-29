#!/bin/bash

usage() {
    echo "$NAME <lat> <lon> <jpg-image>" >&2
    echo "    <lat>:  2345678: N 23° 45.678" >&2
    echo "           -2345678: S 23° 45.678" >&2
    echo "    <lon>:  2345678: E 23° 45.678" >&2
    echo "           -2345678: W 23° 45.678" >&2
    echo >&2
    echo "$NAME -d <lat> <lon> <jpg-image>, dezimal" >&2
    echo "    <lat>:  23.45678: N 23.45678" >&2
    echo "           -23.45678: S 23.45678" >&2
    echo "    <lon>:  23.45678: E 23.45678" >&2
    echo "           -23.45678: W 23.45678" >&2
    echo >&2
    echo "Wichtig: exiv2 muss installiert sein." >&2
    echo >&2
    exit 1
}

DEC=0
[ $# -eq 0 ] && usage

if [ $1 = "-d" ]; then
    DEC=1
    shift
fi

[ $# -eq 3 ] || usage
[ -r "$3" ] || { echo "$3 nicht lesbar" >&2; exit 1; }

awk -v lat=$1 -v lon=$2 -v img=$3 -v dec=$DEC '
function values (val)
{
    rest = val % 100000
    deg = (val - rest) / 100000
    val = rest

    rest = val % 1000
    min = (val - rest) / 1000

    sec = rest * 6
    return deg "/1 " min "/1 " sec "/100"
}

function decvalues (val)
{
    deg = int(val)
    rest = 60.0 * (val - deg)
    min = int(rest)
    sec = int(60.0 * (rest - min) + 0.5)
print     deg "/1 " min "/1 " sec "/100"
    return deg "/1 " min "/1 " sec "/100"
}

BEGIN {
    if (lat < 0) {
        reflat = "S"
        lat = -lat
    } else {
        reflat = "N"
    }
    if (dec == 1) {
        vallat = decvalues(lat)
    } else {
        vallat = values(lat)
    }
    cmd = "exiv2 -M\"set Exif.GPSInfo.GPSLatitude " vallat "\" -M \"set Exif.GPSInfo.GPSLatitudeRef " reflat "\" " img
    system(cmd)

    if (lon < 0) {
        reflon = "W"
        lon = -lon
    } else {
        reflon = "E"
    }
    if (dec == 1) {
        vallon = decvalues(lon)
    } else {
        vallon = values(lon)
    }

    cmd = "exiv2 -M\"set Exif.GPSInfo.GPSLongitude " vallon "\" -M \"set Exif.GPSInfo.GPSLongitudeRef " reflon "\" " img
    system(cmd)
}'

