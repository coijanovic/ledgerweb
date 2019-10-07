#!/usr/bin/env python3

import cgi

form = cgi.FieldStorage()

transdate = form.getvalue("transdate")
transclear = form.getvalue("transclear")
transrep = form.getvalue("transrep")
fromacc = form.getvalue("fromacc")
fromamount = form.getvalue("fromamount")
toacc = form.getvalue("toacc")

if transclear == "on":
    c = " * "
else:
    c = " "

transdate = transdate.replace("-","/")

ledgerfile = open("test.txt","a")
ledgerfile.write(transdate + c + transrep + "\n")
ledgerfile.write("    " + fromacc + "          " + fromamount + " EUR\n")
ledgerfile.write("    " + toacc + "\n\n")
ledgerfile.close()
