import sqlite3
import os
import string # needed for A-Z string shortcut

if os.path.exists('CIFP_parse.sqlite'):
    os.remove('CIFP_parse.sqlite')

conn = sqlite3.connect('CIFP_parse.sqlite')
cursr = conn.cursor()

# To-Dos:
# Add continuation records to tables...
# Complete the first half of the tables
# Complete the 'id' tables



cursr.executescript('''
--VHF navaids
CREATE TABLE D_ (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    VOR_ident   TEXT UNIQUE,
    VOR_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    AirportICAO_id  INTEGER, --points to table PA
    ICAO_id     INTEGER,
    VOR_ICAO_id INTEGER,
    VOR_freq    INTEGER,
    navaidClass1_id INTEGER,
    navaidClass2_id INTEGER,
    navaidClass3_id INTEGER,
    navaidClass4_id INTEGER,
    navaidClass5_id INTEGER,
    VOR_lat     TEXT,
    VOR_long    TEXT,
    DME_name    TEXT UNIQUE,
    DME_lat     TEXT,
    DME_long    TEXT,
    declination TEXT,
    DME_elevation   TEXT,
    meritFigure_id  INTEGER,
    ILSDMEbias  INTEGER,
    freqProtectionDistance  TEXT,
    datum_id    INTEGER,
    routeInappropriate_id   INTEGER,
    DMEserviceVolume_id INTEGER,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--Enroute NDB navaids
CREATE TABLE DB (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    NDB_itent   TEXT UNIQUE,
    NDB_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    AirportICAO_id  INTEGER, --points to table PA
    ICAO_id     INTEGER,
    NDB_ICAO_id INTEGER,
    NDB_freq    INTEGER,
    NDBclass1_id INTEGER,
    NDBclass2_id INTEGER,
    NDBclass3_id INTEGER,
    NDBclass4_id INTEGER,
    NDBclass5_id INTEGER,
    NDB_lat     TEXT,
    NDB_long    TEXT,
    magneticVariation TEXT,
    datum_id    INTEGER,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--Terminal NDB navaids--copy above table fields
CREATE TABLE PN (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    NDB_itent   TEXT UNIQUE,
    NDB_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    AirportICAO_id  INTEGER, --points to table PA
    ICAO_id     INTEGER,
    NDB_ICAO_id INTEGER,
    NDB_freq    INTEGER,
    NDBclass1_id INTEGER,
    NDBclass2_id INTEGER,
    NDBclass3_id INTEGER,
    NDBclass4_id INTEGER,
    NDBclass5_id INTEGER,
    NDB_lat     TEXT,
    NDB_long    TEXT,
    magneticVariation TEXT,
    datum_id    INTEGER,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--enroute waypoints
CREATE TABLE EA (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    waypoint_identifier    TEXT UNIQUE,
    waypoint_name          TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    region_id   INTEGER,
    ICAO_id     INTEGER,
    waypoint_ICAO_id    INTEGER,
    waypointType_id     INTEGER,
    waypointUsage_id    INTEGER,
    waypoint_lat    TEXT,
    waypoint_long   TEXT,
    magneticVariation   TEXT,
    datum_id    INTEGER,
    --nameFormatIndicator_id  INTEGER, --this doesn't appear in FAA file as of Apr 2021
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--enroute airways
CREATE TABLE ER (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    route_name  TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    sequenceNumber  INTEGER,
    fix_identifier  TEXT,
    ICAO_id         INTEGER,
    waypointDescription_id  INTEGER,
    boundaryCode_id INTEGER,
    type_id    INTEGER,
    level_id    INTEGER,
    directionRestriction_id INTEGER
    --cruiseTable_id  INTEGER
    --Don't care about the rest of these in MVP, will come back
);
--airport ref points
CREATE TABLE PA (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    airport_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id   INTEGER
    --Don't care about these in MVP, will come back
);
--SIDs
CREATE TABLE PD (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    SID_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id     INTEGER,
    airport_id  INTEGER,
    SIDType_id     INTEGER, --change for STARs and approach
    SIDtransition_id   INTEGER,
    aircraftCategory_id INTEGER,
    sequenceNumber INTEGER,
    fix_id  INTEGER,
    fixICAO_id  INTEGER,
    fixSecCode_id   INTEGER,
    fixSubSecCode_id    INTEGER,
    waypointDescription1_id  INTEGER,
    waypointDescription2_id  INTEGER,
    waypointDescription3_id  INTEGER,
    waypointDescription4_id  INTEGER,
    turnDirection_id        INTEGER,
    requiredNavPerformance  INTEGER,
    pathAndTermination_id   INTEGER,
    turnDirectionValid_id   INTEGER,
    recommendedNAVAID_id    INTEGER,
    recNAVAIDicao_id    INTEGER,
    arcRadius   INTEGER,
    theta       INTEGER,
    rho         INTEGER,
    magneticCourse  TEXT,
    routeDistanceorTime   TEXT,
    recNAVAIDsec_id     INTEGER,
    recNAVAIDsubsec_id  INTEGER,
    inboundOutbound_id  INTEGER,
    altitudeDescrip_id  INTEGER,
    ATCindicator_id     INTEGER,
    altitude1           TEXT,
    altitude2           TEXT,
    transitionAltitude  INTEGER,
    speedLimit          INTEGER,
    centerFix_id        INTEGER,
    multipleCode        TEXT,
    centerFixICAO_id    INTEGER,
    centerfixSecCode_id INTEGER,
    centerfixSubSecCode_id  INTEGER,
    --GNSS_FMS_indication TEXT, --add this later, useless
    speedLimitDescrip_id    INTEGER,
    SIDTypeQual1_id         INTEGER,
    SIDTypeQual2_id         INTEGER,
    SIDTypeQual3_id         INTEGER,
    preferred           TEXT,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--STARs
CREATE TABLE PE (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    SID_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id     INTEGER,
    airport_id  INTEGER,
    STARType_id     INTEGER,
    STARtransition_id   INTEGER,
    aircraftCategory_id INTEGER,
    sequenceNumber INTEGER,
    fix_id  INTEGER,
    fixICAO_id  INTEGER,
    fixSecCode_id   INTEGER,
    fixSubSecCode_id    INTEGER,
    waypointDescription1_id  INTEGER,
    waypointDescription2_id  INTEGER,
    waypointDescription3_id  INTEGER,
    waypointDescription4_id  INTEGER,
    turnDirection_id        INTEGER,
    requiredNavPerformance  INTEGER,
    pathAndTermination_id   INTEGER,
    turnDirectionValid_id   INTEGER,
    recommendedNAVAID_id    INTEGER,
    recNAVAIDicao_id    INTEGER,
    arcRadius   INTEGER,
    theta       INTEGER,
    rho         INTEGER,
    magneticCourse  TEXT,
    routeDistanceorTime   TEXT,
    recNAVAIDsec_id     INTEGER,
    recNAVAIDsubsec_id  INTEGER,
    inboundOutbound_id  INTEGER,
    altitudeDescrip_id  INTEGER,
    ATCindicator_id     INTEGER,
    altitude1           TEXT,
    altitude2           TEXT,
    transitionAltitude  INTEGER,
    speedLimit          INTEGER,
    verticalAngle       TEXT,
    centerFix_id        INTEGER,
    multipleCode        TEXT,
    centerFixICAO_id    INTEGER,
    centerfixSecCode_id INTEGER,
    centerfixSubSecCode_id  INTEGER,
    --GNSS_FMS_indication TEXT, --add this later, useless
    speedLimitDescrip_id    INTEGER,
    SIDTypeQual1_id         INTEGER,
    SIDTypeQual2_id         INTEGER,
    SIDTypeQual3_id         INTEGER,
    preferred           TEXT,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--Approach records
CREATE TABLE PF (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    SID_name    TEXT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id     INTEGER,
    airport_id  INTEGER,
    appchType_id     INTEGER,
    appchTransition_id   INTEGER,
    aircraftCategory_id INTEGER,
    sequenceNumber INTEGER,
    fix_id  INTEGER,
    fixICAO_id  INTEGER,
    fixSecCode_id   INTEGER,
    fixSubSecCode_id    INTEGER,
    waypointDescription1_id  INTEGER,
    waypointDescription2_id  INTEGER,
    waypointDescription3_id  INTEGER,
    waypointDescription4_id  INTEGER,
    turnDirection_id        INTEGER,
    requiredNavPerformance  INTEGER,
    pathAndTermination_id   INTEGER,
    turnDirectionValid_id   INTEGER,
    recommendedNAVAID_id    INTEGER,
    recNAVAIDicao_id    INTEGER,
    arcRadius   INTEGER,
    theta       INTEGER,
    rho         INTEGER,
    magneticCourse  TEXT,
    routeDistanceorTime   TEXT,
    recNAVAIDsec_id     INTEGER,
    recNAVAIDsubsec_id  INTEGER,
    inboundOutbound_id  INTEGER,
    altitudeDescrip_id  INTEGER,
    ATCindicator_id     INTEGER,
    altitude1           TEXT,
    altitude2           TEXT,
    transitionAltitude  INTEGER,
    speedLimit          INTEGER,
    verticalAngle       TEXT,
    procedureTurnFlag_id  INTEGER,
    multipleCode        TEXT,
    --GNSS_FMS_indication TEXT, --add this later, useless
    speedLimitDescrip_id    INTEGER,
    SIDTypeQual1_id         INTEGER,
    SIDTypeQual2_id         INTEGER,
    SIDTypeQual3_id         INTEGER,
    preferred           TEXT,
    file_rec        INTEGER,
    cycle_date      INTEGER
);
--airport runways
CREATE TABLE PG (
    runway_number   TEXT,
    airport_id  INTEGER,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id         INTEGER,
    rwy_length      INTEGER,
    rwy_bearing     TEXT,
    rwy_lat         TEXT,
    rwy_long        TEXT,
    rwy_grade       TEXT,
    ellipse_h       TEXT,
    thresh_elev     TEXT,
    disp_thresh_l   INTEGER,
    rwy_width       INTEGER,
    TCH_val         TEXT,
    stopway_l       INTEGER,
    thresh_h        INTEGER,
    rwy_descrip     TEXT,
    file_rec        INTEGER,
    cycle_date      INTEGER,
    PRIMARY KEY (airport_id, runway_number)
);
--Airport/Heliport Localizer/Glideslopes
CREATE TABLE PI (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    localizer_id      TEXT UNIQUE,
    ICAO_id     INTEGER,
    ILS_cat_id  INTEGER,
    localizerFreq    INTEGER
    runway_number   TEXT,
    localizer_lat     TEXT,
    localizer_long    TEXT,
    localizer_bearing TEXT,
    glidesl_lat TEXT,
    glidesl_long    TEXT,
    localizer_position    INTEGER,
    localizer_width   INTEGER,
    glidesl_angle   INTEGER,
    station_dec TEXT,
    glidesl_elev    TEXT,
    supp_fac_id INTEGER,
    supp_fac_ICAO_id    INTEGER,
    supp_fac_SecCode_id INTEGER,
    supp_fac_SubSecCode_id  INTEGER,
    glidesl_TCH    INTEGER,
    file_rec    INTEGER,
    cycle_date INTEGER
);
--Airport SBAS Path Points
--I'm leaving out the final approach remainder field, seems useless to me
CREATE TABLE PP (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id     INTEGER,
    appch_id INTEGER,
    runway_number   TEXT,
    operation_type  INTEGER,
    route_indicator TEXT,
    SBAS_provider_identifier INTEGER,
    refPathDataSelector INTEGER,
    refPathIdendifier   TEXT,
    appchPerformanceDesignator  INTEGER,
    landingThreshold_lat    TEXT,
    landingThreshold_long   TEXT,
    LTP_height              TEXT,
    glidePathAngle          INTEGER,
    flightPathAlightmentPoint_lat   TEXT,
    flightPathAlightmentPoint_long  TEXT,
    courseWidth INTEGER,
    lengthOffset    INTEGER,
    pathPointTCH    INTEGER,
    TCH_units   INTEGER,
    horizontalAlertLimit    INTEGER,
    verticalAlertLimit      INTEGER,
    file_rec    INTEGER,
    cycle_date  INTEGER
);
--airport MSAs:
CREATE TABLE PS (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    airport_id  INTEGER,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id         INTEGER,
    MSAcenter      TEXT,
    MSAcenter_ICAO_id   INTEGER,
    MSAcenter_SecCode_id    INTEGER,
    MSAcenter_SubSecCode_id INTEGER,
    multipleCode    TEXT,
    magOrTrue_id    INTEGER,
    SectorBearing_1     INTEGER,
    SectorAltitude_1    INTEGER,
    SectorRadius_1      INTEGER,
    SectorBearing_2     INTEGER,
    SectorAltitude_2    INTEGER,
    SectorRadius_2      INTEGER,
    SectorBearing_3     INTEGER,
    SectorAltitude_3    INTEGER,
    SectorRadius_3      INTEGER,
    SectorBearing_4     INTEGER,
    SectorAltitude_4    INTEGER,
    SectorRadius_4      INTEGER,
    SectorBearing_5     INTEGER,
    SectorAltitude_5    INTEGER,
    SectorRadius_5      INTEGER,
    SectorBearing_6     INTEGER,
    SectorAltitude_6    INTEGER,
    SectorRadius_6      INTEGER,
    SectorBearing_7     INTEGER,
    SectorAltitude_7    INTEGER,
    SectorRadius_7      INTEGER,
    file_rec    INTEGER,
    cycle_date  INTEGER
);
CREATE TABLE UC (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id         INTEGER,
    airspaceType_id INTEGER,
    airspace_center_id  INTEGER,
    center_SecCode_id   INTEGER,
    center_SubSecCode_id INTEGER,
    airspaceClassification_id   INTEGER,
    multipleCode    TEXT,
    sequenceNumber  INTEGER,
    level_id    INTEGER,
    timeCode_id INTEGER,
    notamActivation_id  INTEGER,
    boundaryVia_id  INTEGER,
    latitude    TEXT,
    longitude   TEXT,
    arcOriginLat    TEXT,
    arcOriginLong   TEXT,
    arcDistance     INTEGER,
    arcBearing      INTEGER,
    requiredNavPerformance  INTEGER,
    lowerLimit  TEXT,
    altitudeUnitLower_id INTEGER,
    upperLimit  TEXT,
    altitudeUnitUpper_id INTEGER,
    airspaceName_id INTEGER,
    file_rec    INTEGER,
    cycle_date  INTEGER
);
CREATE TABLE UR (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    AreaCode_id INTEGER,
    SecCode_id  INTEGER,
    SubSecCode_id   INTEGER,
    ICAO_id         INTEGER,
    restrictiveType_id  INTEGER,
    restrictiveDesignation_id   INTEGER,
    multipleCode    TEXT,
    sequenceNumber  INTEGER,
    level_id    INTEGER,
    timeCode_id INTEGER,
    notamActivation_id  INTEGER,
    boundaryVia_id  INTEGER,
    latitude    TEXT,
    longitude   TEXT,
    arcOriginLat    TEXT,
    arcOriginLong   TEXT,
    arcDistance     INTEGER,
    arcBearing      INTEGER,
    lowerLimit  TEXT,
    altitudeUnitLower_id INTEGER,
    upperLimit  TEXT,
    altitudeUnitUpper_id INTEGER,
    airspaceName_id INTEGER,
    file_rec    INTEGER,
    cycle_date  INTEGER
);
''')


