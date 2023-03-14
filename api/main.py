import io
import base64
import time
from PIL import Image
import qrcode
from solana.rpc.api import Client
def build(publickey,amount,INVOICENUMBER):
    return f"solana:{publickey}?amount={amount}&label=Transacts.co&memo={INVOICENUMBER}"


def generate_qr(data):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(back_color="transparent", fill_color="#F07B7B")
    data = io.BytesIO()
    img.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data.decode('utf-8')

def generate_id():
    import secrets

    hash = secrets.token_hex(12)
    return hash

def transaction(publickey,amount,INVOICENUMBER):
    return generate_qr(build(publickey,amount,INVOICENUMBER))


def check_if_payed(invoice_id,wallet):
    solana_client = Client("https://api.mainnet-beta.solana.com")
    for i in solana_client.get_signatures_for_address(wallet)['result']:

        if i['err'] == None:
            if str(invoice_id ) in str(i['memo']):
                return 'Payed'
    return 'Not Payed'
