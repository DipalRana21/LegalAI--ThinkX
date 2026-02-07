"""
Secure User Database Management with SQLite
Uses bcrypt for password hashing and secure storage
"""

import sqlite3
import bcrypt
import os
from pathlib import Path
from datetime import datetime
import json

class UserDatabase:
    def __init__(self, db_path: str = "legal_db/users.db"):
        """Initialize the user database with secure schema"""
        self.db_path = db_path
        
        # Create directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.init_database()
    
    def init_database(self):
        """Create database tables with proper schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table with secure fields
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP
                )
            ''')
            
            # Create index on email for faster lookups
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON users(email)')
            
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Database initialization error: {e}")
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt with salt
        Uses cost factor of 12 for strong security
        """
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against stored hash
        Secure comparison to prevent timing attacks
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def register_user(self, email: str, full_name: str, password: str) -> dict:
        """
        Register a new user with email, name, and password
        Returns success/error message
        """
        try:
            # Validate inputs
            if not email or '@' not in email:
                return {"success": False, "message": "Invalid email format"}
            
            if not full_name or len(full_name.strip()) < 2:
                return {"success": False, "message": "Full name must be at least 2 characters"}
            
            if not password or len(password) < 8:
                return {"success": False, "message": "Password must be at least 8 characters"}
            
            # Check password strength
            if not self._check_password_strength(password):
                return {
                    "success": False, 
                    "message": "Password must contain uppercase, lowercase, digit, and special character"
                }
            
            email = email.lower().strip()
            password_hash = self.hash_password(password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (email, full_name, password_hash)
                VALUES (?, ?, ?)
            ''', (email, full_name.strip(), password_hash))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "User registered successfully"}
        
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Email already registered. Please login or use a different email."}
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}
    
    def login_user(self, email: str, password: str) -> dict:
        """
        Authenticate user with email and password
        Implements account lockout after failed attempts
        """
        try:
            email = email.lower().strip()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, password_hash, is_active, locked_until FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return {"success": False, "message": "Invalid email or password"}
            
            user_id, password_hash, is_active, locked_until = result
            
            # Check if account is locked
            if locked_until:
                from datetime import datetime
                if datetime.fromisoformat(locked_until) > datetime.now():
                    conn.close()
                    return {"success": False, "message": "Account is locked. Try again later."}
            
            # Check if account is active
            if not is_active:
                conn.close()
                return {"success": False, "message": "Account is inactive. Contact support."}
            
            # Verify password
            if not self.verify_password(password, password_hash):
                # Increment failed attempts
                cursor.execute('SELECT failed_attempts FROM users WHERE id = ?', (user_id,))
                failed_attempts = cursor.fetchone()[0] + 1
                
                if failed_attempts >= 5:
                    # Lock account for 30 minutes
                    from datetime import datetime, timedelta
                    locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
                    cursor.execute(
                        'UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?',
                        (failed_attempts, locked_until, user_id)
                    )
                    conn.commit()
                    conn.close()
                    return {"success": False, "message": "Account locked due to multiple failed attempts. Try again in 30 minutes."}
                
                cursor.execute('UPDATE users SET failed_attempts = ? WHERE id = ?', (failed_attempts, user_id))
                conn.commit()
                conn.close()
                return {"success": False, "message": "Invalid email or password"}
            
            # Reset failed attempts on successful login
            from datetime import datetime
            cursor.execute(
                'UPDATE users SET failed_attempts = 0, locked_until = NULL, last_login = ? WHERE id = ?',
                (datetime.now().isoformat(), user_id)
            )
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "Login successful",
                "user_id": user_id,
                "email": email
            }
        
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}
    
    def get_user(self, email: str) -> dict:
        """Get user details by email"""
        try:
            email = email.lower().strip()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT id, email, full_name, created_at, last_login FROM users WHERE email = ?',
                (email,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "id": result[0],
                    "email": result[1],
                    "full_name": result[2],
                    "created_at": result[3],
                    "last_login": result[4]
                }
            return None
        
        except Exception as e:
            raise Exception(f"Error fetching user: {e}")
    
    def change_password(self, email: str, old_password: str, new_password: str) -> dict:
        """Change user password securely"""
        try:
            email = email.lower().strip()
            
            # Verify old password first
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT password_hash FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            
            if not result or not self.verify_password(old_password, result[0]):
                conn.close()
                return {"success": False, "message": "Current password is incorrect"}
            
            # Hash and update new password
            if not self._check_password_strength(new_password):
                conn.close()
                return {"success": False, "message": "New password must be strong"}
            
            new_password_hash = self.hash_password(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE email = ?', (new_password_hash, email))
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "Password changed successfully"}
        
        except Exception as e:
            return {"success": False, "message": f"Password change error: {str(e)}"}
    
    def _check_password_strength(self, password: str) -> bool:
        """
        Check password strength requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character
        """
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        return has_upper and has_lower and has_digit and has_special


# Initialize global database instance
db = UserDatabase()
