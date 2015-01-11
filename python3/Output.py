from Waypoint import *
import time

## Output ####################################################
class Output:
    def __init__(self):
        t1 = time.time()
        t2 = time.gmtime(t1)
        self._time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t2)
        self._initSymbols()

    def _initSymbols(self):
        pass

    def print(self, waypoints):
        self._printHead()
        self._printWaypoints(waypoints)
        self._printFoot()

    def _printHead(self):
        pass

    def _printWaypoints(self, waypoints):
        waypoints.print(self)

    def printMark(self, waypoint):
        if waypoint.isEmpty():
            return False
        else:
            self._printMark(waypoint)
            return True

    def _printMark(self, waypoint):
        pass

    def printStage(self, stage):
        if stage.isEmpty():
            return False
        else:
            self._printStage(stage)
            return True

    def _printStage(self, waypoint):
        pass

    def _printFoot(self):
        pass


## ListOutput ################################################
class ListOutput(Output):
    def __init__(self):
        Output.__init__(self)

    def _printHead(self):
        pass

    def _printWaypoints(self, waypoints):
        waypoints.print(self)

    def printMark(self, waypoint):
        if waypoint.isEmpty():
            return False
        else:
            self._printMark(waypoint)
            return True

    def _printMark(self, waypoint):
        code = waypoint.getGcCode() + ":"
        print("{:<8s}  {:<45s} {:s}".format(code, waypoint.getName(), waypoint.getWaypointType()))

    def printStage(self, stage):
        if stage.isEmpty():
            return False
        else:
            self._printStage(stage)
            return True

    def _printStage(self, stage):
        self._printMark(stage)

    def _printFoot(self):
        pass


## GpxOutput #################################################
class GpxOutput(Output):
    def __init__(self, caption):
        self._symbol = {}
        self._caption = caption
        Output.__init__(self)

    def _initSymbols(self):
        self._symbol[WaypointType.to_be_found] = "Navaid, Amber"
        self._symbol[WaypointType.archived] = "Navaid, Red"
        self._symbol[WaypointType.found] = "Navaid, Green"
        self._symbol[WaypointType.own] = "Navaid, Blue"
        self._symbol[WaypointType.stage] = "Navaid, Violet"
        self._symbol[WaypointType.waypoint] = "Navaid, White"

    def _printHead(self):
        print("""<?xml version="1.0" encoding="UTF-8"?>
<gpx
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    version="1.0"
    creator="gc-gpx.sh"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0 http://www.groundspeak.com/cache/1/0/cache.xsd" xmlns="http://www.topografix.com/GPX/1/0">
    <name>""" + self._caption + """</name>
    <desc>GPX file created by gc-gpx.sh</desc>""")
        print("<time>" + self._time + "</time>")

    def _printWaypoints(self, waypoints):
        waypoints.print(self)

    def printMark(self, waypoint):
        if waypoint.isEmpty():
            return False
        else:
            self._printMark(waypoint)
            return True

    def _printMark(self, waypoint):
        print("    <wpt lat=\"" + str(waypoint.getLatitude()) + 
              "\" lon=\"" + str(waypoint.getLongitude()) + "\">")
        print("        <time>" + self._time + "</time>")
        print("        <name>" + waypoint.getGcCode() + " - " +
              waypoint.getName() + "</name>")
        print("        <url>http://coord.info/" + waypoint.getGcCode() +
              "</url>")
        print("        <cmt>" + waypoint.getHint() + "</cmt>")
        print("        <desc>" + waypoint.getName() + " (" +
              waypoint.getSize() + ")</desc>")
        print("        <sym>" + self._symbol[waypoint.getWaypointType()] +
              "</sym>")
        print("    </wpt>")

    def printStage(self, stage):
        if stage.isEmpty():
            return False
        else:
            self._printStage(stage)
            return True

    def _printStage(self, stage):
        self._printMark(stage)

    def _printFoot(self):
        print("</gpx>")


## KmlOutput #################################################
class KmlOutput(Output):
    def __init__(self, caption):
        self._symbol = {}
        self._url = {}
        self.caption = caption
        Output.__init__(self)

    def _initSymbols(self):
        self._symbol[WaypointType.to_be_found] = "yellow"
        self._symbol[WaypointType.archived] = "red"
        self._symbol[WaypointType.found] = "green"
        self._symbol[WaypointType.own] = "blue"
        self._symbol[WaypointType.stage] = "violet"
        self._symbol[WaypointType.waypoint] = "white"

        self._url[WaypointType.to_be_found] = \
            "http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png"
        self._url[WaypointType.archived] = \
            "http://maps.google.com/mapfiles/kml/paddle/red-blank.png"
        self._url[WaypointType.found] = \
            "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png"
        self._url[WaypointType.own] = \
            "http://maps.google.com/mapfiles/kml/paddle/blu-blank.png"
        self._url[WaypointType.stage] = \
            "http://maps.google.com/mapfiles/kml/paddle/purple-blank.png"
        self._url[WaypointType.waypoint] = \
            "http://maps.google.com/mapfiles/kml/paddle/wht-blank.png"

    def _printHeaderSection(self, wp_type):
        print("  <Style id=\"" + self._symbol[wp_type] + "\">")
        print("""    <IconStyle>
      <Icon>
        <href>""" + self._url[wp_type] + """</href>
      </Icon>
    </IconStyle>
  </Style>""")

    def _printHead(self):
        print("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  <name>""" + self.caption + "</name>")
        self._printHeaderSection(WaypointType.to_be_found)
        self._printHeaderSection(WaypointType.archived)
        self._printHeaderSection(WaypointType.found)
        self._printHeaderSection(WaypointType.own)
        self._printHeaderSection(WaypointType.stage)
        self._printHeaderSection(WaypointType.waypoint)



    def _printWaypoints(self, waypoints):
        waypoints.print(self)

    def printMark(self, waypoint):
        if waypoint.isEmpty():
            return False
        else:
            self._printMark(waypoint)
            return True

    def _printMark(self, waypoint):
        print("""  <Placemark>
    <name>""" + waypoint.getName() + """</name>
    <description><![CDATA[http://coord.info/""" + waypoint.getGcCode() + """]]></description>
    <styleUrl>""" + self._symbol[waypoint.getWaypointType()] + """</styleUrl>
    <Point>
      <coordinates>""" + str(waypoint.getLongitude()) + "," + str(waypoint.getLatitude()) + """,0</coordinates>
    </Point>
  </Placemark>""")


    def printStage(self, stage):
        if stage.isEmpty():
            return False
        else:
            self._printStage(stage)
            return True

    def _printStage(self, stage):
        self._printMark(stage)

    def _printFoot(self):
        print("  </Document>")
        print("</kml>")