cursr.executescript('''
--The following are consistent items in many entries:
CREATE TABLE AreaCode (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    area    TEXT UNIQUE
);
CREATE TABLE SecCode (
    section TEXT,
    subsec  TEXT,
    PRIMARY KEY (section, subsec)
);
CREATE TABLE RtType_ER (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    type    TEXT UNIQUE
);
CREATE TABLE RtType_SIDSTAR (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    type    TEXT UNIQUE
);
CREATE TABLE ApproachType (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    type    TEXT UNIQUE
);
CREATE TABLE Rte_Identifier (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    rte_name    TEXT UNIQUE
);
CREATE TABLE Approach_Identifier (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Appch_name    TEXT UNIQUE
);
CREATE TABLE ICAOcode (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code    TEXT UNIQUE
);
CREATE TABLE TCHunits (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    unit    TEXT UNIQUE
);
CREATE TABLE MagneticTrueIndicator (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    magOrTrue   TEXT UNIQUE
);
CREATE TABLE AirspaceTypes (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    type    TEXT UNIQUE
);
CREATE TABLE AirspaceClassifications (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class    TEXT UNIQUE
);
CREATE TABLE NOTAMactivationTypes (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    notamActivation TEXT UNIQUE
);
CREATE TABLE LimitUnits (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    unit TEXT UNIQUE
);
CREATE TABLE ControlledAirspaceName (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE FigureOfMerit (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    figure  INTEGER UNIQUE
);
--VOR is Inappropriate for RNAV 1 or RNAV 2 routes:
CREATE TABLE RouteInappropriate (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    YorN    TEXT UNIQUE
);
CREATE TABLE DMEserviceVolume (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    serviceVolume   TEXT UNIQUE
);
CREATE TABLE RegionCode (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code   TEXT UNIQUE
);
CREATE TABLE DatumCode (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code    TEXT UNIQUE
);
CREATE TABLE SIDtransitionCodes (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code    TEXT UNIQUE
);
CREATE TABLE aircraftCategories (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    category    TEXT UNIQUE
);
CREATE TABLE waypointDescription1 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    desc    TEXT UNIQUE
);
CREATE TABLE waypointDescription2 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    desc    TEXT UNIQUE
);
CREATE TABLE waypointDescription3 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    desc    TEXT UNIQUE
);
CREATE TABLE waypointDescription4 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    desc    TEXT UNIQUE
);
CREATE TABLE waypointUsage (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code    TEXT UNIQUE
);
CREATE TABLE turnDirections (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    direction    TEXT UNIQUE
);
CREATE TABLE SID_STAR_Appch_Paths (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    pathType    TEXT UNIQUE
);
CREATE TABLE turnDirectionValid (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    turnRequired    TEXT UNIQUE
);
CREATE TABLE InboundOutboundFlag (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    flag    TEXT UNIQUE
);
CREATE TABLE AltitudeDesciption (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    descrip    TEXT UNIQUE
);
CREATE TABLE ATCindicator (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    flag    TEXT UNIQUE
);
CREATE TABLE SpeedLimitDescription (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    code    TEXT UNIQUE
);
CREATE TABLE procedureTurnFlag (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    flag    TEXT UNIQUE
);
CREATE TABLE NAVAIDclass1 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NAVAIDclass2 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NAVAIDclass3 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NAVAIDclass4 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NAVAIDclass5 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NDBclass1 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NDBclass2 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NDBclass3 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NDBclass4 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
CREATE TABLE NDBclass5 (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    class   TEXT UNIQUE
);
''')

