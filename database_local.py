import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
import json

class LocalDatabaseManager:
    def __init__(self, db_path="shefin_local.db"):
        self.db_path = db_path
        self.init_database()
        print(f"Local SQLite database initialized: {db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL,
                monthly_income REAL NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                target_date DATE NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Learning progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module_name TEXT NOT NULL,
                level TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Mood tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mood_type TEXT NOT NULL,
                mood_intensity INTEGER NOT NULL,
                spending_trigger TEXT,
                notes TEXT,
                amount_spent REAL DEFAULT 0,
                date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name, email, age, monthly_income, password):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, age, monthly_income, password_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, age, monthly_income, password_hash))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, name, email, age, monthly_income
                FROM users 
                WHERE email = ? AND password_hash = ?
            ''', (email, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'age': user[3],
                    'monthly_income': user[4]
                }
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, age, monthly_income
                FROM users 
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'age': user[3],
                    'monthly_income': user[4]
                }
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def update_user_profile(self, user_id, name, age, monthly_income):
        """Update user profile"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET name = ?, age = ?, monthly_income = ?
                WHERE id = ?
            ''', (name, age, monthly_income, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def add_transaction(self, user_id, transaction_type, amount, category, description, date):
        """Add a new transaction"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (user_id, type, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, transaction_type, amount, category, description, date))
            
            transaction_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return transaction_id
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def get_user_transactions(self, user_id, limit=None):
        """Get user transactions"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = '''
                SELECT id, type, amount, category, description, date, created_at
                FROM transactions 
                WHERE user_id = ?
                ORDER BY date DESC, created_at DESC
            '''
            
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            transactions = []
            for row in rows:
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'category': row[3],
                    'description': row[4],
                    'date': row[5],
                    'created_at': row[6]
                })
            
            return transactions
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def create_goal(self, user_id, name, target_amount, target_date, current_amount, category):
        """Create a new financial goal"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO goals (user_id, name, target_amount, target_date, current_amount, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, name, target_amount, target_date, current_amount, category))
            
            goal_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return goal_id
        except Exception as e:
            print(f"Error creating goal: {e}")
            return None
    
    def get_user_goals(self, user_id):
        """Get user financial goals"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, target_amount, current_amount, target_date, category, created_at
                FROM goals 
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            goals = []
            for row in rows:
                goals.append({
                    'id': row[0],
                    'name': row[1],
                    'target_amount': row[2],
                    'current_amount': row[3],
                    'target_date': row[4],
                    'category': row[5],
                    'created_at': row[6]
                })
            
            return goals
        except Exception as e:
            print(f"Error getting goals: {e}")
            return []
    
    def update_goal_progress(self, goal_id, new_amount):
        """Update goal progress"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE goals 
                SET current_amount = ?
                WHERE id = ?
            ''', (new_amount, goal_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating goal progress: {e}")
            return False
    
    def track_learning_progress(self, user_id, module_name, level):
        """Track user's learning progress"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO learning_progress (user_id, module_name, level)
                VALUES (?, ?, ?)
            ''', (user_id, module_name, level))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error tracking learning progress: {e}")
            return False
    
    def get_learning_progress(self, user_id):
        """Get user's learning progress"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT module_name, level, completed_at
                FROM learning_progress 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            progress = []
            for row in rows:
                progress.append({
                    'module_name': row[0],
                    'level': row[1],
                    'completed_at': row[2]
                })
            
            return progress
        except Exception as e:
            print(f"Error getting learning progress: {e}")
            return []
    
    def save_chat_history(self, user_id, message, response):
        """Save chat conversation"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (user_id, message, response)
                VALUES (?, ?, ?)
            ''', (user_id, message, response))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def get_chat_history(self, user_id, limit=10):
        """Get recent chat history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT message, response, created_at
                FROM chat_history 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                history.append({
                    'message': row[0],
                    'response': row[1],
                    'created_at': row[2]
                })
            
            return list(reversed(history))  # Return in chronological order
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []