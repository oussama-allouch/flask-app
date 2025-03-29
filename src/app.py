from flask import Flask
from flask_mysqldb import MySQL
from routes.web_routes import init_routes

app = Flask(__name__,
           template_folder='./templates',
           static_folder='./static')
app.secret_key = 'your-secret-key'

# Configuration MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_auth'

mysql = MySQL(app)

# Initialisation des routes
init_routes(app, mysql)

if __name__ == '__main__':
    app.run(debug=True)