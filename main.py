from flask import Flask, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
import requests
from decimal import Decimal
import api.main as api
mysql = MySQL()
app = Flask(__name__)


#app.config["MYSQL_DATABASE_USER"] = "transacts"
#app.config["MYSQL_DATABASE_PASSWORD"] = "SQLDATABASE"
#app.config["MYSQL_DATABASE_DB"] = "transacts$db"
#app.config["MYSQL_DATABASE_HOST"] = "transacts.mysql.pythonanywhere-services.com"

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"


mysql.init_app(app)


app = Flask(__name__)



app.secret_key = "123456"



@app.route('/', methods =["POST", "GET"])
def formAdd():
    if request.method == "POST":
        wallet = request.form.get("wallet")
        amount = request.form.get("amount")
        des = request.form.get("description")

        


        
        id = api.generate_id()

        conn = mysql.connect()
        cur = conn.cursor()

        invoice_id = id
        print(amount)

        cur.execute(''' select * from form where invoice_id=%s ;''',[invoice_id])
        invoice_idd = cur.fetchone()

        if invoice_id != None:
            cur.execute(''' insert into form (wallet,amount,des,invoice_id) values(%s,%s,%s,%s);''',[wallet,amount,des,invoice_id])
            conn.commit()
            cur.close()
            conn.close()
            session["message"] = "Invoice Has Been added Successfully"


            return redirect("/form-invoice"+ "?"+"invoice_id"+ "="+str(invoice_id))
        else:
            session["message"] = "Try Again Please"
            return redirect("/form-invoice")


    else:

        return render_template("index.html")


@app.route('/form-invoice', methods =["POST", "GET"])
def formInvoice():
    invoice_id = request.args.get("invoice_id")
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(""" select * from form where invoice_id=%s ;""",[invoice_id])
    data = cur.fetchone()
    print(data)
    amount = float(data[2])
    des = data[3]
    id = invoice_id
    usd = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd').json()['solana']['usd']
    dollars = round(float(amount * usd),2)

    des = des.split('\n')


    if api.check_if_payed(id, data[1]) == 'Payed':
        notpaiD = 'Paid'
        style = 'paid'

    else:
        notpaiD = 'Not Paid'
        style = 'notpaid'









    print(data)
    cur.close()
    conn.close()
    print(data)

    return render_template("invoice.html",notpaid=notpaiD,amountinsol=float(amount), des=des, style=style,dollaramt=dollars, wallet = data[1], invoice_number=data[4],imgdata=api.transaction(data[1],amount,id))









if __name__=="__main__":
    app.run(debug=False)