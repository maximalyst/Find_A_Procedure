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


# def _primary_matcher(_table_name):
# #     """"""
# #     # TODO: Error handling of unrecognized section/subsection pairs
# #     # TODO: come pack to passed statements
# #     # if _table_name == 'AS':
# #     #     pass
# #     if _table_name in ['D_', 'DB', 'PN']:  # VHF, NDB navaid, Apt Term NDB
# #         return 'navaid'
# #     if _table_name in ['EA', 'ER', 'PC']:  # Enroute Waypoint, Apt Term WP
# #         return 'waypointIdent'
# #     # if _table_name == 'ER': # Enroute Airway/Route
# #     #     pass
# #     # if _table_name == 'HA': # Heliport reference point
# #     #     pass
# #     # if _table_name == 'HC': # Heliport terminal waypoint
# #     #     pass
# #     # if _table_name == 'HF': # Heliport approach procedure
# #     #     pass
# #     # if _table_name == 'HS': # Heliport MSA
# #     #     pass
# #     if _table_name in ['PA', 'PD', 'PE', 'PF', 'PG', 'PI',
# #                        'PP']:  # Airport reference point
# #         return 'airHeli_portIdent'
# #     # if _table_name == 'PC': # Airport terminal waypoint
# #     # pass
# #     # if _table_name == 'PD': # Airport SID
# #     #     pass
# #     # if _table_name == 'PE': # Airport STAR
# #     #     pass
# #     # if _table_name == 'PF': # Airport Approach
# #     #     pass
# #     # if _table_name == 'PG': # Airport Runway
# #     #     pass
# #     # if _table_name == 'PI': # Airport Localizer/Glideslope
# #     #     pass
# #     # if _table_name == 'PP': # Airport SBAS Path Point
# #     #     pass
# #     # if _table_name == 'PS': # Airport MSA
# #     #     pass
# #     # if _table_name == 'UC': # Controlled airspace
# #     #     pass
# #     # if _table_name == 'UR': # Restrictive airspace
# #     #     pass


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
            if self.data[4:6] == 'D ':
                self.subsection = '_'  # covers D_ (VHF navaid) case
            else:
                self.subsection = self.data[5]
        else:
            self.subsection = self.data[12]

        self.table_name = self.section + self.subsection
        # Simplifying equivalencies:
        if self.table_name == 'PC':
            self.table_name = 'EA'
        # elif self.table_name == 'PN':
        #     self.table_name = 'DB'

        if self.table_name in ['D_', 'DB', 'PN', 'EA', 'PA', 'HA', 'HC', 'PD',
                               'PE', 'PF',
                               'HD', 'HE', 'HF', 'PG', 'PI', 'PP', 'PS', 'HS']:
            self.airHeli_portIdent = self.data[6:10]
            self.airHeli_GeoIcao = self.data[10:12]
            self.c.execute(
                'INSERT OR IGNORE INTO PA (airHeli_portIdent) VALUES (?);',
                (self.airHeli_portIdent,))

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
            self.navaid = self.data[13:17]
            self.navaidGeoIcao = self.data[19:21]
            self.navaidFrequency = self.data[22:27]
            self.navaidClass = self.data[27:32]
            if self.table_name == 'D_':
                if self.data[51:55] == '    ':
                    self.DMEident = self.navaid
                else:
                    self.DMEident = self.data[51:55]
                self.c.execute(
                    'INSERT OR IGNORE INTO DMEident (name) VALUES (?);',
                    (self.DMEident,))
                self.DMElatitude = self.data[55:64]
                self.DMElongitude = self.data[64:74]
            self.c.execute('INSERT OR IGNORE INTO navaid (ident) VALUES (?);',
                           (self.navaid,))

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
            self.c.execute('INSERT OR IGNORE INTO IATAcode (code) VALUES (?);',
                           (self.IATAcode,))

        if self.table_name in ['ER', 'PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
            self.fixIdent = self.data[29:34]
            self.fixIcao = self.data[34:36]
            self.fixSectionCode = self.data[36]
            self.fixSubsectionCode = self.data[37]
            if self.table_name != 'ER':
                self.SidStarApproachIdent = self.data[13:19]
                self.routeType = self.data[19]
                # First continuation record to deal with; this might go to
                # another spot later for "general continuation records"
                if (self.routeType == 'R' or self.routeType == 'H') and (
                        self.data[38] != '1'):
                    self.LVnavAuth = self.data[51]
                    self.LVnavLevelOfService = self.data[52:62]
                    self.LnavAuth = self.data[62]
                    self.LnavLevelOfService = self.data[63:73]
                    self.remoteAltimeterFlag = self.data[73]
                    self.RNPAuth1 = self.data[88]
                    self.RNPAuth2 = self.data[92]
                    self.RNPAuth3 = self.data[96]
                    self.RNPAuth4 = self.data[100]
                    self.RNPLevelOfService1 = self.data[89:92]
                    self.RNPLevelOfService2 = self.data[93:96]
                    self.RNPLevelOfService3 = self.data[97:100]
                    self.RNPLevelOfService4 = self.data[101:104]
                self.transitionIdent = self.data[20:25]
                self.aircraftDesignTypes = self.data[25]
                self.sequenceNumber = self.data[26:29]
                self.speedLimit = self.data[99:102]
                self.speedLimitDescription = self.data[117]
                self.routeQual1 = self.data[118]
                self.routeQual2 = self.data[119]
                self.routeQual3 = self.data[120]
                self.recommendedNavaidSection = self.data[78]
                self.recommendedNavaidSubsection = self.data[79]
                # Need to do the same as earlier, for simplicity:
                # TODO: Remove this old code
                # if self.data[78:80] == 'PN':
                #     self.recommendedNavaidSection = 'P'
                #     self.recommendedNavaidSubsection = 'N'
                if self.recommendedNavaidSubsection == ' ':
                    self.recommendedNavaidSubsection = '_'
                    # For when rec. navaid is VHF navaid ('D ')
            else:
                self.routeIdent = self.data[13:18]
                self.sequenceNumber = self.data[25:29]
            if self.table_name == 'ER' or int(self.data[38]) <= 1:
                self.descriptionCode = self.data[39:43]
                self.recommendedNavaid = self.data[50:54]
                self.recommendedNavaidGeoIcao = self.data[54:56]
                self.c.execute(
                    '''INSERT OR IGNORE INTO fixIdent (name) VALUES (?);''',
                    (self.fixIdent,))
                #if self.recommendedNavaid != '    ':
                self.c.execute('INSERT OR IGNORE INTO navaid (ident) VALUES (?)',
                                   (self.recommendedNavaid,))

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
            self.runwayWidth = self.data[77:80]
            self.TCHvalueIndicator = self.data[80]
            self.stopwayLength = self.data[86:90]
            self.thresholdCrossingHeight = self.data[95:98]
            self.runwayDescrip = self.data[101:123]

        if self.table_name == 'PI':
            self.navaid = self.data[13:17]
            self.ILScategory = self.data[17]
            self.localizerFreq = self.data[22:27]
            self.runwayIdent = self.data[27:32]

        # TODO: Figure out if I can fully remove this
        # self.hinge = self._get_hinge(self.table_name)[0]
        # self.hingeValue = self._get_hinge(self.table_name)[1]
        # if self.table_name in ['D_', 'DB', 'PN']:
        #     self.hinge = 'navaid'
        #     self.hingeValue = self.navaid
        # if self.table_name in ['EA', 'PC']:
        #     self.hinge = 'waypointIdent'
        #     self.hingeValue = self.waypointIdent
        # if self.table_name in ['ER']:
        #     self.hinge = 'routeIdent'
        #     self.hingeValue = self.routeIdent
        # if self.table_name in ['PA']:
        #     self.hinge = 'airHeli_portIdent'
        #     self.hingeValue = self.airHeli_portIdent
        # if self.table_name in ['PD', 'PE', 'PF', 'HD', 'HE',
        #                        'HF']:  # heliports aren't in MVP, but this is where SID/STAR/Appch will go eventually
        #     self.hinge = 'SidStarApproachIdent'
        #     self.hingeValue = self.SidStarApproachIdent
        # if self.table_name in ['PI']:
        #     self.hinge = 'navaid'
        #     self.hingeValue = self.navaid
        # TODO: Figure out runway (PG) situation?

        self.connection.commit()

    # TODO: This is going to break now since hinge is removed.
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
        if self.table_name in ['D_', 'DB', 'PN']:
            self.navaid_line()
        if self.table_name in ['EA', 'PC']:
            self.waypointIdent_line()
        if self.table_name in ['ER']:
            self.routeIdent_line()
        if self.table_name in ['PA']:
            self.airHeli_portIdent_line()
        if self.table_name in ['PD', 'PE', 'PF', 'HD', 'HE', 'HF']:
            self.SidStarApproachIdent_line()
        if self.table_name in ['PI']:
            self.localizerIdent_line()

    def _standard_selects(self, _sec, _subsec):
        self.c.execute('''SELECT rowid FROM SecCode WHERE
                          (section = ?) AND (subsec = ?)''',
                       (_sec, _subsec))
        _sectionCode_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM AreaCode WHERE area = ?',
                       (self.areaCode,))
        _areaCode_id = self.c.fetchone()[0]

        return _sectionCode_id, _areaCode_id

    def navaid_line(self):  # D_, DB, and PN lines
        self.c.execute('SELECT id FROM navaid WHERE ident = ?',
                       (self.navaid,))
        navaid_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.navaidGeoIcao,))
        navaidGeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
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
        self.c.execute('SELECT id FROM PA WHERE airHeli_portIdent = ?',
                       (self.airHeli_portIdent,))
        airHeli_portIdent_id = self.c.fetchone()[0]
        sectionCode_id = self._standard_selects(self.section, self.subsection)[
            0]
        areaCode_id = self._standard_selects(self.section, self.subsection)[1]
        self.c.execute('INSERT OR IGNORE INTO ' + self.table_name + ''' (
                                     navaid_id,
                                     latitude,
                                     longitude,
                                     featureName,
                                     navaidGeoIcao_id,
                                     airHeli_portIdent_id,
                                     airHeli_GeoIcao_id,
                                     navaidFrequency,
                                     navaidClass1_id,
                                     navaidClass2_id,
                                     navaidClass3_id,
                                     navaidClass4_id,
                                     navaidClass5_id,
                                     areaCode_id,
                                     sectionCode_id,
                                     file_rec,
                                     cycle_date)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                       (navaid_id, self.latitude, self.longitude,
                        self.featureName, navaidGeoIcao_id,
                        airHeli_portIdent_id,
                        airHeli_GeoIcao_id, self.navaidFrequency,
                        navaidClass1_id, navaidClass2_id, navaidClass3_id,
                        navaidClass4_id, navaidClass5_id,
                        areaCode_id, sectionCode_id, self.fileRecord,
                        self.fileCycle))
        if self.table_name == 'D_':
            self.c.execute('SELECT id FROM DMEident WHERE name = ?',
                           (self.DMEident,))
            DMEident_id = self.c.fetchone()[0]
            self.c.execute('''UPDATE D_
                               SET DMElatitude = (?),
                                   DMElongitude = (?),
                                   DMEident_id = (?)
                               WHERE navaid_id = (?);''',
                           (self.DMElatitude, self.DMElongitude, DMEident_id,
                            navaid_id))
        if self.table_name in ['DB', 'PN']:
            self.c.execute('SELECT id FROM DB_or_PN WHERE flag = ?',
                           (self.table_name,))
            DB_or_PN_id = self.c.fetchone()[0]
            self.c.execute('''UPDATE DB
                               SET DB_or_PN_id = (?)
                               WHERE navaid_id = (?);''',
                           (DB_or_PN_id, navaid_id))
        self.connection.commit()

    def waypointIdent_line(self):  # EA, PC lines
        self.c.execute('SELECT id FROM WaypointType1 WHERE type = ?',
                       (self.waypointType1[0],))
        waypointType1_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM WaypointType2 WHERE type = ?',
                       (self.waypointType2[0],))
        waypointType2_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM WaypointType3 WHERE type = ?',
                       (self.waypointType3[0],))
        waypointType3_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM WaypointUsage WHERE usage = ?',
                       (self.waypointType3[0],))
        waypointUsage_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.airHeli_GeoIcao,))
        airHeli_GeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM PA WHERE airHeli_portIdent = ?',
                       (self.airHeli_portIdent,))
        airHeli_portIdent_id = self.c.fetchone()[0]
        sectionCode_id = self._standard_selects(self.section, self.subsection)[
            0]
        areaCode_id = self._standard_selects(self.section, self.subsection)[1]
        self.c.execute('''INSERT OR IGNORE INTO EA (
                                waypointIdent,
                                waypointIcao_id,
                                waypointType1_id,
                                waypointType2_id,
                                waypointType3_id,
                                waypointusage_id,
                                airHeli_portIdent_id,
                                airHeli_GeoIcao_id,
                                latitude,
                                longitude,
                                featureName,
                                areaCode_id,
                                sectionCode_id,
                                file_rec,
                                cycle_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                       (self.waypointIdent, self.waypointIdent,
                        waypointType1_id,
                        waypointType2_id, waypointType3_id, waypointUsage_id,
                        airHeli_portIdent_id, airHeli_GeoIcao_id,
                        self.latitude,
                        self.longitude, self.featureName, areaCode_id,
                        sectionCode_id,
                        self.fileRecord, self.fileCycle))

    def routeIdent_line(self):  # ER lines
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.fixIcao,))
        fixIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.recommendedNavaidGeoIcao,))
        recommendedNavaidGeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM fixIdent WHERE name = ?',
                       (self.fixIdent,))
        fixIdent_id = self.c.fetchone()[0]
        self.c.execute('''SELECT rowid FROM SecCode WHERE
                          (section = ?) AND (subsec = ?)''',
                       (self.section, self.subsection,))
        fixSectionCode_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM waypointDescription1 WHERE desc = ?',
                       (self.descriptionCode[0],))
        waypointDescription1_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM waypointDescription2 WHERE desc = ?',
                       (self.descriptionCode[1],))
        waypointDescription2_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM waypointDescription3 WHERE desc = ?',
                       (self.descriptionCode[2],))
        waypointDescription3_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM waypointDescription4 WHERE desc = ?',
                       (self.descriptionCode[3],))
        waypointDescription4_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM navaid WHERE ident = ?',
                       (self.recommendedNavaid,))
        recommendedNavaid_id = self.c.fetchone()[0]
        sectionCode_id = self._standard_selects(self.section, self.subsection)[
            0]
        areaCode_id = self._standard_selects(self.section, self.subsection)[1]
        self.c.execute('''INSERT OR IGNORE INTO ER (
                                routeIdent,
                                sequenceNumber,
                                fixIdent_id,
                                fixIcao_id,
                                fixSectionCode_id,
                                waypointDescription1_id,
                                waypointDescription2_id,
                                waypointDescription3_id,
                                waypointDescription4_id,
                                recommendedNavaid_id,
                                recommendedNavaidGeoIcao_id,
                                areaCode_id,
                                sectionCode_id,
                                file_rec,
                                cycle_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                       (self.routeIdent, self.sequenceNumber, fixIdent_id,
                        fixIcao_id,
                        fixSectionCode_id, waypointDescription1_id,
                        waypointDescription2_id,
                        waypointDescription3_id, waypointDescription4_id,
                        recommendedNavaid_id,
                        recommendedNavaidGeoIcao_id, areaCode_id,
                        sectionCode_id, self.fileRecord,
                        self.fileCycle))

    def airHeli_portIdent_line(self):  # PA and HA lines
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.airHeli_GeoIcao,))
        airHeli_GeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM hasIFR WHERE flag = ?',
                       (self.hasIFR,))
        hasIFR_id = self.c.fetchone()[0]
        # 11 Jun '21: This could be a future bug, unclear if rec. navaid will ALWAYS be VHF for airports
        self.c.execute('SELECT id FROM navaid WHERE ident = ?',
                       (self.recommendedNavaid,))
        recommendedNavaid_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.recommendedNavaidGeoIcao,))
        recommendedNavaidGeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM publicOrMilitary WHERE flag = ?',
                       (self.publicOrMilitary,))
        publicOrMilitary_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM DST WHERE flag = ?',
                       (self.DST,))
        DST_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IATAcode WHERE code = ?',
                       (self.IATAcode,))
        IATAcode_id = self.c.fetchone()[0]
        sectionCode_id = self._standard_selects(self.section, self.subsection)[
            0]
        areaCode_id = self._standard_selects(self.section, self.subsection)[1]
        if self.table_name == 'PA':
            # var1 = 'longestRunway'  # inputting these maybe later
            # var2 = 'longRwySfcCode'
            # var3 = 'magOrTrue'
            pass
        else:
            # var1 = 'datumCode'
            # var2 = 'heliType'
            # TODO: finish this area
            pass
        # We need to UPDATE instead of insert because we already added the 4-char name earlier
        self.c.execute('UPDATE ' + self.table_name + '''
                        SET airHeli_GeoIcao_id = (?),
                            latitude = (?),
                            longitude = (?),
                            featureName = (?),
                            IATAcode_id = (?),
                            speedLimitAltitude = (?),
                            hasIFR_id = (?),
                            magneticVariation = (?),
                            elevation = (?),
                            speedLimit = (?),
                            recommendedNavaid_id = (?),
                            recommendedNavaidGeoIcao_id = (?),
                            publicOrMilitary_id = (?),
                            timeZone = (?),
                            DST_id = (?),
                            areaCode_id = (?),
                            sectionCode_id = (?),
                            file_rec = (?),
                            cycle_date = (?)
                        WHERE airHeli_portIdent = (?);''',
                       (airHeli_GeoIcao_id, self.latitude,
                        self.longitude, self.featureName, IATAcode_id,
                        self.speedLimitAltitude,
                        hasIFR_id, self.magneticVariation, self.elevation,
                        self.speedLimit,
                        recommendedNavaid_id, recommendedNavaidGeoIcao_id,
                        publicOrMilitary_id,
                        self.timeZone, DST_id, areaCode_id, sectionCode_id,
                        self.fileRecord,
                        self.fileCycle, self.airHeli_portIdent))
        if self.table_name == 'PA':
            # TODO: future expansion
            # self.c.execute('''UPDATE PA
            #                   SET longestRunway = (?),
            #                       longestSurface = (?)
            #                   WHERE airHeli_portIdent = (?);''',
            #                (self.longestRunway, self.longRunwaySurface, self.airHeli_portIdent))
            pass
        else:
            # insert other heliport values (Heliport Type)
            pass

    def SidStarApproachIdent_line(self):  # PD, PE, PF (and H_) lines
        if int(self.data[38]) <= 1:
            self.c.execute('SELECT id FROM IcaoCode WHERE code = (?)',
                           (self.fixIcao,))
            fixIcao_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM IcaoCode WHERE code = (?)',
                           (self.airHeli_GeoIcao,))
            airHeli_GeoIcao_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM PA WHERE airHeli_portIdent = (?)',
                           (self.airHeli_portIdent,))
            airHeli_PortIdent_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM waypointDescription1 WHERE desc = (?)',
                (self.descriptionCode[0],))
            descriptionCode1_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM waypointDescription2 WHERE desc = (?)',
                (self.descriptionCode[1],))
            descriptionCode2_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM waypointDescription3 WHERE desc = (?)',
                (self.descriptionCode[2],))
            descriptionCode3_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM waypointDescription4 WHERE desc = (?)',
                (self.descriptionCode[3],))
            descriptionCode4_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM navaid WHERE ident = (?)',
                    (self.recommendedNavaid,))
            recommendedNavaid_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM IcaoCode WHERE code = (?)',
                           (self.recommendedNavaidGeoIcao,))
            recommendedNavaidGeoIcao_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM aircraftDesignType WHERE type = (?)',
                (self.aircraftDesignTypes,))
            aircraftDesignType_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM speedLimitDescription WHERE descrip = (?)',
                (self.speedLimitDescription,))
            speedLimitDescription_id = self.c.fetchone()[0]
            if self.table_name == 'PD':
                _qual_type = 'SID'
            elif self.table_name == 'PE':
                _qual_type = 'STAR'
            else:  # self.table_name == 'PF':
                _qual_type = 'Appch'
            self.c.execute(Template('SELECT id FROM $table WHERE qual = (?)')
                           .substitute(table='route' + _qual_type + 'Qual1'),
                           (self.routeQual1,))
            routeQual1_id = self.c.fetchone()[0]
            self.c.execute(Template('SELECT id FROM $table WHERE qual = (?)')
                           .substitute(table='route' + _qual_type + 'Qual2'),
                           (self.routeQual2,))
            routeQual2_id = self.c.fetchone()[0]
            self.c.execute(Template('SELECT id FROM $table WHERE qual = (?)')
                           .substitute(table='route' + _qual_type + 'Qual3'),
                           (self.routeQual3,))
            routeQual3_id = self.c.fetchone()[0]
            sectionCode_id = self._standard_selects(self.section, self.subsection)[0]
            areaCode_id = self._standard_selects(self.section, self.subsection)[1]
            fixSectionCode_id = self._standard_selects(self.section, self.subsection)[0]
            self.c.execute('INSERT OR IGNORE INTO ' + self.table_name + ''' (
                                airHeli_portIdent_id,
                                airHeli_GeoIcao_id,
                                fixIdent_id, --NOTE: _id for historical purposes, can be globally changed if this works.
                                fixIcao_id,
                                fixSectionCode_id,
                                descriptionCode1_id,
                                descriptionCode2_id,
                                descriptionCode3_id,
                                descriptionCode4_id,
                                recommendedNavaid_id,
                                recommendedNavaidGeoIcao_id,
                                SidStarApproachIdent,
                                transitionIdent,
                                aircraftDesignType_id,
                                sequenceNumber,
                                speedLimit,
                                speedLimitDescription_id,
                                routeQual1_id,
                                routeQual2_id,
                                routeQual3_id,
                                areaCode_id,
                                sectionCode_id,
                                file_rec,
                                cycle_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                           (airHeli_PortIdent_id, airHeli_GeoIcao_id,
                            self.fixIdent, fixIcao_id,
                            fixSectionCode_id, descriptionCode1_id,
                            descriptionCode2_id, descriptionCode3_id,
                            descriptionCode4_id,
                            recommendedNavaid_id, recommendedNavaidGeoIcao_id,
                            self.SidStarApproachIdent,
                            self.transitionIdent, aircraftDesignType_id,
                            self.sequenceNumber, self.speedLimit,
                            speedLimitDescription_id,
                            routeQual1_id, routeQual2_id, routeQual3_id,
                            areaCode_id,
                            sectionCode_id, self.fileRecord, self.fileCycle))
            if self.table_name == 'PD':
                self.c.execute('SELECT id FROM routeTypeSID WHERE type = (?)',
                               (self.routeType,))
                routeTypeSID_id = self.c.fetchone()[0]
                self.c.execute('''UPDATE PD SET routeTypeSID_id = ?
                                  WHERE SidStarApproachIdent = ?''',
                               (routeTypeSID_id, self.SidStarApproachIdent))
            if self.table_name == 'PE':
                self.c.execute('''UPDATE PE SET routeTypeSTAR = ?
                                  WHERE SidStarApproachIdent = ?''',
                               (self.routeType, self.SidStarApproachIdent))
                # Reminder: Doing this since the Types are literally 1-3 already
            if self.table_name == 'PF':
                self.c.execute('SELECT id FROM routeTypeApproach WHERE type = (?)',
                               (self.routeType,))
                routeTypeApproach_id = self.c.fetchone()[0]
                self.c.execute('''UPDATE PF SET routeTypeApproach_id = (?)
                                  WHERE SidStarApproachIdent =(?)''',
                               (routeTypeApproach_id, self.SidStarApproachIdent))
        # TODO: Change self.data calls into variable names during __init__
        if self.table_name == 'PF' and (
                self.routeType == 'R' or self.routeType == 'H') and \
                int(self.data[38]) > 1 and self.data[39] == 'W':
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.LVnavAuth,))
            LVnavAuth_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.LnavAuth,))
            LnavAuth_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.RNPAuth1,))
            RNPAuth1_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.RNPAuth2,))
            RNPAuth2_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.RNPAuth3,))
            RNPAuth3_id = self.c.fetchone()[0]
            self.c.execute('SELECT id FROM RNAVAuthorized WHERE flag = (?)',
                           (self.RNPAuth4,))
            RNPAuth4_id = self.c.fetchone()[0]
            self.c.execute(
                'SELECT id FROM remoteAltimeterFlag WHERE flag = (?)',
                (self.remoteAltimeterFlag,))
            remoteAltimeterFlag_id = self.c.fetchone()[0]
            self.c.execute('''UPDATE PF SET 
                                    LVnavLevelOfService = (?),
                                    LnavLevelOfService = (?),
                                    remoteAltimeterFlag_id = (?),
                                    LVnavAuth_id = (?),
                                    LnavAuth_id = (?),
                                    RNPAuth1_id = (?),
                                    RNPAuth2_id = (?),
                                    RNPAuth3_id = (?),
                                    RNPAuth4_id = (?),
                                    RNPLevelOfService1 = (?),
                                    RNPLevelOfService2 = (?),
                                    RNPLevelOfService3 = (?),
                                    RNPLevelOfService4 = (?)
                                  WHERE SidStarApproachIdent = (?)''',
                           (self.LVnavLevelOfService, self.LnavLevelOfService,
                            remoteAltimeterFlag_id,
                            LVnavAuth_id, LnavAuth_id, RNPAuth1_id,
                            RNPAuth2_id, RNPAuth3_id, RNPAuth4_id,
                            self.RNPLevelOfService1, self.RNPLevelOfService2,
                            self.RNPLevelOfService3,
                            self.RNPLevelOfService4,
                            self.SidStarApproachIdent))

    def localizerIdent_line(self):  # PI lines
        self.c.execute('SELECT id FROM navaid WHERE ident = ?',
                       (self.navaid,))
        navaid_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM IcaoCode WHERE code = ?',
                       (self.airHeli_GeoIcao,))
        airHeli_GeoIcao_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM PA WHERE airHeli_portIdent = ?',
                       (self.airHeli_portIdent,))
        airHeli_portIdent_id = self.c.fetchone()[0]
        self.c.execute('SELECT id FROM ILScategory WHERE category = ?',
                       (self.ILScategory,))
        ILScategory_id = self.c.fetchone()[0]
        sectionCode_id = self._standard_selects(self.section, self.subsection)[
            0]
        areaCode_id = self._standard_selects(self.section, self.subsection)[1]
        self.c.execute('''INSERT OR IGNORE INTO PI (
                                     airHeli_portIdent_id,
                                     airHeli_GeoIcao_id,
                                     latitude,
                                     longitude,
                                     navaid_id,
                                     ILScategory_id,
                                     localizerFreq,
                                     runwayIdent,
                                     areaCode_id,
                                     sectionCode_id,
                                     file_rec,
                                     cycle_date)
                           VALUES (?, ?, ?, ?, ?, ?,
                                   ?, ?, ?, ?, ?, ?);''',
                       (airHeli_portIdent_id, airHeli_GeoIcao_id,
                        self.latitude, self.longitude, navaid_id,
                        ILScategory_id, self.localizerFreq, self.runwayIdent,
                        areaCode_id, sectionCode_id, self.fileRecord,
                        self.fileCycle))
