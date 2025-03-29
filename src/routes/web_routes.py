from flask import Blueprint
from controllers.auth_controller import AuthController
from controllers.home_controller import HomeController
from controllers.task_controller import TaskController

def init_routes(app, mysql):
    # Création des contrôleurs
    auth_controller = AuthController(mysql)
    home_controller = HomeController()
    task_controller = TaskController(mysql)
    
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
    
    # Blueprint pour les routes des tâches
    task_bp = Blueprint('task', __name__)
    
    @task_bp.route('/tasks')
    def show_tasks():
        return task_controller.show_tasks()
    
    @task_bp.route('/tasks/add', methods=['GET', 'POST'])
    def add_task():
        return task_controller.add_task()
    
    @task_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    def edit_task(task_id):
        return task_controller.edit_task(task_id)
    
    @task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
    def delete_task(task_id):
        return task_controller.delete_task(task_id)
    
    # Enregistrement des Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp, url_prefix='')