#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

db_str = 'dnssrf.db'

conn = sqlite3.connect(db_str)

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE logmessage
             (logtimestamp text, src_ip text,iplocation text,datatype text,hostname text,fulldata text,isshow integer)''')


# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
