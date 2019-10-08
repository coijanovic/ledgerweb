from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST', 'GET'])
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

    ledgerfile = open("test.txt","a")
    ledgerfile.write(transdate + c + transrep + "\n")
    ledgerfile.write("    " + fromacc + "          " + fromamount + "\n")
    ledgerfile.write("    " + toacc + "        " + toamount + "\n\n")
    ledgerfile.close()

    return str(response),200


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.221')
