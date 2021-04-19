# This is going to be where the cursr.execute() functions go

# class RecordString:
#     def __init__(self,line):
#         self.line = line
#         self.recordType = line[0]
#         self.areaCode = line[1:4]
#         self.section = line[4]
#         self.fileRecord = line[123:128]
#         self.fileCycle = line[128:]
#
#         if self.section != 'P' and (self.section != 'H'):
#             self.subsection = line[5]
#         else: self.subsection = line[12]
#
#
""" Flow through each loop of CFIP data:
    Read line
    Remove trailing \n and force upper case
    ^^^ Did the above in the loop itself

    Set "standard" features--line[0],]1:4],[123:128],[128:]
    Set section--line[4]
    Determine if it's section P/H or not
        If it is, get subsection -- line[12]
        If it isn't, get subsection -- line[5]

    Depending on section/subsection, input data into database
        Get "standard" features from each section--line[xx:yy]
        Input repeated data (ex. airport abbrevs) into ID tables
        Reference ID tables into line's database entry
        Input unique data (ex. lat/long) into line's database entry
"""


# 'l' is the line of the CIFP we're looking at.

# Naming convention: my functions are going to be prefaced with 'r'

class CIFPLine:
    def __init__(self, data, connection):
        self.data = data
        self.connection = connection
        self.c = self.connection.cursor()
        self.recordType = self.data[0]
        self.areaCode = self.data[1:4]
        self.section = self.data[4]
        self.fileRecord = self.data[123:128]
        self.fileCycle = self.data[128:]

        if self.section not in ['P', 'H']:
            if self.data[5] == ' ':
                self.data[5] = '_'  # covers D_ (VHF navaid) case
                self.subsection = self.data[5]
        else:
            self.subsection = self.data[12]

        self.table_name = self.section + self.subsection

        if self.table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PD',
                               'PE', 'PF',
                               'HD', 'HE', 'HF', 'PG', 'PI', 'PP', 'PS', 'HS']:
            self.airHeli_portIdent = self.data[6:10]
            self.airHeli_GeoIcao = self.data[10:12]

        if self.table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PG',
                               'PI', 'UR',
                               'UC']:
            self.latitude = self.data[32:41]
            self.longitude = self.data[41:51]

        if self.table_name in ['D_', 'DB', 'PN', 'PA', 'HA', 'UR', 'UC', 'EA',
                               'PC',
                               'HC']:
            if self.table_name == 'D_':
                self.featureName = self.data[93:118]
            elif self.table_name in ['EA', 'PC', 'HC']:
                self.featureName = self.data[98:123]
            else:
                self.featureName = self.data[93:123]

        if self.table_name in ['D_', 'DB', 'PN']:
            self.navaidIdent = self.data[13:17]
            self.navaidGeoIcao = self.data[19:21]
            self.navaidFrequency = self.data[22:27]
            self.navaidClass = self.data[27:32]
            if self.table_name == 'D_':
                self.DMEident = self.data[51:55]
                self.DMElatitude = self.data[55:64]
                self.DMElongitude = self.data[64:74]

        if self.table_name in ['PA', 'HA']:
            self.IATAcode = self.data[13:16]
            self.speedLimitAltitude = self.data[22:27]
            self.hasIFR = self.data[30]
            self.magneticVariation = self.data[51:56]
            self.elevation = self.data[56:61]
            self.speedLimit = self.data[61:64]
            self.recommendedNavaid = self.data[64:68]
            self.recommendedNavaidGeoIcao = self.data[68:70]
            self.publicOrMilitary = self.data[80]
            self.timeZone = self.data[81:84]
            self.DST = self.data[84]
            if self.table_name == 'PA':
                self.longestRunway = self.data[27:30]
                self.longRunwaySurface = self.data[31]
            else:
                self.heliportType = self.data[31]

        if self.table_name in ['ER', 'PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
            self.fixIdent = self.data[29:34]
            self.fixIcao = self.data[34:36]
            self.fixSectionCode = self.data[36]
            self.fixSubsectionCode = self.data[37]
            self.descriptionCode = self.data[39:43]
            self.recommendedNavaid = self.data[50:54]
            self.recommendedNavaidGeoIcao = self.data[54:56]
            if self.table_name in ['PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
                self.SidStarApproachIdent = self.data[13:19]
                self.routeType = self.data[20]
                self.transitionIdent = self.data[20:25]
                self.aircraftDesignTypes = self.data[25]
                self.sequenceNumber = self.data[26:29]
                self.speedLimit = self.data[99:102]
                self.speedLimitDescription = self.data[117]
                self.routeQual1 = self.data[118]
                self.routeQual2 = self.data[119]
                self.routeQual3 = self.data[120]
            else:
                self.routeIdent = self.data[13:18]
                self.sequenceNumber = self.data[25:29]

        if self.table_name in ['EA', 'PC', 'HC']:
            self.waypointIdent = self.data[13:18]
            self.waypointIcao = self.data[19:21]
            self.waypointType1 = self.data[26]
            self.waypointType2 = self.data[27]
            self.waypointType3 = self.data[28]
            self.waypointusage = self.data[30]

        if self.table_name == 'PG':
            self.runwayIdent = self.data[13:18]
            self.runwayLength = self.data[22:27]
            self.runwayBearing = self.data[27:31]
            self.runwayGradient = self.data[51:56]
            self.landingThresholdElev = self.data[66:71]
            self.displacedTresholdLength = self.data[71:75]
            self.runwayWidth = self.data[7780]
            self.TCHvalueIndicator = self.data[80]
            self.stopwayLength = self.data[86:90]
            self.thresholdCrossingHeight = self.data[95:98]
            self.runwayDescrip = self.data[101:123]

        if self.table_name == 'PI':
            self.localizerIdent = self.data[13:17]
            self.ILScategory = self.data[17]
            self.localizerFreq = self.data[22:27]
            self.runwayIdent = self.data[27:32]

    # def AS(self, connection):  # Grid MORA
    #     c = connection.cursor()

    def D_(self):  # VHF navaid
        self.c.execute('''INSERT OR IGNORE INTO D_ (
                                     latitude,
                                     longitude,
                                     featureName,
                                     navaidIdent,
                                     DMElatitude,
                                     DMElongitude) 
                           VALUES (?, ?, ?, ?, ?, ?)''',
                       [(self.latitude,), (self.longitude,),
                        (self.featureName,), (self.navaidIdent,),
                        (self.DMElatitude,), (self.DMElongitude,)])

    def DB(self):  # NDB navaid
        pass

    def EA(self, connection):  # Enroute Waypoint
        pass

    def ER(self, connection):  # Enroute Airway/Route
        pass

    def HA(self, connection):  # Heliport reference point
        pass

    def HC(self, connection):  # Heliport terminal waypoint
        pass

    def HF(self, connection):  # Heliport approach procedure
        pass

    def HS(self, connection):  # Heliport MSA
        pass

    def PA(self, connection):  # Airport reference point
        pass

    def PC(self, connection):  # Airport terminal waypoint
        pass

    def PD(self, connection):  # Airport SID
        pass

    def PE(self, connection):  # Airport STAR
        pass

    def PF(self, connection):  # Airport Approach
        pass

    def PG(self, connection):  # Airport Runway
        pass

    def PI(self, connection):  # Airport Localizer/Glideslope
        pass

    def PN(self, connection):  # Airport Terminal NDB
        pass

    def PP(self, connection):  # Airport SBAS Path Point
        pass

    def PS(self, connection):  # Airport MSA
        pass

    def UC(self, connection):  # Controlled airspace
        pass

    def UR(self, connection):  # Restrictive airspace
        pass
