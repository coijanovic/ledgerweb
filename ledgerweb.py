from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os.path
import yaml
import time

if os.path.exists('config.yaml'):
    configfile = 'config.yaml'
else:
    configfile = 'defaultconfig.yaml'

with open(configfile, 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

app = Flask(__name__)

@app.route('/input')
def input():
    cmd = "rclone sync {rname}:{rpath}/finance.ledger  data/".format(rname=config['remotename'], rpath=config['remotepath'])
    r = subprocess.call(cmd, shell=True)

    return render_template('input.html', ac=config['accounts'])

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

    ledgerfile = open("./data/finance.ledger","a")
    ledgerfile.write(transdate + c + transrep + "\n")
    ledgerfile.write("    ; generated by ledgerweb\n")
    ledgerfile.write("    " + fromacc + "          " + fromamount + "\n")
    ledgerfile.write("    " + toacc + "        " + toamount + "\n\n")
    ledgerfile.close()

    cmd = "rclone sync data/finance.ledger {rname}:{rpath}".format(rname=config['remotename'], rpath=config['remotepath'])
    
    r = subprocess.call(cmd, shell = True)
    return redirect(url_for('input'))

@app.route('/reports')
def reports():
    cmd = "rclone sync {rname}:{rpath} data/".format(rname=config['remotename'], rpath=config['remotepath'])
    r = subprocess.call(cmd, shell = True)
    
    reps = []
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger -C Assets", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger Expenses -U --register-format \"%D %P - %A - %T\n\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger Expenses -C --period=\"this month\" --period-sort \"(amount)\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger bal -f ./data/finance.ledger Expenses -C --period=\"last month\" --period-sort \"(amount)\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger ^Expenses ^Income -n -M --register-format \"%D %P %A  %T\n\"", shell = True).decode("utf-8"))
    reps.append(subprocess.check_output("ledger reg -f ./data/finance.ledger Income -Y --register-format \"%A  %T\n\"", shell = True).decode("utf-8"))

    return render_template('reports.html', reps=reps)

@app.route('/')
def favorites():
    favs = list(config['favs'].keys())

    return render_template('index.html', favs=favs)

@app.route('/fsubmit', methods = ['GET'])
def fsubmit():
    amount = request.args.get('famount')
    rep = request.args.get('fselect')

    print(amount + " " + rep)
    cmd = "rclone sync {rname}:{rpath} data/".format(rname=config['remotename'], rpath=config['remotepath'])
    r = subprocess.call(cmd, shell = True)
    
    ledgerfile = open('data/finance.ledger', 'a')
    ledgerfile.write("{date} {rep}\n".format(date=time.strftime("%Y/%m/%d"), rep=rep))
    ledgerfile.write("    ; generated by ledgerweb\n")
    ledgerfile.write("    {f}\n".format(f=config['favs'][rep]['from']))
    ledgerfile.write("    {to}   {amount}\n\n".format(to=config['favs'][rep]['to'], amount=amount))
    ledgerfile.close()

    cmd = "rclone sync data/finance.ledger {rname}:{rpath}".format(rname=config['remotename'], rpath=config['remotepath'])
    r = subprocess.call(cmd, shell = True)

    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(debug=False, host=config['hostip'], port=config['hostport'])
