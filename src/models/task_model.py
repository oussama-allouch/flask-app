class TaskModel:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def create_task(self, user_id, title, description, status='pending'):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tasks (user_id, title, description, status) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, title, description, status))
        self.mysql.connection.commit()
        task_id = cur.lastrowid
        cur.close()
        return task_id
    
    def get_user_tasks(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            SELECT id, title, description, status, created_at, updated_at 
            FROM tasks 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        tasks = cur.fetchall()
        cur.close()
        return tasks
    
    def update_task(self, task_id, user_id, title=None, description=None, status=None):
        updates = []
        params = []
        
        if title:
            updates.append("title = %s")
            params.append(title)
        if description:
            updates.append("description = %s")
            params.append(description)
        if status:
            updates.append("status = %s")
            params.append(status)
        
        if not updates:
            return False
        
        params.extend([task_id, user_id])
        
        query = "UPDATE tasks SET " + ", ".join(updates) + " WHERE id = %s AND user_id = %s"
        
        cur = self.mysql.connection.cursor()
        cur.execute(query, tuple(params))
        self.mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        return affected_rows > 0
    
    def delete_task(self, task_id, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        self.mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        return affected_rows > 0