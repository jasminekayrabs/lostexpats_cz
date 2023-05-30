from django.apps import AppConfig
from flask import Flask, request, make_response, render_template, redirect


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'authentication.apps.AuthenticationConfig',
    'django.contrib.staticfiles',

]


app = Flask(__name__)

COOKIE_NAME = 'cookie_preferences'

@app.route('/', methods=['GET', 'POST'])
def index():
    cookie_preferences = request.cookies.get(COOKIE_NAME)

    if cookie_preferences == 'accepted':
        # Cookie preferences accepted, show the main page
        return render_template('index.html')
    
    # Cookie preferences not set or declined, show the cookie consent pop-up
    return render_template('cookie_popup.html')

@app.route('/set_cookie_preferences', methods=['POST'])
def set_cookie_preferences():
    preferences = request.form.get('preferences')

    if preferences in ['accept', 'decline', 'modify']:
        # Set the cookie preferences based on user selection
        response = make_response(render_template('index.html'))

        if preferences == 'accept':
            response.set_cookie(COOKIE_NAME, 'accepted', max_age=30*24*60*60)  # 30 days
        elif preferences == 'decline':
            response.set_cookie(COOKIE_NAME, 'declined', max_age=30*24*60*60)  # 30 days
        elif preferences == 'modify':
            response.set_cookie(COOKIE_NAME, 'modified', max_age=30*24*60*60)
        
        return response
    
    # Invalid preference selection, redirect back to the index page
    return redirect('/')
   
if __name__ == '__main__':
    app.run()
