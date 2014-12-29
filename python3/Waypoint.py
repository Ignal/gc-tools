import sys;
import csv;
import enum;
from Output import *

## WaypointType ##############################################
class WaypointType(enum.Enum):
    empty = 0
    to_be_found = 1
    found = 2
    archived = 3
    own = 4
    stage = 5
    waypoint = 6


## Waypoint ##################################################
class Waypoint:
    __map_is_initialized = False
    __waypoint_type_map = {}

    @staticmethod
    def decval(value):
        sign = 1
        if value == None:
            return None
        value = int(value)
        if value < 0.0:
            value = - value
            sign = -1
        rest = value % 100000
        ret = (value - rest) // 100000
        ret += rest / 60000
        ret *= sign
        return ret

    @staticmethod
    def createEmptyWaypoint(gc_code):
        params = []
        params.append(gc_code)
        for i in range(1, 9):
            params.append(None)
        return Waypoint(params)

    @staticmethod
    def __setDefaultWaypointTypes():
        Waypoint.__waypoint_type_map[""] = WaypointType.to_be_found
        Waypoint.__waypoint_type_map["s"] = WaypointType.stage
        Waypoint.__waypoint_type_map["f"] = WaypointType.found
        Waypoint.__waypoint_type_map["a"] = WaypointType.archived
        Waypoint.__waypoint_type_map["o"] = WaypointType.own
        Waypoint.__waypoint_type_map["w"] = WaypointType.waypoint
        Waypoint.__map_is_initialized = True

    @staticmethod
    def passConfiguration(config):
        Waypoint.__waypoint_type_map[""] = WaypointType.to_be_found
        if config.printStages():
            Waypoint.__waypoint_type_map["s"] = WaypointType.stage
        else:
            Waypoint.__waypoint_type_map["s"] = None

        if config.printFound():
            Waypoint.__waypoint_type_map["f"] = WaypointType.found
        else:
            Waypoint.__waypoint_type_map["f"] = None

        if config.printArchived():
            Waypoint.__waypoint_type_map["a"] = WaypointType.archived
        else:
            Waypoint.__waypoint_type_map["a"] = None

        if config.printOwn():
            Waypoint.__waypoint_type_map["o"] = WaypointType.own
        else:
            Waypoint.__waypoint_type_map["o"] = None

        if config.printWaypoints():
            Waypoint.__waypoint_type_map["w"] = WaypointType.waypoint
        else:
            Waypoint.__waypoint_type_map["w"] = None
        Waypoint.__map_is_initialized = True

    @staticmethod
    def __getWaypointType(code):
        if code  == None:
            return None
        if code not in Waypoint.__waypoint_type_map:
            print("invalid waypoint code: \"" + code + "\"", file=sys.stderr)
            sys.exit(1)
        return Waypoint.__waypoint_type_map[code]

    @staticmethod
    def create(params):
        if not Waypoint.__map_is_initialized:
           Waypoint.__setDefaultWaypointTypes()

        if Waypoint.__getWaypointType(params[8]) == None:
            return None
        else:
            return Waypoint(params)

    def __init__(self, params):
        if not Waypoint.__map_is_initialized:
           Waypoint.__setDefaultWaypointTypes()

        self.__gc_code = params[0]
        self.__name = params[1]
        self.__size = params[2]
        self.__latitude = Waypoint.decval(params[3])
        self.__longitude = Waypoint.decval(params[4])
        self.__hint = params[5]
        self.__location = params[6]
        self.__advice = params[7]
        if params[8] == None:
            self.__waypoint_type = WaypointType.empty
        else:
            self.__waypoint_type = Waypoint.__getWaypointType(params[8])
        self.__stages = []

    def setValues(self, ref):
        if not self.isEmpty():
            print("waypoint with code: \"" + self.__gc_code + \
                "\" already set", file=sys.stderr)
            sys.exit(1)

        self.__gc_code = ref.getGcCode()
        self.__name = ref.getName()
        self.__size = ref.getSize()
        self.__latitude = ref.getLatitude()
        self.__longitude = ref.getLongitude()
        self.__hint = ref.getHint()
        self.__location = ref.getLocation()
        self.__advice = ref.getAdvice()
        self.__waypoint_type = ref.getWaypointType()

    def isEmpty(self):
        return self.__waypoint_type == WaypointType.empty

    def isStage(self):
        return self.__waypoint_type == WaypointType.stage

    def isWaypoint(self):
        return self.__waypoint_type == WaypointType.waypoint

    def getGcCode(self):
        return self.__gc_code

    def getName(self):
        return self.__name

    def getSize(self):
        return self.__size

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude

    def getHint(self):
        return self.__hint

    def getLocation(self):
        return self.__location

    def getAdvice(self):
        return self.__advice

    def getWaypointType(self):
        return self.__waypoint_type

    def getStages(self):
        return self.__stages

    def appendStage(self, waypoint):
        self.__stages.append(waypoint)

    def __str__(self):
        ret = {}
        ret["GCcode:"] = self.__gc_code
        ret["name:"] = self.__name
        ret["size:"] = self.__size
        ret["latitude:"] = self.__latitude
        ret["longitude:"] = self.__longitude
        ret["hint:"] = self.__hint
        ret["location:"] = self.__location
        ret["advice:"] = self.__advice
        ret["type:"] = self.__waypoint_type
        return str(ret)


## Waypoints #################################################
class Waypoints:
    def __init__(self):
        self.__stages = []
        self.__waypoints = []
        self.__marks = []
        self.__mark_map = {}

    def insert(self, waypoint):
        if waypoint == None:
            return
        if waypoint.isStage():
            self.__addStage(waypoint)
        elif waypoint.isWaypoint():
            self.__addWaypoint(waypoint)
        else:
            self.__addMark(waypoint)

    def __getParent(self, waypoint):
        parent_waypoint = None
        gc_code = waypoint.getGcCode()
        if waypoint.getGcCode() in self.__mark_map:
            return self.__mark_map[gc_code]
        else:
            new_empty_waypoint = Waypoint.createEmptyWaypoint(gc_code)
            self.__addMark(new_empty_waypoint)
            return new_empty_waypoint

    def __addStage(self, waypoint):
        parent = self.__getParent(waypoint)
        parent.appendStage(waypoint)

    def __addWaypoint(self, waypoint): # evtl. ueberfluessig
        self.__addMark(waypoint)

    def __addMark(self, waypoint):
        gc_code = waypoint.getGcCode()
        if gc_code in self.__mark_map:
            self.__mark_map[gc_code].setValues(waypoint)
        else:
            self.__marks.append(waypoint)
            self.__mark_map[gc_code] = waypoint

    def print(self, output):
        for mark in self.__marks:
            output.printMark(mark)
            stages = mark.getStages()
            for stage in stages:
                output.printStage(stage)
