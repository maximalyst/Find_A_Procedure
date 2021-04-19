import sqlite3
import os
import DatabaseSetup
from RecordString import CIFPLine

if os.path.exists('CIFP_parse.sqlite'):
    os.remove('CIFP_parse.sqlite')

conn = sqlite3.connect('CIFP_parse.sqlite')
cursr = conn.cursor()

# Versions:
# 0.1, 0.2 and 0.3 just got basic syntax errors ironed out, and tweaks
# 0.4 is splitting out the setup and parsing into different files

DatabaseSetup.table_define(conn)

#############################
k = 0 # counter for commits

with open('./Private_Files/FAACIFP18_full.txt', 'r') as fh:
    # Get the header info first...
    lastspot = fh.tell()  # This "saves" our current position in file stream
    this = fh.readline().rstrip().upper()
    while this[0:3] == 'HDR':
        print(this[0:5])
        lastspot=fh.tell()  # we're still in a header line, so update "save"
        this = fh.readline().rstrip().upper()

    # we need to skip back to the first line after the last header line,
    #    because the upcoming '''in fh''' advances ANOTHER line past the last
    #    fh.readline()
    fh.seek(lastspot, 0)

    # now for the part we're all here for
    for a in fh:
        k += 1

        # RecordString.parse_cifp_line(this)
        this = CIFPLine(a.rstrip().upper(), conn)

        print('Got through the loop once!')
        print(this.data)
        break
        # if k == 10:
        #     conn.commit()
        #     k = 0

conn.close()
