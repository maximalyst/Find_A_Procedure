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
    filename = 'FAACIFP18_full.txt'

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

print(record_type)
pprint.pprint(area_code)
pprint.pprint(section_code)

print("Added areas:")
print(added_areas)

print("Added sections:")
print(added_sections)
