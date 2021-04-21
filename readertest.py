# import sqlite3
#
# conn = sqlite3.connect('Procedure_db.sqlite')
# cur = conn.cursor()
#
# cur.execute('DROP TABLE IF EXISTS Approach')
# cur.execute('CREATE TABLE Approach (org TEXT, count INTEGER)')


# Just want to output how many of each record type is in FAACIFP18, so I don't
# do needless work

"""
Areas I found:
AS: Grid MORA
D_: VHF navaid
DB: NDB navaid
EA: Enroute Waypoint
ER: Enroute Airway/Route
HA: Heliport reference point
HC: Heliport terminal waypoint
HF: Heliport approach procedure
HS: Heliport MSA
PA: Airport reference point
PC: Airport terminal waypoint
PD: Airport SID
PE: Airport STAR
PF: Airport Approach
PG: Airport Runway
PI: Airport Localizer/Glideslope
PN: Airport Terminal NDB
PP: Airport SBAS Path Point
PS: Airport MSA
UC: Controlled airspace
UR: Restrictive airspace
"""

import pprint  #pretty printing dictionaries

print("Blank for default file")
filename = input('Path to filename: ')
if len(filename)==0:
    filename = './Private_Files/FAACIFP18_full.txt'

record_type = [0,0,0] # [Standard, Tailored, Unknown]; column 1
area_code = {k: 0 for k in [ #column 2 thru 4
    'USA',
    'PAC',
    'CAN',
    'EEU',
    'LAM',
    'SAM',
    'SPA',
    'EUR',
    'AFR',
    'MES'
    ]}
section_code = {k: 0 for k in #column 5 and 6
    ['AS',
     'D ','DB','DT',
     'EA','EM','EP','ER','ES','ET','EU','EV',
     'HA','HC','HD','HE','HF','HH','HK','HS','HP','HV',
     'PA','PB','PC','PD','PE','PF','PG','PH','PI','PK','PL','PM','PN','PP','PQ','PR','PS','PT','PV',
     'R ','RA','RH',
     'TC','TG','TV',
     'UC','UF','UR']}

# In Enroute Waypoint Records (EA), the Subsection Code occupies column 6, with
#  column 13 blank. In Airport or Heliport Terminal Waypoint Records (PC and HC),
#  the Subsection Code occupies column 13, with column 6 blank.

added_areas = []
added_sections = []

ICAOcodes = {}

