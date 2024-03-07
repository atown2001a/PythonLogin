from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You should change this to a random secret key

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')

def find_auth_module():
    # List of directories to search
    search_dirs = [
        'C:/Users/Ahmed/Documents/Pass',
        'G:/Pass/Ahmed IT/',
        # Add more directories as needed
    ]

    # Name of the auth module file (without extension)
    auth_module_name = 'auth'

    # Loop through each directory in the search_dirs list
    for directory in search_dirs:
        print("Searching in:", directory)
        # Construct the full path to the auth module file
        auth_module_path = os.path.join(directory, auth_module_name + '.py')
        # Check if the file exists
        if os.path.isfile(auth_module_path):
            print("Auth module file found at:", auth_module_path)
            return auth_module_path  # Return the path if found

    # Return None if the file is not found in any directory
    print("Auth module file not found.")
    return None
@app.route('/', methods=['GET', 'POST'])


def login():
    auth_module_path = find_auth_module()

    if auth_module_path:
        # Import the authenticate function from the auth module
        try:
            from importlib.machinery import SourceFileLoader
            auth_module = SourceFileLoader("auth", auth_module_path).load_module()
            authenticate = auth_module.authenticate
            
            # Debugging output
            print("Authentication module found at:", auth_module_path)

            # Example: Get username and password from the login form
            form = LoginForm(request.form)
            if request.method == 'POST' and form.validate():
                username = form.username.data
                password = form.password.data

                # Call the authenticate function with provided username and password
                if authenticate(username, password):
                    # Authentication succeeded
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    # Authentication failed
                    return render_template('login.html', form=form, error='Invalid username or password')
            else:
                return render_template('login.html', form=form)
        except Exception as e:
            print("Error importing or executing the authenticate function:", e)
    else:
        print("Auth module file not found.")

    form = LoginForm()
    if form.validate_on_submit():
        if authenticate(form.username.data, form.password.data):
            session['username'] = form.username.data
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form, error='Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
