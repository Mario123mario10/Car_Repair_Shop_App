from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory user database for demonstration purposes
users = [
    {'username': 'mechanic1', 'password': 'mechpass1', 'role': 'mechanic'},
    {'username': 'admin1', 'password': 'adminpass1', 'role': 'administrator'},
    {'username': 'client1', 'password': 'clientpass1', 'role': 'client'}
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if authenticate_user(username, password, role):
            return redirect(url_for('dashboard', role = role))  # Redirect to the appropriate dashboard based on the role
        else:
            error_message = 'Invalid credentials. Please try again.'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        street = request.form['street']
        house_number = request.form['house_number']
        apartment_number = request.form['apartment_number']
        zip_code = request.form['zip_code']
        city = request.form['city']
        country = request.form['country']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        
        # Perform validation
        if not (street and house_number and zip_code and city and country and first_name and last_name and phone_number and email and password):
            error_message = 'Not all required fields are completed.'
            return render_template('register.html', error_message=error_message)

        # Register the user as a client
        user = {
            'username': email,
            'password': password,
            'role': 'client'
        }
        users.append(user)

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard/<role>')
def dashboard(role):
    # Replace this logic with your own implementation to retrieve the currently logged-in user
    if role== 'mechanic':
        return render_template('mechanic_dashboard.html')
    elif role == 'administrator':
        return render_template('admin_dashboard.html')
    else:
        return render_template('client_dashboard.html')

def authenticate_user(username, password, role):
    for user in users:
        if user['username'] == username and user['password'] == password and user['role'] == role:
            return True
    return False

if __name__ == '__main__':
    app.run()
