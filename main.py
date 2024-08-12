#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, request , render_template, session,redirect,url_for
from models.user import Users, Session
from models.programs import Programs
from groq import Groq

app = Flask(__name__)
mysession = Session()
app.secret_key = 'thisissecret'

@app.route('/home', strict_slashes=False)
@app.route('/', strict_slashes=False)
def home():
    if 'user_id' not in session:
        return render_template('content/home.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    

    return render_template('content/home.html', name=user.name)

@app.route('/about', strict_slashes=False)
def about():
    if 'user_id' not in session:
        return render_template('content/about.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    
    return render_template('content/about.html', name=user.name)

@app.route('/service', methods=['GET', 'POST'], strict_slashes=False)
def service():
    if 'user_id' not in session:
        return render_template('content/service.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()

    return render_template('content/service.html', name=user.name , age=user.age , gender = user.gender)

@app.route('/service/generated', methods=['GET', 'POST'], strict_slashes=False)
def AI_service():
    if request.method == 'POST':
        program_type = request.form['program_type']
        name = request.form['user_name']
        age = request.form['user_age']
        gender = request.form['user_gender']
        prompt = f"give to me a. {program_type} my name is. {name} my age is. {age} my gender is. {gender}"

    if 'user_id' not in session:
        return render_template('content/AI_Genrated.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    
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

    return render_template('content/AI_Genrated.html',data=data, name=user.name, user_id=user.id)

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
    if 'user_id' not in session:
        return render_template('content/register.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()    
    return render_template('content/register.html', name=user.name)
    
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
    if 'user_id' not in session:
        return render_template('content/login.html')

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    return render_template('content/login.html', name=user.name)

@app.route('/login_save', methods=['GET', 'POST'], strict_slashes=False)
def login_save():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mysession.query(Users).filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            return render_template('content/home.html', name=user.name)
        else:
            return render_template('content/login.html', error ='Invalid email or password. Please try again.')

@app.route('/logout', methods=['GET', 'POST'],strict_slashes=False)
def logout():
    session.pop('user_id', None)
    return render_template('content/home.html')

@app.route('/account', strict_slashes=False)
def account():
    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    return render_template('content/account.html',name = user.name , email = user.email , age = user.age )


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
