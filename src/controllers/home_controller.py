from flask import render_template, session

class HomeController:
    def handle_home(self):
        if 'username' in session:
            return render_template('home.html', username=session['username'])
        return render_template('home.html')