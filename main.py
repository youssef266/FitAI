#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, request, render_template, session, redirect, url_for, flash
from models.user import Users, Session
from models.programs import Programs
from groq import Groq
from functools import wraps

app = Flask(__name__)
mysession = Session()
app.secret_key = 'thisissecret'

# Decorator to ensure login is required for specific routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function


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
@login_required
def service():
    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    return render_template('content/service.html', name=user.name, age=user.age, gender=user.gender,weight=user.weight, height=user.height)


@app.route('/service/generated', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def AI_service():
    if request.method == 'POST':
        program_type = request.form['program_type']
        name = request.form['user_name']
        age = request.form['user_age']
        gender = request.form['user_gender']
        weight = request.form['user_weight']
        height = request.form['user_height']
        prompt = f"give to me a. {program_type} my name is. {name} my age is. {age} my gender is. {gender} my weight is. {weight}Kg my height is. {height}cm"

    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()

    client = Groq(api_key="your_api_key")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-70b-versatile",
        max_tokens=1000
    )
    data = chat_completion.choices[0].message.content

    return render_template('content/AI_Genrated.html', data=data, name=user.name, user_id=user.id)


@app.route('/service/save', methods=['GET', 'POST'], strict_slashes=False)
@login_required
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
    if 'user_id' in session:
        userid = session['user_id']
        user = mysession.query(Users).filter_by(id=userid).first()    
        return render_template('content/register.html', name=user.name)
    
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
        weight = request.form['weight']
        height = request.form['height']

        if password != conf_password:
            return render_template('content/register.html', error='Passwords do not match', new_name=name, new_email=email, new_age=age, new_gender=gender, new_weight=weight, new_height=height)
        else:
            new_user = Users(name=name, email=email, password=password, conf_password=conf_password, age=age, gender=gender, weight=weight, height=height)
            mysession.add(new_user)
            mysession.commit()
            return redirect(url_for('login'))


@app.route('/edit', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def edit():
    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    return render_template('content/edit.html', name=user.name, email=user.email, age=user.age, gender=user.gender,weight = user.weight, height = user.height ,password=user.password, conf_password=user.conf_password)


@app.route('/edit/submit', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def edit_submit():
    userid = session['user_id']
    user_to_update = mysession.query(Users).filter_by(id=userid).first()

    if user_to_update:
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.age = request.form['age']
        user_to_update.gender = request.form['gender']
        user_to_update.weight = request.form['weight']
        user_to_update.height = request.form['height']
        user_to_update.password = request.form['password']
        user_to_update.conf_password = request.form['conf_password']
        mysession.commit()

    flash('User updated successfully!', 'success')
    return redirect(url_for('account'))


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
            return redirect(url_for('home')) 
        else:
            return render_template('content/login.html', error='Invalid email or password')


@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    session.pop('user_id', None)
    
    return redirect(url_for('home'))


@app.route('/account', strict_slashes=False)
@login_required
def account():
    userid = session['user_id']
    user = mysession.query(Users).filter_by(id=userid).first()
    return render_template('content/account.html', name=user.name, email=user.email, age=user.age)


@app.route('/programs', strict_slashes=False)
@login_required
def programs():
    userid = session.get('user_id')
    user = mysession.query(Users).filter_by(id=userid).first()

    # Pagination logic here...
    page = request.args.get('page', 1, type=int)
    per_page = 3
    programs_query = mysession.query(Programs).filter_by(user_id=userid)
    total_programs = programs_query.count()
    programs = programs_query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total_programs + per_page - 1) // per_page

    return render_template('content/programs.html', name=user.name, programs=[program.program_text for program in programs], page=page, total_pages=total_pages)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