with open(filename,'r') as fh:
    for thisline in fh:
        test = thisline.rstrip()
        #print(test)
        if test[:3] == 'HDR':
            continue # skip the header lines

        if test[0] == 'S': record_type[0] += 1
        elif test[0] == 'T': record_type[1] += 1
        else: record_type[2] += 1 # Uh Oh

        if test[1:4] not in area_code:
            area_code[test[1:4]] = 1
            added_areas.append(test[1:4])
        else: area_code[test[1:4]] += 1

        if (test[4]!='P') & (test[4]!='H') & (test[4:6] not in section_code):
            section_code[test[4:6]] = 1
            added_sections.append(test[4:6])
        elif (test[4:6]=='P ') | (test[4:6]=='H '):
            if test[4]+test[12] not in section_code:
                section_code[test[4]+test[12]] = 1
                added_sections.append(test[4]+test[12])
            else: section_code[test[4]+test[12]] += 1
        else: section_code[test[4:6]] += 1
        
        ###############

        recordType = test[0]
        areaCode = test[1:4]
        section = test[4]
        fileRecord = test[123:128]
        fileCycle = test[128:]

        if section not in ['P', 'H']:
            if test[5] == ' ':
                subsection = '_'  # covers D_ (VHF navaid) case
            else:
                subsection = test[5]
        else:
            subsection = test[12]

        table_name = section + subsection

        if table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PD', 'PE', 'PF', 'HD', 'HE', 'HF', 'PG', 'PI',
                               'PP', 'PS', 'HS']:
            airHeli_portIdent = test[6:10]
            airHeli_GeoIcao = test[10:12]
            if airHeli_GeoIcao in ICAOcodes:
                ICAOcodes[airHeli_GeoIcao] += 1
            else:
                ICAOcodes[airHeli_GeoIcao] = 1

        if table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PG', 'PI', 'UR', 'UC']:
            latitude = test[32:41]
            longitude = test[41:51]

        if table_name in ['D_', 'DB', 'PN', 'PA', 'HA', 'UR', 'UC', 'EA',
                               'PC', 'HC']:
            if table_name == 'D_':
                featureName = test[93:118]
            elif table_name in ['EA', 'PC', 'HC']:
                featureName = test[98:123]
            else:
                featureName = test[93:123]

        if table_name in ['D_', 'DB', 'PN']:
            navaidIdent = test[13:17]
            navaidGeoIcao = test[19:21]
            navaidFrequency = test[22:27]
            navaidClass = test[27:32]
            if table_name == 'D_':
                DMEident = test[51:55]
                DMElatitude = test[55:64]
                DMElongitude = test[64:74]
            if navaidGeoIcao in ICAOcodes:
                ICAOcodes[navaidGeoIcao] += 1
            else:
                ICAOcodes[navaidGeoIcao] = 1

        if table_name in ['PA', 'HA']:
            IATAcode = test[13:16]
            speedLimitAltitude = test[22:27]
            hasIFR = test[30]
            magneticVariation = test[51:56]
            elevation = test[56:61]
            speedLimit = test[61:64]
            recommendedNavaid = test[64:68]
            recommendedNavaidGeoIcao = test[68:70]
            publicOrMilitary = test[80]
            timeZone = test[81:84]
            DST = test[84]
            if table_name == 'PA':
                longestRunway = test[27:30]
                longRunwaySurface = test[31]
            else:
                heliportType = test[31]
            if recommendedNavaidGeoIcao in ICAOcodes:
                ICAOcodes[recommendedNavaidGeoIcao] += 1
            else:
                ICAOcodes[recommendedNavaidGeoIcao] = 1

        if table_name in ['ER', 'PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
            fixIdent = test[29:34]
            fixIcao = test[34:36]
            fixSectionCode = test[36]
            fixSubsectionCode = test[37]
            descriptionCode = test[39:43]
            recommendedNavaid = test[50:54]
            recommendedNavaidGeoIcao = test[54:56]
            if table_name in ['PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
                SidStarApproachIdent = test[13:19]
                routeType = test[20]
                transitionIdent = test[20:25]
                aircraftDesignTypes = test[25]
                sequenceNumber = test[26:29]
                speedLimit = test[99:102]
                speedLimitDescription = test[117]
                routeQual1 = test[118]
                routeQual2 = test[119]
                routeQual3 = test[120]
            else:
                routeIdent = test[13:18]
                sequenceNumber = test[25:29]
            if fixIcao in ICAOcodes:
                ICAOcodes[fixIcao] += 1
            else:
                ICAOcodes[fixIcao] = 1
            if recommendedNavaidGeoIcao in ICAOcodes:
                ICAOcodes[recommendedNavaidGeoIcao] += 1
            else:
                ICAOcodes[recommendedNavaidGeoIcao] = 1

        if table_name in ['EA', 'PC', 'HC']:
            waypointIdent = test[13:18]
            waypointIcao = test[19:21]
            waypointType1 = test[26]
            waypointType2 = test[27]
            waypointType3 = test[28]
            waypointusage = test[30]
            if waypointIcao in ICAOcodes:
                ICAOcodes[waypointIcao] += 1
            else:
                ICAOcodes[waypointIcao] = 1

        if table_name == 'PG':
            runwayIdent = test[13:18]
            runwayLength = test[22:27]
            runwayBearing = test[27:31]
            runwayGradient = test[51:56]
            landingThresholdElev = test[66:71]
            displacedTresholdLength = test[71:75]
            runwayWidth = test[77:80]
            TCHvalueIndicator = test[80]
            stopwayLength = test[86:90]
            thresholdCrossingHeight = test[95:98]
            runwayDescrip = test[101:123]

        if table_name == 'PI':
            localizerIdent = test[13:17]
            ILScategory = test[17]
            localizerFreq = test[22:27]
            runwayIdent = test[27:32]

print(record_type)
pprint.pprint(area_code)
pprint.pprint(section_code)
pprint.pprint(ICAOcodes)

print("Added areas:")
print(added_areas)

print("Added sections:")
print(added_sections)
