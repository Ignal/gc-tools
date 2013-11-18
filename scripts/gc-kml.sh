#!/bin/bash

usage() {
    echo "$NAME [-c <caption>] [-f] [-a] [-r <region 1>] [-r <region 2>] ..." >&2
    echo "    -c <caption>: Titel des KML-Files" >&2
    echo "    -f: zeige auch gefundene an (gruen)" >&2
    echo "    -a: zeige auch archivierte an (rot)" >&2
    echo "    -s: zeige auch Stages an (violett)" >&2
    echo "    -o: zeige auch eigene an (blau)" >&2
    echo "    -r <region>: werte Caches aus Region <region> aus" >&2
    echo "                 kann mehrfach vorkommen. Wenn keine Region" >&2
    echo "                 vorgegeben wird, werden alle Caches ausgegeben." >&2
    exit 1
}

head() {
cat << EOF
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  <name>$CAPTION</name>
  <Style id="yellow">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/yellow-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Style id="red">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/red-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Style id="green">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/green-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Style id="blue">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/blue-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <Style id="violet">
    <IconStyle>
      <Icon>
        <href>http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/purple-dot.png</href>
      </Icon>
    </IconStyle>
  </Style>
EOF
}

foot() {
cat << EOF
  </Document>
</kml>
EOF
}



CAPTION="GC-Finals"
REGIONS=
NAME=$0

