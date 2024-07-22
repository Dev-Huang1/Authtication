from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    # Generate a new TOTP secret key for the user
    if 'totp_secret' not in session:
        session['totp_secret'] = pyotp.random_base32()
    
    totp = pyotp.TOTP(session['totp_secret'])
    otp_uri = totp.provisioning_uri(name='user@example.com', issuer_name='YourApp')
    
    # Generate QR code for the TOTP URI
    qr = qrcode.make(otp_uri)
    img = io.BytesIO()
    qr.save(img, 'PNG')
    img_str = base64.b64encode(img.getvalue()).decode('ascii')
    
    return render_template('index.html', img_str=img_str)

@app.route('/validate', methods=['POST'])
def validate():
    token = request.form['token']
    totp = pyotp.TOTP(session['totp_secret'])
    
    if totp.verify(token):
        return 'TOTP validated successfully!'
    else:
        return 'Invalid TOTP. Please try again.'

if __name__ == '__main__':
    app.run(debug=True)