KNOWN_AREACODES = [('CAN',),('EEU',),('LAM',),('PAC',),('SPA',),('USA',)]
KNOWN_SECCODES = [('AS',),('D ',),('DB',),('EA',),('ER',),
    ('HA',),('HC',),('HF',),('HS',),('PA',),('PC',),
    ('PD',),('PE',),('PF',),('PG',),('PI',),('PN',),
    ('PP',),('PS',),('UC',),('UR',)]
ROUTE_TYPES_ER = [('A',),('C',),('D',),('H',),('O',),('R',),('S',),('T',)]
ROUTE_TYPES_RTE_QUAL1 = [('G',),('F',),('A',),('U',)]
ROUTE_TYPES_RTE_QUAL2 = [('R',),('P',),('T',)]
ROUTE_TYPES_RTE_QUAL3 = [('W',),('Z',),('Y',),('X',),('B',),('P',),('C',),('D',),
    ('E',),('A',),('G',),('U',),('V',),('N',)]
ROUTE_TYPES_SIDS = [('0',),('1',),('2',),('3',),('T',),('V',)]
ROUTE_TYPES_STARQUAL1 = [('D',),('G',),('R',),('H',),('P',)]
ROUTE_TYPES_STARQUAL2 = [('D',),('E',),('F',),('G',),('W',),('X',)]
ROUTE_TYPES_STARQUAL3 = [('Z',),('Y',),('X',),('B',),('P',),('D',),('E',),('F',),
    ('A',),('G',),('M',),('U',),('V',)]