while [ $# -gt 0 ]; do
    if [ $1 = "-f" ]; then
        AWK_OPT="$AWK_OPT -v f=1"
    elif [ $1 = "-a" ]; then
        AWK_OPT="$AWK_OPT -v a=1"
    elif [ $1 = "-s" ]; then
        AWK_OPT="$AWK_OPT -v s=1"
    elif [ $1 = "-o" ]; then
        AWK_OPT="$AWK_OPT -v o=1"
    elif [ $1 = "-c" ]; then
        shift
        if [ $# -eq 0 ]; then
            usage
        fi
        CAPTION="$1"
    elif [ $1 = "-r" ]; then
        shift
        if [ $# -eq 0 ]; then
            usage
        fi
        if [ -n "$REGIONS" ]; then
            REGIONS="${REGIONS}#"
        fi
        REGIONS="${REGIONS}$1"
    else
        usage
    fi
    shift
done

export REGIONS

head
awk $AWK_OPT '
function create_empty_mark (code)
{
    ++n_marks
    gc_code[n_marks] = code
    gc_symbol[code] = ""
}

function fill_mark (symbol, code, name, size, lon, lat, hint)
{
    gc_symbol[code] = symbol
    gc_name[code] = name
    gc_size[code] = size
    gc_lon[code] = lon
    gc_lat[code] = lat
    gc_hint[code] = hint
}

function add_mark (symbol, code, name, size, lon, lat, hint)
{
    if (symbol == "") {
        if (code in gc_symbol) {
            print "unzulaessiger Aufruf von add_mark mit leerem" > "/dev/stderr"
            print "    symbol-Argument:" > "/dev/stderr"
            print "        code = " code > "/dev/stderr"
            exit_code = 1
            exit 1
        }
    } else {
        if (code in gc_symbol) {
            if (gc_symbol[code] == "") {
                fill_mark(symbol, code, name, size, lon, lat, hint)
            } else {
                print "Zeile " NR ": GC-Code " code " kommt mehrfach vor." > "/dev/stderr"
                return
            }
        } else {
            create_empty_mark(code)
            fill_mark(symbol, code, name, size, lon, lat, hint)
        }
    }
}


function add_stage (symbol, code, name, size, lon, lat, hint)
{
    if (!(code in gc_symbol)) {
        create_empty_mark(code)
    }
    if (!(code in n_stages)) {
        n_stages[code] = 0
    }
    ++n_stages[code]
    fill_mark(symbol, code SUBSEP n_stages[code], name, size, lon, lat, hint)
}

function print_mark (code)
{
    split(code, bare_code, SUBSEP)
    print "  <Placemark>"
    print "    <name>" gc_name[code] "</name>"
    print "    <description><![CDATA[http://coord.info/" bare_code[1] "]]></description>"
    print "    <styleUrl>" gc_symbol[code]  "</styleUrl>"
    print "    <Point>"
    print "      <coordinates>" decval(gc_lon[code]) "," decval(gc_lat[code]) ",0</coordinates>"
    print "    </Point>"
    print "  </Placemark>"
}

function decval (val)
{
    if (val < 0) {
        sign = -1
        val = -val;
    } else {
        sign = 1
    }
    rest = val % 100000
    ret = (val - rest) / 100000
    ret += rest / 60000
    ret *= sign
    return ret
}

function init_regions () {
    selected_regions = ENVIRON["REGIONS"]
    if (selected_regions != "") {
        split(selected_regions, tmp_array, "#")
    }
    for (i in tmp_array) {
        regions[tmp_array[i]] = i
    }
}

function init_symbols () {
    symbol_name[""] = "yellow"
    symbol_name["y"] = "red"
    symbol_name["a"] = "red"
    symbol_name["x"] = "green"
    symbol_name["f"] = "green"
    symbol_name["o"] = "blue"
    symbol_name["s"] = "violet"

    valid_symbol["yellow"] = 1

    if (a == 1) {
        valid_symbol["red"] = 1
    }

    if (f == 1) {
        valid_symbol["green"] = 1
    }

    if (o == 1) {
        valid_symbol["blue"] = 1
    }

    if (s == 1) {
        valid_symbol["violet"] = 1
    }
}

function handle_quotes_and_commas(input) {
    is_inside = 0
    input = $0
    output = ""
    max = length(input)
    if (max <= 1) {
        output = input
    } else {
        skip = 0
        char = substr(input, 1, 1)
        next_char = substr(input, 2, 1)
        n = 2
        while (1) {
            if (skip) {
                skip = 0
            } else {
                if (is_inside) {
                    if (char == "\"") {
                        if (next_char == "\"") {
                            output = output "\""
                            skip = 1;
                        } else {
                            is_inside = 0
                        }
                    } else if (char == ",") {
                        output = output magic
                    } else {
                        output = output char
                    }
                } else {
                    if (char == "\"") {
                        is_inside = 1
                    } else {
                        output = output char
                    }
                }
            }
            if (n > max) {
                break;
            }
            ++n
            char = next_char
            next_char = substr(input, n, 1)
        }
    }
    return output
}

function restore_commas() {
    gsub(magic, ",", field[1])
    gsub(magic, ",", field[2])
    gsub(magic, ",", field[3])
    gsub(magic, ",", field[4])
    gsub(magic, ",", field[5])
    gsub(magic, ",", field[6])
    gsub(magic, ",", field[7])
    gsub(magic, ",", field[8])
    gsub(magic, ",", field[9])
}

BEGIN {
    # maskieren von Nutzkommas
    magic="2a7749bb360duzt57c223b3cbf56ai00ad1"

    FS="#"
    CONVFMT="%.13g"

    init_regions()
    init_symbols()

    n_marks = 0
    exit_code = 0
}

NR > 2 {
    prepared_line = handle_quotes_and_commas($0)
    array_length = split(prepared_line, field, ",")
    restore_commas()

    if (field[1] == "") {
        next
    }
    if (field[1] == "region") {
        if (selected_regions == "") {
            selected = 1
        } else {
            selected = 0
            for (field_index = 2;
                   (field_index <= array_length) && !selected; ++field_index) {
                value = field[field_index]
                selected = (value in regions)
            }
        }
    } else if (selected) {
        if (field[9] == "s") {
            add_stage(symbol_name[field[9]], field[1], field[2], field[3], field[5], field[4], field[6])
        } else {
            add_mark(symbol_name[field[9]], field[1], field[2], field[3], field[5], field[4], field[6])
        }
    }
}

END {
    if (exit_code != 0) {
        exit exit_code
    }
    for (i = 1; i <= n_marks; ++i) {
        c = gc_code[i]
        if (gc_symbol[c] in valid_symbol) {
            print_mark(c)
        }
        if ((gc_symbol[c] == "") || (gc_symbol[c] in valid_symbol)) {
            if (c in n_stages) {
                for (j = 1; j <= n_stages[c]; ++j) {
                    if (gc_symbol[c SUBSEP j] in valid_symbol) {
                        print_mark(c SUBSEP j)
                    }
                }
            }
        }
    }
}'

foot
