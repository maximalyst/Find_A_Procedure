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
''' Flow through each loop of CFIP data:
    Read line
    Remove trailing \n and force upper case
    ^^^ Did the above in the loop itself

    Set "standard" features--line[0],]1:4],[123:128],[128:]
    Set section--line[4]
    Determine if it's section P/H or not
        If it is, get subsection -- line[12]
        If it isn't, get subsection -- line[5]

    Depending on sectionsubsection, input data into databse
        Get "standard" features from each section--line[xx:yy]
        Input repeated data (ex. airport abbrevs) into ID tables
        Reference ID tables into line's database entry
        Input unique data (ex. lat/long) into line's database entry
'''

# 'l' is the line of the CFIP we're looking at.

# Naming convention: my functions are going to be prefaced with 'r'


def Parse_CFIP_Line(l):
    recordType = l[0]
    areaCode = l[1:4]
    section = l[4]
    fileRecord = l[123:128]
    fileCycle = l[128:]

    if l[4] not in ['P','H']:
        if l[5] == ' ': l[5] = '_'   # covers D_ (VHF navaid) case
        subsection = l[5]
    else: subsection = l[12]

    tableName = section + subsection

    if tableName in ['D_','DB','PN','EA','PC','PA','HA','HC','PD','PE','PF',
            'HD','HE','HF','PG','PI','PP','PS','HS']:
        airHeli_portIdent = l[6:10]
        airHeli_GeoIcao = l[10:12]

    if tableName in ['D_','DB','PN','EA','PC','PA','HA','HC','PG','PI','UR',
            'UC']:
        latitude = l[32:41]
        longitude = l[41:51]

    if tableName in ['D_','DB','PN','PA','HA','UR','UC','EA','PC','HC']:
        if tableName == 'D_': featureName = l[93:118]
        elif tableName in ['EA','PC','HC']: featureName = l[98:123]
        else: featureName = l[93:123]

    if tableName in ['D_','DB','PN']:
        navaidIdent = l[13:17]
        navaidGeoIcao = l[19:21]
        navaidFrequency = l[22:27]
        navaidClass = l[27:32]
        if tableName == 'D_':
            DMEident = l[51:55]
            DMElatitude = l[55:64]
            DMElongitude = l[64:74]

    if tableName in ['PA','HA']:
        IATAcode = l[13:16]
        speedLimitAltitude = l[22:27]
        hasIFR = l[30]
        magneticVariation = l[51:56]
        elevation = l[56:61]
        speedLimit = l[61:64]
        recommendedNavaid = l[64:68]
        recommendedNavaidGeoIcao = l[68:70]
        publicOrMilitary = l[80]
        timeZone = l[81:84]
        DST = l[84]
        if tableName == 'PA':
            longestRunway = l[27:30]
            longRunwaySurface = l[31]
        else: heliportType = l[31]

    if tableName in ['ER','PD','PE','PF','HD','HE','HF']:
        fixIdent = l[29:34]
        fixIcao = l[34:36]
        fixSectionCode = l[36]
        fixSubsectionCode = l[37]
        descriptionCode = l[39:43]
        recommendedNavaid = l[50:54]
        recommendedNavaidGeoIcao = l[54:56]
        if tableName in ['PD','PE','PF','HD','HE','HF']:
            SidStarApproachIdent = l[13:19]
            routeType = l[20]
            transitionIdent = l[20:25]
            aircraftDesignTypes = l[25]
            sequenceNumber = l[26:29]
            speedLimit = l[99:102]
            speedLimitDescription = l[117]
            routeQual1 = l[118]
            routeQual2 = l[119]
            routeQual3 = l[120]
        else:
            routeIdent = l[13:18]
            sequenceNumber = l[25:29]

    if tableName in ['EA','PC','HC']:
        waypointIdent = l[13:18]
        waypointIcao = l[19:21]
        waypointType1 = l[26]
        waypointType2 = l[27]
        waypointType3 = l[28]
        waypointusage = l[30]

    if tableName == 'PG':
        runwayIdent = l[13:18]
        runwayLength = l[22:27]
        runwayBearing = l[27:31]
        runwayGradient = l[51:56]
        landingThresholdElev = l[66:71]
        displacedTresholdLength = l[71:75]
        runwayWidth = l[7780]
        TCHvalueIndicator = l[80]
        stopwayLength = l[86:90]
        thresholdCrossingHeight = l[95:98]
        runwayDescrip = l[101:123]

    if tableName == 'PI':
        localizerIdent = l[13:17]
        ILScategory = l[17]
        localizerFreq = l[22:27]
        runwayIdent = l[27:32]
