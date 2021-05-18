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
# Flow through each loop of CFIP data:
#    Read line
#    Remove trailing \n and force upper case
#    ^^^ Did the above in the loop itself
#
#    Set "standard" features--line[0],]1:4],[123:128],[128:]
#    Set section--line[4]
#    Determine if it's section P/H or not
#        If it is, get subsection -- line[12]
#        If it isn't, get subsection -- line[5]
#
#    Depending on section/subsection, input data into database
#        Get "standard" features from each section--line[xx:yy]
#        Input repeated data (ex. airport abbrevs) into ID tables
#        Reference ID tables into line's database entry
#        Input unique data (ex. lat/long) into line's database entry


from string import Template


def _primary_matcher(_table_name):
    """"""
    # TODO: Error handling of unrecognized section/subsection pairs
    # TODO: come pack to passed statements
    # if _table_name == 'AS':
    #     pass
    if _table_name in ['D_', 'DB', 'PN']:  # VHF, NDB navaid, Apt Term NDB
        return 'navaidIdent'
    if _table_name in ['EA', 'ER', 'PC']:  # Enroute Waypoint, Apt Term WP
        return 'waypointIdent'
    # if _table_name == 'ER': # Enroute Airway/Route
    #     pass
    # if _table_name == 'HA': # Heliport reference point
    #     pass
    # if _table_name == 'HC': # Heliport terminal waypoint
    #     pass
    # if _table_name == 'HF': # Heliport approach procedure
    #     pass
    # if _table_name == 'HS': # Heliport MSA
    #     pass
    if _table_name in ['PA', 'PD', 'PE', 'PF', 'PG', 'PI',
                       'PP']:  # Airport reference point
        return 'airHeli_portIdent'
    # if _table_name == 'PC': # Airport terminal waypoint
    # pass
    # if _table_name == 'PD': # Airport SID
    #     pass
    # if _table_name == 'PE': # Airport STAR
    #     pass
    # if _table_name == 'PF': # Airport Approach
    #     pass
    # if _table_name == 'PG': # Airport Runway
    #     pass
    # if _table_name == 'PI': # Airport Localizer/Glideslope
    #     pass
    # if _table_name == 'PP': # Airport SBAS Path Point
    #     pass
    # if _table_name == 'PS': # Airport MSA
    #     pass
    # if _table_name == 'UC': # Controlled airspace
    #     pass
    # if _table_name == 'UR': # Restrictive airspace
    #     pass


def _insert_Icao(newcode, cursor):
    # cursor.execute('''INSERT INTO IcaoCode (code) VALUES (?)''',
    #                (newcode,))
    # TODO: Delete this and implementation of insertion in __init__
    #  (old procedure)
    pass


