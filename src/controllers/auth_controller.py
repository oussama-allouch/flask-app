from flask import request, session, redirect, url_for, render_template
from models.user_model import UserModel

class AuthController:
    def __init__(self, mysql):
        self.user_model = UserModel(mysql)
    
    def handle_login(self):
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']
            user = self.user_model.get_user_by_username(username)
            
            if user and pwd == user[3]:  # Le mot de passe est à l'index 3 maintenant
                session['username'] = user[1]  # Le username est à l'index 1
                return redirect(url_for('main.home'))
            
            return render_template('login.html', error='Invalid credentials')
        
        return render_template('login.html')

    def handle_register(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            pwd = request.form['password']
            
            self.user_model.create_user(username, email, pwd)
            return redirect(url_for('auth.login'))
        
        return render_template('register.html')

    def handle_logout(self):
        session.pop('username', None)
        return redirect(url_for('main.home'))