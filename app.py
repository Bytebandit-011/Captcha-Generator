#import necessary modules
from flask import Flask, render_template, request
from flask_session_captcha import FlaskSessionCaptcha
import os
from flask_session import Session

#Configuration of the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
#Configures captcha legth and size
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 6
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60

# If using Flask-Session for server-side sessions
app.config['SESSION_TYPE'] = 'filesystem' 

Session(app)
# Initialize the FlaskSessionCaptcha extension with the Flask app
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    
    if request.method == 'POST':
        if captcha.validate():
            message = 'Authentication Approved'
        else:
            message = 'Wrong CAPTCHA Entered'
    
    # Generate a new captcha 
    captcha_html = captcha.generate()
    
    return render_template('form.html', message=message, captcha_html=captcha_html)

if __name__ == '__main__':
    app.run(debug=True)