ROUTE_TYPES_APPCH = [('A',),('B',),('D',),('F',),('G',),('H',),('I',),('J',),('L',),
    ('M',),('N',),('P',),('Q',),('R',),('S',),('T',),('U',),('V',),('X',),('Z',)]
ROUTE_TYPES_APPCH_QUAL1 = [('D',),('J',),('N',),('P',),('R',),('T',),('U',),('V',),('W',)]
ROUTE_TYPES_APPCH_QUAL2 = [('X',),('E',),('H',),('G',),('A',),('F',),('B',)]
ROUTE_TYPES_APPCH_QUAL3 = [('A',),('B',),('E',),('C',),('H',),('I',),('L',),('S',),('V',),('W',),('X',)]
PATH_TYPES = [('AF',),('CA',),('CD',),('CF',),('CI',),('CR',),('DF',),('FA',),('FC',),('FD',),
              ('FM',),('HA',),('HF',),('HM',),('IF',),('PI',),('RF',),('TF',),('VA',),('VD',),
              ('VI',),('VM',),('VR',)]


cursr.executemany('''INSERT INTO AreaCode (area) VALUES (?);''', KNOWN_AREACODES)
for each in KNOWN_SECCODES:
    cursr.execute('''INSERT INTO SecCode (section,subsec) VALUES (?,?);''',
        (each[0][0],each[0][1]))
