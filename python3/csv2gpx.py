import sys;
import csv;
import getopt;
from Output import *
from Waypoint import *

## Config ####################################################
class Config:
    def __init__(self):
        self.__print_own = False
        self.__print_archived = False
        self.__print_found = False
        self.__print_stages = False
        self.__print_waypoints = False
        self.__args = []
        self.__regions = []
        self.__progname = None
        self.__caption = "GC finals"
        self.__output = None

    def getOutput(self):
        return self.__output

    def usage(self):
        progname = self.__progname
        if progname == None:
           progname = "xxx.py"

        print(progname, " [-c <caption>] [-G|-K|-L|-T] [-f] [-a] [-s] [-o] [-w] [-r <region 1>] [-r <region 2>] ...", file=sys.stderr)
        print("    -c <caption>: title of output file", file=sys.stderr)
        print("    -f: also list found caches (green)", file=sys.stderr)
        print("    -a: also list archived caches (red)", file=sys.stderr)
        print("    -s: also list stages (violet)", file=sys.stderr)
        print("    -o: also list own caches (blue)", file=sys.stderr)
        print("    -w: also list arbitrary waypoints (white)", file=sys.stderr)
        print("    -r <region>: evaluate caches in region <region>", file=sys.stderr)
        print("                 may occur multiply. If no region", file=sys.stderr)
        print("                 is selected all caches will be listed.", file=sys.stderr)
        print("    -G: GPX output[default]", file=sys.stderr)
        print("    -K: KML output", file=sys.stderr)
        print("    -T: text output", file=sys.stderr)
        print("    -L: simple list", file=sys.stderr)

    def printOwn(self):
        return self.__print_own

    def printArchived(self):
        return self.__print_archived

    def printFound(self):
        return self.__print_found

    def printStages(self):
        return self.__print_stages

    def printWaypoints(self):
        return self.__print_waypoints

    def getRegions(self):
        return self.__regions

    def getCaption(self):
        return self.__caption

    def getProgramName(self):
        return self.__progname

    def parseCommandLine(self, argv):
        try:
            self.__progname = argv[0]
            opts, args = getopt.getopt(argv[1:], "GKLTac:for:sw")
        except getopt.GetoptError as err:
            print (str(err), file=sys.stderr)
            self.usage()
            sys.exit(1)

        for opt, value in opts:
            if opt == "-o":
                self.__print_own = True
            elif opt == "-a":
                self.__print_archived = True
            elif opt == "-f":
                self.__print_found = True
            elif opt == "-s":
                self.__print_stages = True
            elif opt == "-w":
                self.__print_waypoints = True
            elif opt == "-c":
                self.__caption = value
            elif opt == "-r":
                self.__regions.append(value)
            elif opt == "-G":
                if self.__output != None:
                    self.usage()
                    sys.exit(1)
                self.__output = GpxOutput()
            elif opt == "-K":
                if self.__output != None:
                    self.usage()
                    sys.exit(1)
                self.__output = KmlOutput()
            elif opt == "-L":
                if self.__output != None:
                    self.usage()
                    sys.exit(1)
                self.__output = ListOutput()
            elif opt == "-T":
                if self.__output != None:
                    self.usage()
                    sys.exit(1)
                self.__output = TextOutput()
            else:
                usage()
                sys.exit(1)
        if self.__output == None:
            self.__output = GpxOutput()
        self.__output.setCaption(self.getCaption())
        self.__args__ = args


## Parser ####################################################
class Parser:
    def __init__(self, regions):
        self.config = config

    def __setBinaryMode(self):
        try:
            import msvcrt
            import os
            use_msvcrt = True # binary mode in Windows platforms
            msvcrt.setmode (sys.stdin.fileno(), os.O_BINARY)
        except:
            pass

    def __checkRegion(self, row):
        return len(set(self.config.getRegions()).intersection(set(row[1:]))) > 0

    def read(self):
        self.__setBinaryMode()
        handle_all_regions = not self.config.getRegions()
        is_selected_region = False

        reader = csv.reader(sys.stdin)
        Waypoint.passConfiguration(self.config)
        waypoints = Waypoints()

        for row in reader:
            if (not row[0]):
                continue

            if (row[0].lower() == "region"):
                is_selected_region = (handle_all_regions or
                    self.__checkRegion(row))
                continue

            if (is_selected_region and (len(row[0]) > 0)):
                waypoints.insert(Waypoint.create(row))

        return waypoints

config = Config()
config.parseCommandLine(sys.argv)

parser = Parser(config.getRegions())
waypoints = parser.read()

output = config.getOutput()
output.print(waypoints)
