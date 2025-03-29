class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def get_user_by_username(self, username):
        """Récupère un utilisateur par son nom d'utilisateur"""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def create_user(self, username, email, password):
        """Crée un nouvel utilisateur"""
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (username, email, password) 
            VALUES (%s, %s, %s)
        """, (username, email, password))
        self.mysql.connection.commit()
        cur.close()
        return True
    
    # Vous pouvez ajouter d'autres méthodes selon les besoins, par exemple:
    def get_user_by_email(self, email):
        """Récupère un utilisateur par son email"""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def update_user_password(self, user_id, new_password):
        """Met à jour le mot de passe d'un utilisateur"""
        cur = self.mysql.connection.cursor()
        cur.execute("""
            UPDATE users SET password = %s WHERE id = %s
        """, (new_password, user_id))
        self.mysql.connection.commit()
        cur.close()
        return True