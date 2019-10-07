#!/usr/bin/env python3

import cgi

form = cgi.FieldStorage()

transdate = form.getvalue("transdate")
transclear = form.getvalue("transclear")
transrep = form.getvalue("transrep")
fromacc = form.getvalue("fromacc")
fromamount = form.getvalue("fromamount")
toacc = form.getvalue("toacc")
toamount = form.getvalue("toamount")

if transclear == "on":
    c = " * "
else:
    c = " "

if fromamount:
    fromamount = str(fromamount) + " EUR"
else:
    fromamount = ""

if toamount:
    toamount = str(toamount) + " EUR"
else:
    toamount = ""

transdate = transdate.replace("-","/")

ledgerfile = open("test.txt","a")
ledgerfile.write(transdate + c + transrep + "\n")
ledgerfile.write("    " + fromacc + "          " + fromamount + "\n")
ledgerfile.write("    " + toacc + "        " + toamount + "\n\n")
ledgerfile.close()
