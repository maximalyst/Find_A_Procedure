# functions to categorize procedures per ARINC-424

class CIFPline:
    def __init__(self, linetext):
        self.linetext = linetext

    def getRecordType(self):
        rectype_id = self.linetext[0]
        if rectype_id = 'A': rectype = 'MORA'
        elif rectype_id = 'D': rectype = 'Navaid'
        elif rectype_id = 'E': rectype = 'Enroute'
        elif rectype_id = 'H': rectype = 'Heliport'
        elif rectype_id = 'P': rectype = 'Airport'
        elif rectype_id = 'R': rectype = 'Company Route'
        elif rectype_id = 'T': rectype = 'Table'
        elif rectype_id = 'U': rectype = 'Airspace'