class CIFPLine:
    IcaoCodes = []  # Yup, we're appending for the whole class, not unique

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
                self.subsection = '_'  # covers D_ (VHF navaid) case
            else:
                self.subsection = self.data[5]
        else:
            self.subsection = self.data[12]

        self.table_name = self.section + self.subsection
        # Simplifying equivalencies:
        if self.table_name == 'PC':
            self.table_name = 'EA'
        elif self.table_name == 'PN':
            self.table_name = 'DB'

        if self.table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PD', 'PE', 'PF', 'HD', 'HE', 'HF', 'PG', 'PI',
                               'PP', 'PS', 'HS']:
            self.airHeli_portIdent = self.data[6:10]
            self.airHeli_GeoIcao = self.data[10:12]
            if self.airHeli_GeoIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.airHeli_GeoIcao)
                _insert_Icao(self.airHeli_GeoIcao, self.c)

        if self.table_name in ['D_', 'DB', 'PN', 'EA', 'PC', 'PA', 'HA', 'HC',
                               'PG', 'PI', 'UR', 'UC']:
            self.latitude = self.data[32:41]
            self.longitude = self.data[41:51]

        if self.table_name in ['D_', 'DB', 'PN', 'PA', 'HA', 'UR', 'UC', 'EA',
                               'PC', 'HC']:
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
            if self.navaidGeoIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.navaidGeoIcao)
                _insert_Icao(self.navaidGeoIcao, self.c)

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
            if self.recommendedNavaidGeoIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.recommendedNavaidGeoIcao)
                _insert_Icao(self.recommendedNavaidGeoIcao, self.c)

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
            if self.fixIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.fixIcao)
                _insert_Icao(self.fixIcao, self.c)
            if self.recommendedNavaidGeoIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.recommendedNavaidGeoIcao)
                _insert_Icao(self.recommendedNavaidGeoIcao, self.c)

        if self.table_name in ['EA', 'PC', 'HC']:
            self.waypointIdent = self.data[13:18]
            self.waypointIcao = self.data[19:21]
            self.waypointType1 = self.data[26]
            self.waypointType2 = self.data[27]
            self.waypointType3 = self.data[28]
            self.waypointusage = self.data[30]
            if self.waypointIcao not in self.IcaoCodes:
                self.IcaoCodes.append(self.waypointIcao)
                _insert_Icao(self.waypointIcao, self.c)

        if self.table_name == 'PG':
            self.runwayIdent = self.data[13:18]
            self.runwayLength = self.data[22:27]
            self.runwayBearing = self.data[27:31]
            self.runwayGradient = self.data[51:56]
            self.landingThresholdElev = self.data[66:71]
            self.displacedTresholdLength = self.data[71:75]
            self.runwayWidth = self.data[77:80]
            self.TCHvalueIndicator = self.data[80]
            self.stopwayLength = self.data[86:90]
            self.thresholdCrossingHeight = self.data[95:98]
            self.runwayDescrip = self.data[101:123]

        if self.table_name == 'PI':
            self.localizerIdent = self.data[13:17]
            self.ILScategory = self.data[17]
            self.localizerFreq = self.data[22:27]
            self.runwayIdent = self.data[27:32]

        if self.table_name in ['D_', 'DB', 'PN']:
            self.hinge = 'navaidIdent'
            self.hingeValue = self.navaidIdent
        if self.table_name in ['EA', 'PC']:
            self.hinge = 'waypointIdent'
            self.hingeValue = self.waypointIdent
        if self.table_name in ['ER']:
            self.hinge = 'routeIdent'
            self.hingeValue = self.routeIdent
        if self.table_name in ['PA']:
            self.hinge = 'airHeli_portIdent'
            self.hingeValue = self.airHeli_portIdent
        if self.table_name in ['PD', 'PE', 'PF', 'HD', 'HE', 'HF']: #  heliports aren't in MVP, but this is where SID/STAR/Appch will go eventually
            self.hinge = 'SidStarApproachIdent'
            self.hingeValue = self.SidStarApproachIdent
        if self.table_name in ['PI']:
            self.hinge = 'localizerIdent'
            self.hingeValue = self.localizerIdent
        # TODO: Figure out runway (PG) situation?

    def already_exists(self):
        self.c.execute(Template('''SELECT id FROM $table WHERE $hinge = '''
                                "'$hingevalue'")
                       .substitute(table=self.table_name, hinge=self.hinge,
                                   hingevalue=self.hingeValue))
        if self.c.fetchone() is not None:
            return True
        else:
            return False

    def record_line(self):
        if self.hinge == 'navaidIdent':
            self.navaidIdent_line()
        if self.hinge == 'waypointIdent':
            self.waypointIdent_line()
        if self.hinge == 'routeIdent':
            self.routeIdent_line()
        if self.hinge == 'airHeli_portIdent':
            self.airHeli_portIdent_line()
        if self.hinge == 'SidStarApproachIdent':
            self.SidStarApproachIdent_line()
        if self.hinge == 'localizerIdent':
            self.localizerIdent_line()

    def standard_inserts(self, _table_name, _primary_key):
        self.c.execute('''INSERT INTO ? (file_rec) VALUES ? WHERE ? = ?''',
                       (self.table_name, self.fileRecord,
                        _primary_matcher(self.table_name), _primary_key))
        self.c.execute('''INSERT INTO ? (cycle_date) VALUES ? WHERE ? = ?''',
                       (self.table_name, self.fileCycle,
                        _primary_matcher(self.table_name), _primary_key))
        pass

    def navaidIdent_line(self):  # D_, DB, and PN lines
        # _areaCode_id, _sectionCode_id = CIFPLine.standard_inserts(self, self.table_name, 'navaidIdent')  # TODO fix this
        # TODO: Need INSERT OR IGNORE statements for all of these. Function?
        print('Hello navaids!!')
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.navaidGeoIcao,))
        navaidGeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM PA WHERE airHeli_portIdent = ?',
                       (self.airHeli_portIdent,))
        airHeli_portIdent_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM GeoIcao WHERE code = ?',
                       (self.airHeli_GeoIcao,))
        airHeli_GeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM NAVAIDclass1 WHERE class = ?',
                       (self.navaidClass[0],))
        navaidClass1_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM NAVAIDclass2 WHERE class = ?',
                       (self.navaidClass[1],))
        navaidClass2_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM NAVAIDclass3 WHERE class = ?',
                       (self.navaidClass[2],))
        navaidClass3_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM NAVAIDclass4 WHERE class = ?',
                       (self.navaidClass[3],))
        navaidClass4_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM NAVAIDclass5 WHERE class = ?',
                       (self.navaidClass[4],))
        navaidClass5_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM DMEident WHERE name = ?',
                       (self.DMEident,))
        DMEident_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM AreaCode WHERE area = ?',
                       (self.areaCode,))
        areaCode_id = self.c.fetchone()[0]
        self.c.execute('''SELECT rowid FROM SecCode WHERE
                          (section = ?) AND (subsec = ?)''',
                       (self.section, self.subsection,))
        sectionCode_id = self.c.fetchone()[0]
        self.c.execute('''INSERT OR IGNORE INTO D_ (
                                     navaidIdent,
                                     latitude,
                                     longitude,
                                     featureName,
                                     DMElatitude,
                                     DMElongitude,
                                     navaidGeoIcao_id,
                                     airHeli_portIdent_id,
                                     airHeli_GeoIcao_id,
                                     navaidFrequency,
                                     navaidClass1_id,
                                     navaidClass2_id,
                                     navaidClass3_id,
                                     navaidClass4_id,
                                     navaidClass5_id,
                                     DMEident_id,
                                     areaCode_id,
                                     sectionCode_id
                                     file_rec,
                                     cycle,date)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?)''',
                       (self.navaidIdent, self.latitude, self.longitude,
                        self.featureName, self.DMElatitude, self.DMElongitude,
                        navaidGeoIcao_id, airHeli_portIdent_id,
                        airHeli_GeoIcao_id, self.navaidFrequency,
                        navaidClass1_id, navaidClass2_id, navaidClass3_id,
                        navaidClass4_id, navaidClass5_id, DMEident_id,
                        areaCode_id, sectionCode_id, self.fileRecord,
                        self.fileCycle))

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
        # Just send them to the DB table!
        pass

    def PP(self, connection):  # Airport SBAS Path Point
        pass

    def PS(self, connection):  # Airport MSA
        pass

    def UC(self, connection):  # Controlled airspace
        pass

    def UR(self, connection):  # Restrictive airspace
        pass
