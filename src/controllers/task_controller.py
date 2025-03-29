from flask import render_template, request, redirect, url_for, session, flash

class TaskController:
    def __init__(self, mysql):
        self.mysql = mysql
        # Vous pourriez aussi importer et utiliser TaskModel ici
    
    def show_tasks(self):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        
        # Ici vous devriez utiliser TaskModel
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user = cur.fetchone()
        
        if not user:
            return redirect(url_for('auth.login'))
        
        user_id = user[0]
        cur.execute("""
            SELECT id, title, description, status, created_at 
            FROM tasks 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        tasks = cur.fetchall()
        cur.close()
        
        return render_template('tasks.html', tasks=tasks)
    
    def add_task(self):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description', '')
            
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
            user_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO tasks (user_id, title, description) 
                VALUES (%s, %s, %s)
            """, (user_id, title, description))
            self.mysql.connection.commit()
            cur.close()
            
            flash('Tâche ajoutée avec succès!', 'success')
            return redirect(url_for('task.show_tasks'))
        
        return render_template('add_task.html')
    
    def edit_task(self, task_id):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cur.fetchone()[0]
        
        if request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description', '')
            status = request.form.get('status', 'pending')
            
            cur.execute("""
                UPDATE tasks 
                SET title = %s, description = %s, status = %s 
                WHERE id = %s AND user_id = %s
            """, (title, description, status, task_id, user_id))
            self.mysql.connection.commit()
            cur.close()
            
            flash('Tâche mise à jour avec succès!', 'success')
            return redirect(url_for('task.show_tasks'))
        
        cur.execute("""
            SELECT id, title, description, status 
            FROM tasks 
            WHERE id = %s AND user_id = %s
        """, (task_id, user_id))
        task = cur.fetchone()
        cur.close()
        
        if not task:
            flash('Tâche non trouvée', 'error')
            return redirect(url_for('task.show_tasks'))
        
        return render_template('edit_task.html', task=task)
    
    def delete_task(self, task_id):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cur.fetchone()[0]
        
        cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
        self.mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows > 0:
            flash('Tâche supprimée avec succès!', 'success')
        else:
            flash('Tâche non trouvée', 'error')
        
        return redirect(url_for('task.show_tasks'))