cursr.executemany('''INSERT INTO TCHunits (unit) VALUES (?);''', [('F',),('M',)]) #0 for feet, 1 for meters
cursr.executemany('''INSERT INTO MagneticTrueIndicator (magOrTrue) VALUES (?);''', [('M',),('T',)]) #0 for magnetic, 1 for true
cursr.executemany('''INSERT INTO NOTAMactivationTypes (notamActivation) VALUES (?);''', [(' ',),('N',)]) #0 for continuous, 1 for NOTAM only activation
cursr.executemany('''INSERT INTO LimitUnits (unit) VALUES (?);''', [('M',),('A',)]) #0 for MSL, 1 for AGL
cursr.executemany('''INSERT INTO FigureOfMerit (figure) VALUES (?);''', [('0',),('1',),('2',),('3',),('7',),('9',)])
cursr.executemany('''INSERT INTO RouteInappropriate (YorN) VALUES (?);''', [('N',),('Y',)]) #0 for no, 1 for yes
cursr.executemany('''INSERT INTO DMEserviceVolume (serviceVolume) VALUES (?);''', [('A',),('B',),('C',),('D',),('U',)])
cursr.execute('''INSERT INTO RegionCode (code) VALUES (?);''', ('ENRT',))
cursr.execute('''INSERT INTO NAVAIDclass1 (class) VALUES (?);''', ('V',))
cursr.executemany('''INSERT INTO NAVAIDclass2 (class) VALUES (?);''',[('D',),('T',),('M',),('I',),('N',),('P',)])
cursr.executemany('''INSERT INTO NAVAIDclass3 (class) VALUES (?);''',[('T',),('L',),('H',),('U',),('C',)])
cursr.executemany('''INSERT INTO NAVAIDclass4 (class) VALUES (?);''',[('D',),('A',),('B',),('W',),(' ',)])
cursr.executemany('''INSERT INTO NAVAIDclass5 (class) VALUES (?);''',[(' ',),('N',)])
cursr.executemany('''INSERT INTO NDBclass1 (class) VALUES (?);''', [('H',),('S',),('M',)])
cursr.executemany('''INSERT INTO NDBclass2 (class) VALUES (?);''',[('I',),('M',),('O',),('C',)])
cursr.executemany('''INSERT INTO NDBclass3 (class) VALUES (?);''',[('H',),(' ',),('M',),('L',)])
cursr.executemany('''INSERT INTO NDBclass4 (class) VALUES (?);''',[('A',),('B',),('W',),(' ',)])
cursr.execute('''INSERT INTO NDBclass5 (class) VALUES (?);''',('B',))
cursr.executemany('''INSERT INTO SIDtransitionCodes (code) VALUES (?);''',[('0',),('1',),('2',),('3',),('T',),('V',)])
cursr.executemany('''INSERT INTO aircraftCategories (category) VALUES (?);''',
    [each for each in (list(string.ascii_uppercase)[:-1]+[' '])])
