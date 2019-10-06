#!/usr/bin/env python3

import cgi

form = cgi.FieldStorage()

transdate = form.getvalue("transdate")

ledgerfile = open("test.txt","w")
ledgerfile.write(transdate)
ledgerfile.close()
