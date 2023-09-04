import sqlite3
import os
import DatabaseSetup
import logging
from RecordString import CIFPLine

# Temporary things I'm only allowing for MVP version
ALLOWED_DATA_LINES = ['D ', 'DB', 'PN', 'EA', 'PC', 'ER',
                      'PA', 'PD', 'PE', 'PF', 'PI']  # , 'PG']
ALLOWED_COUNTRY = ['CAN', 'EEU', 'LAM', 'PAC', 'SPA', 'USA']
'''
if os.path.exists('CIFP_parse.sqlite'):
    os.remove('CIFP_parse.sqlite')

logging.basicConfig(filename='parse_log.log', encoding='utf-8',
                    level=logging.DEBUG, filemode='w')

conn = sqlite3.connect('CIFP_parse.sqlite')
cursr = conn.cursor()

DatabaseSetup.table_define(conn)

#############################
k = 0  # counter for commits
# with open('./Private_Files/D_example.txt', 'r') as fh:
with open('./Private_Files/FAACIFP18_Aug23.txt', 'r') as fh:
    # Get the header info first...
    lastspot = fh.tell()  # This "saves" our current position in file stream
    this = fh.readline().rstrip().upper()
    while this[0:3] == 'HDR':
        lastspot = fh.tell()  # we're still in a header line, so update "save"
        this = fh.readline().rstrip().upper()

    # we need to skip back to the first line after the last header line,
    #    because the upcoming ''in fh'' advances ANOTHER line past the last
    #    fh.readline()
    fh.seek(lastspot, 0)

    # now for the part we're all here for
    print('Running, standby...')
    for a in fh:
        k += 1
        rawdata = a.rstrip().upper()
        # In this version we're only dealing with certain datatypes
        if rawdata[4] == 'P':
            if rawdata[4] + rawdata[12] not in ALLOWED_DATA_LINES:
                continue
        elif rawdata[4:6] not in ALLOWED_DATA_LINES:
            continue

        if rawdata[1:4] in ALLOWED_COUNTRY:
            pass
        else:
            continue

        print(rawdata)  # DEBUG
        this = CIFPLine(rawdata, conn)
        # if this.already_exists() is True:
        #     logging.warning('%s', rawdata)
        #     logging.warning('%s already exists in database table %s\n',
        #                     this.hingeValue, this.table_name)
        #     continue
        # Now handle the line since it's "new"
        # try:
        this.record_line()
        # except:
        #     print("oops on that line")
        #     logging.error(this.data)
        #     flag = flag + 1

        # if k == 10:
        #     conn.commit()
        #     k = 0
        #     break  # debug

conn.commit()
conn.close()
'''

USEFILE = './Private_Files/FAACIFP18_Aug23.txt'
DATABASENAME = 'CIFP_parse.sqlite'


def open_the_actual_file(datafile):
    with open(datafile, 'r') as file:
        for line in file:
            if not (line.startswith("HDR") or not (
                    line[1:4] in ALLOWED_COUNTRY)) and (
                    line[4:6] in ALLOWED_DATA_LINES):
                # avoids header lines and grid MORA lines
                yield line.upper().rstrip()


def main():
    if os.path.exists(DATABASENAME):
        os.remove(DATABASENAME)
    # Make the actual database framework first:
    conn = sqlite3.connect(DATABASENAME)
    DatabaseSetup.table_define(conn)

    # Where we're doing the actual work of parsing each line into the database
    for each in open_the_actual_file(USEFILE):
        this = CIFPLine(each, conn)
        this.record_line()
        print(each)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()



