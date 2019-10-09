from flask import Flask, render_template, request, redirect, url_for
import subprocess

with open('accounts.txt', 'r') as f:
    ac = f.read().splitlines()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ac=ac)

@app.route('/submit', methods = ['GET'])
def submit():
    transdate = request.args.get('transdate') 
    transclear = request.args.get('transclear') 
    transrep = request.args.get('transrep') 
    fromacc = request.args.get('fromacc') 
    fromamount = request.args.get('fromamount') 
    toacc = request.args.get('toacc') 
    toamount = request.args.get('toamount') 

    response = ('okay', str(transdate))
    
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

    ledgerfile = open("lweb.ledger","a")
    ledgerfile.write(transdate + c + transrep + "\n")
    ledgerfile.write("    " + fromacc + "          " + fromamount + "\n")
    ledgerfile.write("    " + toacc + "        " + toamount + "\n\n")
    ledgerfile.close()
    
    r = subprocess.call("rclone sync lweb.ledger Nextcloud:/accounting/", shell = True)
    return redirect(url_for('index'))

@app.route('/reports')
def reports():
    r = subprocess.call("rclone sync Nextcloud:/accounting data/", shell = True)
    
    reps = []
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger -C Assets", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger Expenses -U --register-format \"%D %P - %A - %T\n\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger Expenses -C --period=\"this month\" --period-sort \"(amount)\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger Expenses -C --period=\"last month\" --period-sort \"(amount)\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger ^Expenses ^Income -n -M --register-format \"%D %P %A  %T\n\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger Income -Y --register-format \"%A  %T\n\"", shell = True).decode("utf-8"))

    return render_template('reports.html', reps=reps)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
