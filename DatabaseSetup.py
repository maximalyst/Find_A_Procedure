from string import ascii_uppercase  # needed for A-Z string shortcut


# TODO: Add Helicopter things (none in MVP version of script)


def table_define(connection):
    # Constants, for cleanliness
    # Commented-out items may be added back in future versions
    KNOWN_AREACODES = [('CAN',), ('EEU',), ('LAM',), ('PAC',), ('SPA',),
                       ('USA',)]
    KNOWN_SECCODES = [('AS',), ('D_',), ('DB',), ('EA',), ('ER',),
                      ('HA',), ('HC',), ('HF',), ('HS',), ('PA',), ('PC',),
                      ('PD',), ('PE',), ('PF',), ('PG',), ('PI',), ('PN',),
                      ('PP',), ('PS',), ('UC',), ('UR',)]
    # Navaid classes include both VOR and NDB codes:
    # TODO: ADD AIR/HELIPORT LOCALIZER/MARKER MEANINGS FROM PI
    NAVAID_CLASS1 = [(' ',), ('V',), ('H',), ('S',), ('M',)]
    NAVAID_CLASS2 = [(' ',), ('D',), ('T',), ('M',), ('I',), ('N',), ('P',), ('O',), ('C',)]
    NAVAID_CLASS3 = [(' ',), ('T',), ('L',), ('H',), ('U',), ('C',), ('M',)]
    NAVAID_CLASS4 = [(' ',), ('D',), ('A',), ('B',), ('W',)]
    NAVAID_CLASS5 = [(' ',), ('N',), ('B',)]
    # ROUTE_TYPES_ER = [('A',),('C',),('D',),('H',),('O',),('R',),('S',),('T',)]
    # ROUTE_TYPES_RTE_QUAL1 = [('G',),('F',),('A',),('U',)]
    # ROUTE_TYPES_RTE_QUAL2 = [('R',),('P',),('T',)]
    # ROUTE_TYPES_RTE_QUAL3 = [('W',),('Z',),('Y',),('X',),('B',),('P',),('C',),('D',),
    #     ('E',),('A',),('G',),('U',),('V',),('N',)]
    ROUTE_TYPES_SIDS = [(' ',), ('0',), ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('F',),
                        ('M',), ('S',), ('T',), ('V',)]
    ROUTE_TYPES_SIDQUAL1 = [(' ',), ('D',), ('G',), ('R',), ('H',), ('P',)]
    ROUTE_TYPES_SIDQUAL2 = [(' ',), ('D',), ('E',), ('F',), ('G',), ('W',), ('X',)]
    ROUTE_TYPES_SIDQUAL3 = [(' ',), ('Z',), ('Y',), ('X',), ('B',), ('P',), ('D',),
                            ('E',), ('F',), ('A',), ('G',), ('M',), ('U',), ('V',)]
    # Note: No ROUTE_TYPES_STAR because they are just [1,2,3]
    # Fun use of Python >3.5 iterables & * operator below...
    ROUTE_TYPES_STARQUAL1 = [*[(' ',)], *[(str(i),) for i in range(1, 10)], *[('F',), ('M',), ('S',)]]
    ROUTE_TYPES_STARQUAL2 = ROUTE_TYPES_SIDQUAL2[:-2]
    ROUTE_TYPES_STARQUAL3 = ROUTE_TYPES_SIDQUAL3
    ROUTE_TYPES_APPCH = [(' ',), ('A',), ('B',), ('D',), ('F',), ('G',), ('H',),
                         ('I',), ('J',), ('L',),
                         ('M',), ('N',), ('P',), ('Q',), ('R',), ('S',),
                         ('T',), ('U',), ('V',), ('X',), ('Z',)]
    ROUTE_TYPES_APPCH_QUAL1 = [(' ',), ('D',), ('J',), ('N',), ('P',), ('R',),
                               ('T',), ('U',), ('V',), ('W',)]
    ROUTE_TYPES_APPCH_QUAL2 = [(' ',), ('A',), ('B',), ('E',), ('C',), ('H',), ('I',),
                               ('L',), ('S',), ('V',), ('W',), ('X',)]
    ROUTE_TYPES_APPCH_QUAL3 = [(' ',), ('X',), ('E',), ('H',), ('G',), ('A',), ('F',), ('B',)]
    ILS_CATS = [(' ',), ('0',), ('1',), ('2',), ('3',), ('I',), ('L',), ('A',), ('S',),
                ('F',)]
    WAYPOINT_TYPE1 = [(' ',), ('A',), ('C',), ('I',), ('M',), ('N',), ('O',), ('R',), ('U',), ('V',), ('W',)]
    WAYPOINT_TYPE2 = [(' ',), ('A',), ('B',), ('C',), ('D',), ('F',), ('G',), ('H',), ('I',), ('J',), ('K',),
                      ('L',), ('M',), ('N',), ('O',), ('P',), ('R',), ('S',), ('U',), ('V',), ('W',)]
    WAYPOINT_TYPE3 = [(' ',), ('D',), ('E',), ('F',), ('Z',), ('G',)]
    SSA_DESCRIP1 = [(' ',), ('A',), ('E',), ('F',), ('G',), ('H',), ('N',), ('P',), ('R',), ('T',), ('V',)]
    SSA_DESCRIP2 = [(' ',), ('B',), ('E',), ('U',), ('Y',)]
    SSA_DESCRIP3 = [(' ',), ('A',), ('B',), ('C',), ('G',), ('M',), ('R',), ('S',)]
    SSA_DESCRIP4 = [(' ',), ('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',),
                    ('H',), ('I',), ('M',), ('N',), ('P',)]
    # Found the following in testing, and not sure what is up--not in ARINC spec
    SSA_DESCRIP1 = SSA_DESCRIP1 + [('W',)]
    SSA_DESCRIP2 = SSA_DESCRIP2 + [('A',)]
    SSA_DESCRIP3 = SSA_DESCRIP3 + [('L',)]
    ROUTE_TYPES_APPCH_QUAL1 = ROUTE_TYPES_APPCH_QUAL1 + [('F',)]

    REMOTE_ALT_FLAG = [(' ',), ('R',)]
    TIME_ZONES = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K',
                  'L', 'M', '1', '2', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y']

    # PATH_TYPES = [('AF',),('CA',),('CD',),('CF',),('CI',),('CR',),('DF',),('FA',),('FC',),('FD',),
    #               ('FM',),('HA',),('HF',),('HM',),('IF',),('PI',),('RF',),('TF',),('VA',),('VD',),
    #               ('VI',),('VM',),('VR',)]
    ICAO_CODES = [('  ',), ('K1',), ('K2',), ('K3',), ('K4',), ('K5',),
                  ('K6',), ('K7',), ('K ',), ('AG',), ('AN',), ('CY',), ('CZ',),
                  ('PA',), ('PH',), ('AY',), ('BG',), ('BI',), ('BK',),
                  ('DA',), ('DB',), ('DF',), ('DG',), ('DI',),
                  ('DN',), ('DR',), ('DT',), ('DX',), ('EB',), ('ED',),
                  ('EE',), ('EF',), ('EG',), ('EH',), ('EI',), ('EK',),
                  ('EL',), ('EN',), ('EP',), ('ES',), ('ET',), ('EV',),
                  ('EY',), ('FA',), ('FB',), ('FC',), ('FD',), ('FE',),
                  ('FG',), ('FH',), ('FI',), ('FJ',), ('FK',), ('FL',),
                  ('FM',), ('FN',), ('FO',), ('FP',), ('FQ',), ('FS',),
                  ('FT',), ('FV',), ('FW',), ('FX',), ('FY',), ('FZ',),
                  ('GA',), ('GB',), ('GC',), ('GE',), ('GF',), ('GG',),
                  ('GL',), ('GM',), ('GO',), ('GQ',), ('GS',), ('GU',),
                  ('GV',), ('HA',), ('HB',), ('HC',), ('HD',), ('HE',),
                  ('HH',), ('HK',), ('HL',), ('HR',), ('HS',), ('HT',),
                  ('HU',), ('LA',), ('LB',), ('LC',), ('LD',),
                  ('LE',), ('LF',), ('LG',), ('LH',), ('LI',), ('LJ',),
                  ('LK',), ('LL',), ('LM',), ('LN',), ('LO',), ('LP',),
                  ('LQ',), ('LR',), ('LS',), ('LT',), ('LU',), ('LV',),
                  ('LW',), ('LX',), ('LY',), ('LZ',), ('MB',), ('MD',),
                  ('MG',), ('MH',), ('MK',), ('MM',), ('MN',), ('MP',),
                  ('MR',), ('MS',), ('MT',), ('MU',), ('MW',), ('MY',),
                  ('MZ',), ('NC',), ('NF',), ('NG',), ('NI',), ('NL',),
                  ('NS',), ('NT',), ('NV',), ('NW',), ('NZ',), ('OA',),
                  ('OB',), ('OE',), ('OI',), ('OJ',), ('OK',), ('OL',),
                  ('OM',), ('OO',), ('OP',), ('OR',), ('OS',), ('OT',),
                  ('OY',), ('PB',), ('PC',), ('PF',), ('PG',),
                  ('PJ',), ('PK',), ('PL',), ('PM',), ('PO',),
                  ('PP',), ('PT',), ('PW',), ('P ',), ('RC',), ('RJ',), ('RK',),
                  ('RO',), ('RP',), ('SA',), ('SB',), ('SC',), ('SD',),
                  ('SE',), ('SF',), ('SG',), ('SH',), ('SI',), ('SJ',),
                  ('SK',), ('SL',), ('SM',), ('SN',), ('SO',), ('SP',),
                  ('SS',), ('SU',), ('SV',), ('SW',), ('SY',), ('TA',),
                  ('TB',), ('TD',), ('TF',), ('TG',), ('TI',), ('TJ',),
                  ('TK',), ('TL',), ('TN',), ('TQ',), ('TR',), ('TT',),
                  ('TU',), ('TV',), ('TX',), ('UA',), ('UB',), ('UC',),
                  ('UD',), ('UE',), ('UG',), ('UH',), ('UI',), ('UK',),
                  ('UL',), ('UM',), ('UN',), ('UO',), ('UT',), ('UR',),
                  ('US',), ('UU',), ('UW',),
                  ('VA',), ('VC',), ('VD',), ('VE',), ('VG',), ('VH',),
                  ('VI',), ('VL',), ('VM',), ('VN',), ('VO',), ('VQ',),
                  ('VR',), ('VT',), ('VV',), ('VY',), ('WA',), ('WB',),
                  ('WI',), ('WM',), ('WP',), ('WQ',), ('WR',), ('WS',),
                  ('Y',), ('Z',), ('ZK',), ('ZM',)]

    c = connection.cursor()
    # TODO: Fix navaid uniqueness for NDB's
    c.executescript('''
    --VHF navaids
    CREATE TABLE D_ (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        navaid_id INTEGER,
        navaidGeoIcao_id INTEGER,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id INTEGER,
        latitude    TEXT,
        longitude   TEXT,
        featureName TEXT,
        navaidFrequency INTEGER,
        navaidClass1_id INTEGER,
        navaidClass2_id INTEGER,
        navaidClass3_id INTEGER,
        navaidClass4_id INTEGER,
        navaidClass5_id INTEGER,
        DMEident_id  INTEGER,
        DMElatitude  TEXT,
        DMElongitude TEXT,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    -- NDB navaids
    CREATE TABLE DB (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        navaid_id INTEGER,
        navaidGeoIcao_id INTEGER,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id INTEGER,
        latitude    TEXT,
        longitude   TEXT,
        featureName TEXT,
        navaidFrequency INTEGER,
        navaidClass1_id INTEGER,
        navaidClass2_id INTEGER,
        navaidClass3_id INTEGER,
        navaidClass4_id INTEGER,
        navaidClass5_id INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        DB_or_PN_id    INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --Terminal NDB navaids--copy above table fields
    --CREATE TABLE PN (
    --    id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
    --    navaid_id TEXT UNIQUE,
    --    navaidGeoIcao_id INTEGER,
    --    airHeli_portIdent_id INTEGER,
    --    airHeli_GeoIcao_id INTEGER,
    --    latitude    TEXT,
    --    longitude   TEXT,
    --    featureName TEXT,
    --    navaidFrequency INTEGER,
    --    navaidClass1_id INTEGER,
    --    navaidClass2_id INTEGER,
    --    navaidClass3_id INTEGER,
    --    navaidClass4_id INTEGER,
    --    navaidClass5_id INTEGER,
    --    areaCode_id INTEGER,
    --    sectionCode_id INTEGER,
    --    --subsectionCode_id INTEGER,
    --    file_rec        INTEGER,
    --    cycle_date      INTEGER
    --);
    --enroute waypoints
    CREATE TABLE EA (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        waypointIdent TEXT UNIQUE,
        waypointIcao_id  INTEGER,
        waypointType1_id INTEGER,
        waypointType2_id INTEGER,
        waypointType3_id INTEGER,
        waypointusage_id INTEGER,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        latitude        TEXT,
        longitude       TEXT,
        featureName     TEXT,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --enroute airways
    CREATE TABLE ER (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        routeIdent     TEXT UNIQUE,
        sequenceNumber INTEGER,
        fixIdent_id    INTEGER,
        fixIcao_id     INTEGER,
        fixSectionCode_id    INTEGER,
        --fixSubsectionCode_id INTEGER,
        waypointDescription1_id   INTEGER,
        waypointDescription2_id   INTEGER,
        waypointDescription3_id   INTEGER,
        waypointDescription4_id   INTEGER,
        recommendedNavaid_id INTEGER,
        recommendedNavaidGeoIcao_id INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --airport ref points
    CREATE TABLE PA (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent    TEXT UNIQUE,
        airHeli_GeoIcao_id   INTEGER,
        latitude        TEXT,
        longitude       TEXT,
        featureName     TEXT,
        IATAcode_id     INTEGER,
        speedLimitAltitude TEXT,
        --longestRunway TEXT,
        --longestSurface INTEGER,
        hasIFR_id       INTEGER,
        magneticVariation TEXT,
        elevation       TEXT,
        speedLimit      INTEGER,
        recommendedNavaid_id INTEGER,
        recommendedNavaidGeoIcao_id INTEGER,
        publicOrMilitary_id INTEGER,
        timeZone        TEXT,
        DST_id          INTEGER,
        --magOrTrue_id  INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --Airport terminal waypoints -- these are the same as EA
    --CREATE TABLE PC (
    --    id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
    --    airHeli_portIdent_id INTEGER,
    --    airHeli_GeoIcao_id INTEGER,
    --    latitude        TEXT,
    --    longitude       TEXT,
    --    featureName     TEXT,
    --    waypointIdent_id INTEGER,
    --    waypointIcao_id  INTEGER,
    --    waypointType1_id INTEGER,
    --    waypointType2_id INTEGER,
    --    waypointType3_id INTEGER,
    --    waypointUsage_id INTEGER,
    --    areaCode_id     INTEGER,
    --    sectionCode_id  INTEGER,
    --    --subsectionCode_id INTEGER,
    --    file_rec        INTEGER,
    --    cycle_date      INTEGER
    --);
    --SIDs
    CREATE TABLE PD (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        fixIdent_id TEXT, --CHANGE back to INTEGER if this becomes a reference again
        fixIcao_id  INTEGER,
        fixSectionCode_id    INTEGER,
        --fixSubsectionCode_id INTEGER,
        descriptionCode1_id   INTEGER,
        descriptionCode2_id   INTEGER,
        descriptionCode3_id   INTEGER,
        descriptionCode4_id   INTEGER,
        recommendedNavaid_id INTEGER,
        recommendedNavaidGeoIcao_id INTEGER,
        SidStarApproachIdent  TEXT UNIQUE,
        routeTypeSID_id          INTEGER,
        transitionIdent    TEXT,
        aircraftDesignType_id INTEGER,
        sequenceNumber INTEGER,
        speedLimit     INTEGER,
        speedLimitDescription_id INTEGER,
        routeQual1_id INTEGER,
        routeQual2_id INTEGER,
        routeQual3_id INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --STARs
    CREATE TABLE PE (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        fixIdent_id INTEGER,
        fixIcao_id  INTEGER,
        fixSectionCode_id    INTEGER,
        fixSubsectionCode_id INTEGER,
        descriptionCode1_id   INTEGER,
        descriptionCode2_id   INTEGER,
        descriptionCode3_id   INTEGER,
        descriptionCode4_id   INTEGER,
        recommendedNavaid_id INTEGER,
        recommendedNavaidGeoIcao_id INTEGER,
        SidStarApproachIdent  TEXT UNIQUE,
        routeTypeSTAR         INTEGER,--1,2,or 3; so we do it direct
        transitionIdent    TEXT,
        aircraftDesignType_id INTEGER,
        sequenceNumber INTEGER,
        speedLimit     INTEGER,
        speedLimitDescription_id INTEGER,
        routeQual1_id INTEGER,
        routeQual2_id INTEGER,
        routeQual3_id INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --Approach records
    CREATE TABLE PF (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        fixIdent_id INTEGER,
        fixIcao_id  INTEGER,
        fixSectionCode_id    INTEGER,
        fixSubsectionCode_id INTEGER,
        descriptionCode1_id   INTEGER,
        descriptionCode2_id   INTEGER,
        descriptionCode3_id   INTEGER,
        descriptionCode4_id   INTEGER,
        recommendedNavaid_id INTEGER,
        recommendedNavaidGeoIcao_id INTEGER,
        SidStarApproachIdent  TEXT UNIQUE,
        routeTypeApproach_id     INTEGER,
        transitionIdent    TEXT,
        aircraftDesignType_id INTEGER,
        sequenceNumber INTEGER,
        speedLimit     INTEGER,
        speedLimitDescription_id INTEGER,
        routeQual1_id INTEGER,
        routeQual2_id INTEGER,
        routeQual3_id INTEGER,
        LVnavLevelOfService TEXT,
        LnavLevelOfService  TEXT,
        remoteAltimeterFlag_id   INTEGER,
        LVnavAuth_id  INTEGER,
        LnavAuth_id   INTEGER,
        RNPAuth1_id   INTEGER,
        RNPAuth2_id   INTEGER,
        RNPAuth3_id   INTEGER,
        RNPAuth4_id   INTEGER,
        RNPLevelOfService1   INTEGER,
        RNPLevelOfService2   INTEGER,
        RNPLevelOfService3   INTEGER,
        RNPLevelOfService4   INTEGER,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --airport runways
    CREATE TABLE PG (
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        latitude        TEXT,
        longitude       TEXT,
        runwayIdent     TEXT,
        runwayLength    INTEGER,
        runwayBearing   TEXT,
        runwayGradient  TEXT,
        landingThresholdElev    TEXT,
        displacedTresholdLength INTEGER,
        runwayWidth     INTEGER,
        TCHvalueIndicator TEXT,
        stopwayLength   INTEGER,
        thresholdCrossingHeight TEXT,
        runwayDescrip   TEXT,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER,
        PRIMARY KEY (airHeli_portIdent_id, runwayIdent)
    );
    --Airport/Heliport Localizer/Glideslopes
    CREATE TABLE PI (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id INTEGER,
        latitude        TEXT,
        longitude       TEXT,
        navaid_id  INTEGER,
        ILScategory_id  INTEGER,
        localizerFreq   INTEGER,
        runwayIdent     TEXT,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
    );
    --Airport SBAS Path Points (WAAS)
    CREATE TABLE PP (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        areaCode_id       INTEGER,
        sectionCode_id    INTEGER,
        --subsectionCode_id INTEGER,
        file_rec          INTEGER,
        cycle_date        INTEGER
        -- I really dont give AF about these in MVP
    );
    --airport MSAs:
    CREATE TABLE PS (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        airHeli_portIdent_id INTEGER,
        airHeli_GeoIcao_id   INTEGER,
        areaCode_id       INTEGER,
        sectionCode_id    INTEGER,
        --subsectionCode_id INTEGER,
        file_rec          INTEGER,
        cycle_date        INTEGER
        -- I really dont give AF about these in MVP
        --MSAcenter      TEXT,
        --MSAcenter_ICAO_id   INTEGER,
        --MSAcenter_SecCode_id    INTEGER,
        --MSAcenter_SubSecCode_id INTEGER,
        --multipleCode    TEXT,
        --magOrTrue_id    INTEGER,
        --SectorBearing_1     INTEGER,
        --SectorAltitude_1    INTEGER,
        --SectorRadius_1      INTEGER,
        --SectorBearing_2     INTEGER,
        --SectorAltitude_2    INTEGER,
        --SectorRadius_2      INTEGER,
        --SectorBearing_3     INTEGER,
        --SectorAltitude_3    INTEGER,
        --SectorRadius_3      INTEGER,
        --SectorBearing_4     INTEGER,
        --SectorAltitude_4    INTEGER,
        --SectorRadius_4      INTEGER,
        --SectorBearing_5     INTEGER,
        --SectorAltitude_5    INTEGER,
        --SectorRadius_5      INTEGER,
        --SectorBearing_6     INTEGER,
        --SectorAltitude_6    INTEGER,
        --SectorRadius_6      INTEGER,
        --SectorBearing_7     INTEGER,
        --SectorAltitude_7    INTEGER,
        --SectorRadius_7      INTEGER,
    );
    CREATE TABLE UC (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
        -- I really dont give AF about these in MVP
    );
    CREATE TABLE UR (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        latitude    TEXT,
        longitude   TEXT,
        featureName TEXT,
        areaCode_id     INTEGER,
        sectionCode_id  INTEGER,
        --subsectionCode_id INTEGER,
        file_rec        INTEGER,
        cycle_date      INTEGER
        -- I really dont give AF about these in MVP
    );
    ''')
    c.executescript('''
    --The following are consistent items in many entries:
    CREATE TABLE navaid (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        ident   TEXT UNIQUE
    );
    CREATE TABLE IcaoCode (--2 letter codes
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        code    TEXT UNIQUE
    );
    CREATE TABLE AreaCode (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        area    TEXT UNIQUE
    );
    CREATE TABLE SecCode (
        --id INTEGER UNIQUE,
        section TEXT NOT NULL,
        subsec  TEXT NOT NULL,
        PRIMARY KEY (section, subsec)
    );
    CREATE TABLE DMEident (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name    TEXT UNIQUE
    );
    CREATE TABLE fixIdent (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name    TEXT UNIQUE
    );
    --  This one is a repeat of IcaoCode
    --CREATE TABLE GeoIcao (
    --    id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
    --    code    TEXT
    --);
    CREATE TABLE NAVAIDclass1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        class   TEXT UNIQUE
    );
    CREATE TABLE NAVAIDclass2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        class   TEXT UNIQUE
    );
    CREATE TABLE NAVAIDclass3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        class   TEXT UNIQUE
    );
    CREATE TABLE NAVAIDclass4 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        class   TEXT UNIQUE
    );
    CREATE TABLE NAVAIDclass5 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        class   TEXT UNIQUE
    );
    CREATE TABLE WaypointType1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    CREATE TABLE WaypointType2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    CREATE TABLE WaypointType3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    CREATE TABLE WaypointUsage (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        usage   TEXT UNIQUE
    );
    CREATE TABLE RouteIdent (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name    TEXT UNIQUE
    );
    CREATE TABLE waypointDescription1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        desc    TEXT UNIQUE
    );
    CREATE TABLE waypointDescription2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        desc    TEXT UNIQUE
    );
    CREATE TABLE waypointDescription3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        desc    TEXT UNIQUE
    );
    CREATE TABLE waypointDescription4 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        desc    TEXT UNIQUE
    );
    CREATE TABLE IATAcode ( --created with table PA
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        code    TEXT UNIQUE
    );
    CREATE TABLE hasIFR (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );
    CREATE TABLE publicOrMilitary (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );
    CREATE TABLE DST (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );
    CREATE TABLE routeTypeSID (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    --Don't do "routeTypeSTAR" because routeType for STAR is 1, 2, and 3,
    --so we do the value directly in the PE table
    CREATE TABLE routeTypeApproach (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    CREATE TABLE routeSIDQual1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeSIDQual2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeSIDQual3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeSTARQual1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeSTARQual2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeSTARQual3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeAppchQual1 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeAppchQual2 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE routeAppchQual3 (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        qual    TEXT UNIQUE
    );
    CREATE TABLE speedLimitDescription (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        descrip TEXT UNIQUE
    );
    CREATE TABLE ILScategory (
        id       INTEGER NOT NULL PRIMARY KEY UNIQUE,
        category TEXT UNIQUE
    );
    CREATE TABLE aircraftDesignType (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        type    TEXT UNIQUE
    );
    CREATE TABLE remoteAltimeterFlag (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );
    CREATE TABLE RNAVAuthorized (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );
    CREATE TABLE DB_or_PN (
        id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
        flag    TEXT UNIQUE
    );



    --Old things I'm not ready to delete yet
    --CREATE TABLE transitionIdent (
    --    id      INTEGER NOT NULL PRIMARY KEY UNIQUE,
    --    type    TEXT UNIQUE
    --);
    ''')

    # TODO: change routeTypeSID to include all SID/STAR/Appch types (add approaches)

    c.executemany('''INSERT INTO AreaCode (area) VALUES (?);''',
                  KNOWN_AREACODES)
    for each in KNOWN_SECCODES:
        c.execute('''INSERT INTO SecCode (section,subsec) VALUES (?,?);''',
                  (each[0][0], each[0][1]))
    c.executemany('''INSERT INTO NAVAIDclass1 (class) VALUES (?);''', NAVAID_CLASS1)
    c.executemany('''INSERT INTO NAVAIDclass2 (class) VALUES (?);''', NAVAID_CLASS2)
    c.executemany('''INSERT INTO NAVAIDclass3 (class) VALUES (?);''', NAVAID_CLASS3)
    c.executemany('''INSERT INTO NAVAIDclass4 (class) VALUES (?);''', NAVAID_CLASS4)
    c.executemany('''INSERT INTO NAVAIDclass5 (class) VALUES (?);''', NAVAID_CLASS5)
    c.executemany('''INSERT INTO WaypointType1 (type) VALUES (?);''', WAYPOINT_TYPE1)
    c.executemany('''INSERT INTO WaypointType2 (type) VALUES (?);''', WAYPOINT_TYPE2)
    c.executemany('''INSERT INTO WaypointType3 (type) VALUES (?);''', WAYPOINT_TYPE3)
    c.executemany('''INSERT INTO WaypointUsage (usage) VALUES (?)''', [' ', 'B', 'H', 'L'])
    c.executemany('''INSERT INTO aircraftDesignType (type) VALUES (?);''',
                  [each for each in (list(ascii_uppercase)[:-1] + [' '])])
    c.executemany('''INSERT INTO waypointDescription1 (desc) VALUES (?);''',
                  SSA_DESCRIP1)
    c.executemany('''INSERT INTO waypointDescription2 (desc) VALUES (?);''',
                  SSA_DESCRIP2)
    c.executemany('''INSERT INTO waypointDescription3 (desc) VALUES (?);''',
                  SSA_DESCRIP3)
    c.executemany('''INSERT INTO waypointDescription4 (desc) VALUES (?);''',
                  SSA_DESCRIP4)
    c.executemany('''INSERT INTO hasIFR (flag) VALUES (?);''',
                  [('N',), ('Y',)])
    c.executemany('''INSERT INTO publicOrMilitary (flag) VALUES (?);''',
                  [('C',), ('M',), ('P',), ('J',)])
    c.executemany('''INSERT INTO DST (flag) VALUES (?);''',
                  [('N',), ('Y',), (' ',)])  # 1 for No, 2 for Yes, allow for blank
    c.executemany('''INSERT INTO routeTypeSID (type) VALUES (?);''',
                  ROUTE_TYPES_SIDS)
    c.executemany('''INSERT INTO routeTypeApproach (type) VALUES (?);''',
                  ROUTE_TYPES_APPCH)
    c.executemany('''INSERT INTO routeSIDQual1 (qual) VALUES (?);''',
                  ROUTE_TYPES_SIDQUAL1)
    c.executemany('''INSERT INTO routeSIDQual2 (qual) VALUES (?);''',
                  ROUTE_TYPES_SIDQUAL2)
    c.executemany('''INSERT INTO routeSIDQual3 (qual) VALUES (?);''',
                  ROUTE_TYPES_SIDQUAL3)
    c.executemany('''INSERT INTO routeSTARQual1 (qual) VALUES (?);''',
                  ROUTE_TYPES_STARQUAL1)
    c.executemany('''INSERT INTO routeSTARQual2 (qual) VALUES (?);''',
                  ROUTE_TYPES_STARQUAL2)
    c.executemany('''INSERT INTO routeSTARQual3 (qual) VALUES (?);''',
                  ROUTE_TYPES_STARQUAL3)
    c.executemany('''INSERT INTO routeAppchQual1 (qual) VALUES (?);''',
                  ROUTE_TYPES_APPCH_QUAL1)
    c.executemany('''INSERT INTO routeAppchQual2 (qual) VALUES (?);''',
                  ROUTE_TYPES_APPCH_QUAL2)
    c.executemany('''INSERT INTO routeAppchQual3 (qual) VALUES (?);''',
                  ROUTE_TYPES_APPCH_QUAL3)
    c.executemany(
        '''INSERT INTO speedLimitDescription (descrip) VALUES (?);''',
        [(' ',), ('+',), ('-',)])
    c.executemany('''INSERT INTO ILScategory (category) VALUES (?);''',
                  ILS_CATS)
    c.executemany('''INSERT INTO IcaoCode (code) VALUES (?)''',
                  ICAO_CODES)
    c.executemany('''INSERT INTO remoteAltimeterFlag (flag) VALUES (?)''',
                  REMOTE_ALT_FLAG)
    c.executemany('''INSERT INTO RNAVAuthorized (flag) VALUES (?)''',
                  [('N',), ('A',), (' ',)])
    c.executemany('''INSERT INTO DB_or_PN (flag) VALUES (?)''',
                  [('DB',), ('PN',)])

    # Default blank/null values for certain tables...
    c.execute('INSERT INTO navaid (ident) VALUES (?)', ('    ', ))

    # old things that I might come back to
    # c.executemany('''INSERT INTO ATCindicator (flag) VALUES (?);''', [('A',),('S',)])
    # c.executemany('''INSERT INTO SpeedLimitDescription (code) VALUES (?);''', [(' ',),('+',),('-',)])
    # c.executemany('''INSERT INTO procedureTurnFlag (flag) VALUES (?);''', [('N',),('Y',)]) #0 for no, 1 for yes
    # c.executemany('''INSERT INTO AirspaceTypes (type) VALUES (?);''', [('A',),('C',),('M',),('R',),('T',),('Z',)])
    # c.executemany('''INSERT INTO AirspaceClassifications (class) VALUES (?);''', [('A',),('B',),('C',),('D',),('E',),('G',),('',)])
    # c.executemany('''INSERT INTO waypointUsage (code) VALUES (?);''', [('B',),('H',),('L',),(' ',)])

    connection.commit()
