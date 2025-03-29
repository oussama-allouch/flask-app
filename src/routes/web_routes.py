from flask import Blueprint
from controllers.auth_controller import AuthController
from controllers.home_controller import HomeController

def init_routes(app, mysql):
    # Création des contrôleurs
    auth_controller = AuthController(mysql)
    home_controller = HomeController()
    
    # Blueprint pour les routes d'authentification
    auth_bp = Blueprint('auth', __name__)
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        return auth_controller.handle_login()
        
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        return auth_controller.handle_register()
        
    @auth_bp.route('/logout')
    def logout():
        return auth_controller.handle_logout()
    
    # Blueprint pour les routes principales
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def home():
        return home_controller.handle_home()
    
    # Enregistrement des Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)