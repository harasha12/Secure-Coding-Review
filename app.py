from flask import Flask, request, redirect, render_template_string, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simulated user database (store hashed password)
users = {
    'admin': generate_password_hash('admin123')  # Hash the password
}

@app.route('/')
def home():
    return '<h2>Welcome! Go to <a href="/login">/login</a></h2>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username', '')
        pwd = request.form.get('password', '')

        # Input validation
        if user not in users:
            return 'User not found'

        if check_password_hash(users[user], pwd):
            session['user'] = user  # Secure session
            return redirect('/upload')
        else:
            return 'Invalid credentials'
    
    return '''
    <form method="POST">
        Username: <input name="username" required><br>
        Password: <input name="password" type="password" required><br>
        <input type="submit">
    </form>
    '''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        f = request.files['file']
        if f.filename == '':
            return 'No selected file'

        filename = secure_filename(f.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(file_path)

        return f"File {filename} uploaded successfully."
    
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required><br>
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=False)  # Turn OFF debug mode in production