cursr.executemany('''INSERT INTO waypointDescription1 (desc) VALUES (?);''',
    [('A',),('E',),('F',),('G',),('H',),('N',),('P',),('R',),('T',),('V',)])
cursr.executemany('''INSERT INTO waypointDescription2 (desc) VALUES (?);''',
    [('B',),('E',),('U',),('Y',)])
cursr.executemany('''INSERT INTO waypointDescription3 (desc) VALUES (?);''',
    [('A',),('B',),('C',),('G',),('M',),('R',),('S',)])
cursr.executemany('''INSERT INTO waypointDescription4 (desc) VALUES (?);''',
    [each for each in (list(string.ascii_uppercase)[0:9]+['M','N','P'])])
cursr.executemany('''INSERT INTO turnDirections (direction) VALUES (?);''', [('L',),('R',),('E',)])
cursr.executemany('''INSERT INTO SID_STAR_Appch_Paths (pathType) VALUES (?);''', PATH_TYPES)
cursr.executemany('''INSERT INTO turnDirectionValid (turnRequired) VALUES (?);''', [('',),('Y',)]) #0 for no, 1 for yes
cursr.executemany('''INSERT INTO InboundOutboundFlag (flag) VALUES (?);''', [('O',),('I',)]) #0 for outbound, 1 for inbound
cursr.executemany('''INSERT INTO AltitudeDesciption (descrip) VALUES (?);''', [('+',),('-',),(' ',),('B',),('C',),('D',),('G',),('O',)])
cursr.executemany('''INSERT INTO ATCindicator (flag) VALUES (?);''', [('A',),('S',)])
cursr.executemany('''INSERT INTO SpeedLimitDescription (code) VALUES (?);''', [(' ',),('+',),('-',)])
cursr.executemany('''INSERT INTO procedureTurnFlag (flag) VALUES (?);''', [('N',),('Y',)]) #0 for no, 1 for yes
cursr.executemany('''INSERT INTO AirspaceTypes (type) VALUES (?);''', [('A',),('C',),('M',),('R',),('T',),('Z',)])
cursr.executemany('''INSERT INTO AirspaceClassifications (class) VALUES (?);''', [('A',),('B',),('C',),('D',),('E',),('G',),('',)])
cursr.executemany('''INSERT INTO waypointUsage (code) VALUES (?);''', [('B',),('H',),('L',),(' ',)])

conn.commit()

#############################
k = 0 # counter for commits

with open('FAACIFP18_full.txt','r') as fh:
    # Get the header info first...
    lastspot = fh.tell() # This "saves" our current position in file stream
    this = fh.readline().rstrip().upper()
    while this[0:3] == 'HDR':
        print(this[0:5])
        lastspot=fh.tell() # we're still in a header line, so update "save"
        this = fh.readline().rstrip().upper()

    # we need to skip back to the first line after the last header line,
    #    because the upcoming '''in fh''' advances ANOTHER line past the last
    #    fh.readline()
    fh.seek(lastspot,0)

    # now for the part we're all here for
    for a in fh:
        k += 1
        this = a.rstrip().upper() # take the line and knock off trailing \n

        recordType = this[0]
        areaCode = this[1:4]
        section = this[4]

        # these two are at the end of every line!
        fileRecord = this[123:128]
        fileCycle = this[128:]
