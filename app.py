from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import initialize_database, create_user, get_user_by_email, database
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

initialize_database(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        create_user(email, password)
        flash('Conta criada com sucesso! Você pode fazer login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)

        if user and bcrypt.check_password_hash(user[2], password):  # user[2] é a senha
            login_user(User(user[0]))  # user[0] é o id
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Bem-vindo, {current_user.id}! Aqui está o seu painel.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
