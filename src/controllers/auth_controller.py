from flask import request, session, redirect, url_for, render_template

class AuthController:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def handle_login(self):
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            
            if user and pwd == user[1]:
                session['username'] = user[0]
                return redirect(url_for('main.home'))
            
            return render_template('login.html', error='Invalid credentials')
        
        return render_template('login.html')

    def handle_register(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            pwd = request.form['password']
            
            cur = self.mysql.connection.cursor()
            cur.execute("""
                INSERT INTO users (username, email, password) 
                VALUES (%s, %s, %s)
            """, (username, email, pwd))
            self.mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('auth.login'))
        
        return render_template('register.html')

    def handle_logout(self):
        session.pop('username', None)
        return redirect(url_for('main.home'))