# planning on splitting all of the below into separate functions to be able to
#   clear out variables and not clutter things
        if (section != 'P') and (section != 'H'):
            subsection = this[5]
            if   section == 'D':
                airportIdent = this[6:10]
                airportICAOcode = this[10:12]
                navIdent = this[15:19]
                ICAOCode = this[19:21]
                vorFreq = this[22:27]
                navaidClass = this[27:32]
                navLat = this[32:41]
                navLong = this[41:51]
                datum = this[90:93]
                if   subsection == ' ': # VHF Navaid
                    #continuationRecord = this[21]
                    DMEIdent = this[51:55]
                    DMELat = this[55:64]
                    DMELong = this[64:74]
                    declin = this[74:79]
                    DMEElevation = this[79:84]
                    figOfMerit = this[84]
                    DMEBias = this[85:87]
                    freqProtectDist = this[87:90]
                    vorName = this[93:118]
                    isInappropriate = this[121]
                    DMEServiceVol = this[122]

                    # lots of cursr.execute('') functions here
                elif subsection == 'B': # NDB
                # This is all the same as PN--put them in the same function!
                    magVar = this[74:79]
                    ndbName = this[93:123]

                    # lots of cursr.execute('') functions here
            elif section == 'E':
                if   subsection == 'A': # Waypoints
                # This is all the same as PC--put them in the same function!
                    regionOrAirportCode = this[6:10]
                    regionOrAirportICAOCode = this[10:12]
                    waypointIdent = this[13:19]
                    waypointICAOcode = this[19:21]
                    type = this[26:29]
                    useage = this[30]
                    wayLat = this[32:41]
                    wayLong = this[41:51]
                    magVar = this[74:79]
                    datum = this[90:93]
                    waypointName = this[98:123]

                    # lots of cursr.execute('') functions here
                elif subsection == 'R': # Enroute Airways
                    routeIdent = this[13:19]
                    seqNumber = this[25:29]
                    fixIdent = this[29:34]
                    fixICAOcode = this[34:36]
                    descripCode = this[39:43] # this gets split out into multiples, see above
                    boundaryCode = this[43]
                    routeType = this[44]
                    level = this[45]
                    directFlag = this[46]
                    # there's more stuff here I don't care about in MVP.

                    # lots of cursr.execute('') functions here
            elif section == 'U':
                if   subsection == 'C':
                    pass
                elif subsection == 'R':
                    pass
            else: #error case, new-to-code category
                pass
        else: #section is 'P' (an airport) or 'H' (a heliport)
            subsection = this[12]
            if section == 'H': # IDGAF about heliports in MVP
                if   subsection == 'A':
                    identifier = this[6:10]
                    ICAOcode = this[10:12]
                    # don't care about ATA/IATA code ( this[13:17] )
                    speedLimit = this[22:27]
                    # lots of non MVP stuff

                    datum = this[27:30]
                elif subsection == 'C':
                    pass
                elif subsection == 'F':
                    pass
                elif subsection == 'S':
                    pass
            else: # (section == 'P'):
                if   subsection == 'A':
                    identifier = this[6:10]
                    airportICAOcode = this[10:12]
                    # lots of non MVP stuff

                    datum = this[86:89]
                elif subsection == 'C':
                    # This is all the same as EA--put them in the same function!
                    regionOrAirportCode = this[6:10]
                    regionOrAirportICAOCode = this[10:12]
                    waypointIdent = this[13:19]
                    waypointICAOcode = this[19:21]
                    type = this[26:29]
                    useage = this[30]
                    wayLat = this[32:41]
                    wayLong = this[41:51]
                    magVar = this[74:79]
                    datum = this[90:93]
                    waypointName = this[98:123]

                    # lots of cursr.execute('') functions here
                elif subsection == 'D':
                    airportID = this[6:10]
                    airportICAOcode = this[10:12]
                    SID_ID = this[13:19]
                    routeType = this[19]
                    transitionID = this[20:25]
                    aircraftCategory = this[25]
                    sequenceNumber = this[26:29]
                    fixID = this[29:34]
                    fixICAOid = this[34:36]
                    fixSecCode = this[36]
                    fixSubsecCode = this[37]
                    waypointDescripCode = this[39:43]
                    turnDirection = this[43]
                    reqNavPerformance = this[44:47]
                    pathAndTermination = this[47:49]
                    turnDirectionValid = this[49]
                    recommendedNavaid = this[50:54]
                    recNavaidICAOcode = this[54:56]
                    arcRadius = this[56:62]
                    theta = this[62:66]
                    # commenting out stuff that's not needed for MVP
                    # rho
                    # mag course
                    # routeDistance
                    # section
                    # subsection
                    # inboundOrOutbound
                    altitudeDescription = this[82]
                    ATCindicator = this[83]
                    altitude1 = this[84:89]
                    altitude2 = this[89:94]
                    transitionAlt = this[94:99]
                    speedLimit = this[99:102]
                    # vertAnglecenterFix = this[106:111]
                    multipleCode = this[111]
                    centerFixICAO = this[112:114]
                    centerFixSection = this[114]
                    centerFixSubsection = this[115]
                    # GNSS nonsense = this[116]
                    speedLimitDescription = this[117]
                    typeQualifier1 = this[118]
                    typeQualifier2 = this[119]
                    typeQualifier3 = this[120]
                    preferred = this[121]

                elif subsection == 'E':
                    airportID = this[6:10]
                    airportICAOcode = this[10:12]
                    STAR_ID = this[13:19]
                    routeType = this[19]
                    transitionID = this[20:25]
                    aircraftCategory = this[25]
                    sequenceNumber = this[26:29]
                    fixID = this[29:34]
                    fixICAOid = this[34:36]
                    fixSecCode = this[36]
                    fixSubsecCode = this[37]
                    waypointDescripCode = this[39:43]
                    turnDirection = this[43]
                    reqNavPerformance = this[44:47]
                    pathAndTermination = this[47:49]
                    turnDirectionValid = this[49]
                    recommendedNavaid = this[50:54]
                    recNavaidICAOcode = this[54:56]
                    arcRadius = this[56:62]
                    theta = this[62:66]
                    # commenting out stuff that's not needed for MVP
                    # rho
                    # mag course
                    # routeDistance
                    # section
                    # subsection
                    # inboundOrOutbound
                    altitudeDescription = this[82]
                    ATCindicator = this[83]
                    altitude1 = this[84:89]
                    altitude2 = this[89:94]
                    transitionAlt = this[94:99]
                    speedLimit = this[99:102]
                    # vertAnglecenterFix = this[106:111]
                    multipleCode = this[111]
                    centerFixICAO = this[112:114]
                    centerFixSection = this[114]
                    centerFixSubsection = this[115]
                    # GNSS nonsense = this[116]
                    speedLimitDescription = this[117]
                    typeQualifier1 = this[118]
                    typeQualifier2 = this[119]
                    typeQualifier3 = this[120]
                    preferred = this[121]

                elif subsection == 'F':
                    airportID = this[6:10]
                    airportICAOcode = this[10:12]
                    approachID = this[13:19]
                    routeType = this[19]
                    transitionID = this[20:25]
                    aircraftCategory = this[25]
                    sequenceNumber = this[26:29]
                    fixID = this[29:34]
                    fixICAOid = this[34:36]
                    fixSecCode = this[36]
                    fixSubsecCode = this[37]
                    waypointDescripCode = this[39:43]
                    turnDirection = this[43]
                    reqNavPerformance = this[44:47]
                    pathAndTermination = this[47:49]
                    turnDirectionValid = this[49]
                    recommendedNavaid = this[50:54]
                    recNavaidICAOcode = this[54:56]
                    arcRadius = this[56:62]
                    theta = this[62:66]
                    # commenting out stuff that's not needed for MVP
                    # rho
                    # mag course
                    # routeDistance
                    # section
                    # subsection
                    # inboundOrOutbound
                    altitudeDescription = this[82]
                    ATCindicator = this[83]
                    altitude1 = this[84:89]
                    altitude2 = this[89:94]
                    transitionAlt = this[94:99]
                    speedLimit = this[99:102]
                    # vertAnglecenterFix = this[106:111]
                    multipleCode = this[111]
                    centerFixICAO = this[112:114]
                    centerFixSection = this[114]
                    centerFixSubsection = this[115]
                    # GNSS nonsense = this[116]
                    speedLimitDescription = this[117]
                    typeQualifier1 = this[118]
                    typeQualifier2 = this[119]
                    typeQualifier3 = this[120]
                    preferred = this[121]

                elif subsection == 'G':
                    airport = this[6:10]
                    airportICAO = this[10:11]
                    rwyIdent = this[13:20]
                    length = this[22:27]
                    bearing = this[27:31]
                    latitude = this[32:41]
                    longitude = this[41:51]
                    gradient = this[51:56]
                    # ellipsoid don't care
                    threshElev = this[66:71]
                    displacedThresh = this[71:75]
                    width = this[77:80]
                    TCHindicator = this[80]
                    stopway = this[86:90]
                    threshCrossHeight = this[95:98]
                    description = this[101:123]

                elif subsection == 'I':
                    airport = this[6:10]
                    airportICAOcode = this[10:11]
                    localizerIdent = this[13:17]
                    ILScategory = this[17]
                    frequence = this[22:27]
                    rwyIdent = this[27:32]
                    locLatitude = this[32:41]
                    locLongitude = this[41:51]
                    locBearing = this[51:55]
                    glideSlopeLat = this[55:64]
                    glideSlopeLong = this[64:74]
                    # distFromRwyEnd = this[74:78]
                    locPosition = this[78]
                    locWidth = this[83:87]
                    glideSlopeAngle = this[87:90]
                    stationDeclination = this[90:95]
                    glideSlopeElevation = this[97:102]
                    supportFac = this[102:106]
                    supportFacICAO = this[106:108]
                    supportFacSection = this[108]
                    supportFacSubsection = this[109]
                    glideSlopeTCH = this[110:113]

                elif subsection == 'N':
                    # This is all the same as DB--put them in the same function!
                    airport = this[6:10]
                    airportICAOcode = this[10:12]
                    navIdent = this[15:19]
                    ICAOCode = this[19:21]
                    vorFreq = this[22:27]
                    navaidClass = this[27:32]
                    navLat = this[32:41]
                    navLong = this[41:51]
                    datum = this[90:93]
                    magVar = this[74:79]
                    ndbName = this[93:123]

                    # lots of cursr.execute('') functions here
                elif subsection == 'P':
                    pass # going to skip these, they're only in Canada!

                elif subsection == 'S':
                    pass # this is all only in American Samoa! Skip for MVP.
                    # airpot = this[6:10]
                    # airportICAOcode = this[10:12]
                    # MSAcenter = this[13:18]
                    # MSA_ICAOcode = this[18:20]
                    # MSA_secCode = this[20]
                    # MSA_subsecCode = this[21]

        print('Got through the loop once!')
        print(this)
        break
        # if k == 10:
        #     conn.commit()
        #     k = 0

conn.close()









# extra lines for cleanliness
