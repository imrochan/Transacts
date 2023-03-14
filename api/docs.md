**create_transaction** -> output A with UNIQUE reference number 

**get_qr_code**  -> input A  -> output B as a URL for image  
A. "solana:recipientAddress?amount=amount_in_sol&reference=publicKey&label=Transacts.co&memo=INVOICE-NUMBER"

from flask import Flask, send_file

app = Flask(__name__)

@app.route('/image')
def image():
    return send_file('image.png', mimetype='image/png')

**check_transaction_status** 
based on wallet and invoice number, fetch sol transactions for wallet and go through latest 1000 checking for a memo that matches invoice number

HOST ON PYTHONANYWHERE?