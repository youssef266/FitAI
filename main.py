#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, request , render_template, session,redirect,url_for
import requests
from models.user import Users, Session
from models.programs import Programs
from groq import Groq

app = Flask(__name__)
mysession = Session()
app.secret_key = 'thisissecret'

@app.route('/home', strict_slashes=False)
@app.route('/', strict_slashes=False)
def home():
    return render_template('content/home.html')

@app.route('/about', strict_slashes=False)
def about():
    return render_template('content/about.html')

@app.route('/service', methods=['GET', 'POST'], strict_slashes=False)
def service():
    return render_template('content/service.html')

@app.route('/service/generated', methods=['GET', 'POST'], strict_slashes=False)
def AI_service():
    if request.method == 'POST':
        prompt = request.form['prompt']

    client = Groq(
            api_key="your_api_key",
        )
        
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",
        )
    data = chat_completion.choices[0].message.content

    return render_template('content/AI_Genrated.html',data=data)

@app.route('/service/save', methods=['GET', 'POST'], strict_slashes=False)
def service_save():
    if request.method == 'POST':
        user_id = request.form['user_id']
        program_text = request.form['program_text']
    
    new_program = Programs(user_id=user_id, program_text=program_text)
    mysession.add(new_program)
    mysession.commit()
    return redirect(url_for('service'))

@app.route('/register', strict_slashes=False)
def register():    
    return render_template('content/register.html')
    
@app.route('/register/submit', methods=['GET', 'POST'], strict_slashes=False)
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        age = request.form['age']
        gender = request.form['gender']

        if password != conf_password:
            return "Password and confirmation password do not match. Please try again."

        new_user = Users(name=name, email=email, password=password, conf_password=conf_password, age=age, gender=gender)
        mysession.add(new_user)
        mysession.commit()

        return render_template('content/login.html')
    
    if request.method == 'GET':
        return render_template('content/register.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)

def login():
    return render_template('content/login.html')

@app.route('/login_save', methods=['GET', 'POST'], strict_slashes=False)
def login_save():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mysession.query(Users).filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            return render_template('content/home.html')
        else:
            return render_template('content/login.html', error ='Invalid email or password. Please try again.')




if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
