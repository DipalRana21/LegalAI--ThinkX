# 🔐 NyayaSahayak Authentication System

## Overview

Your legal AI application now has a **secure, production-ready authentication system** with the following features:

### ✅ Security Features Implemented

1. **Password Hashing with bcrypt**
   - Uses bcrypt with 12-round salt rounds (OWASP standard)
   - Passwords are never stored in plain text
   - Secure comparison prevents timing attacks

2. **Password Strength Requirements**
   - Minimum 8 characters
   - Must contain uppercase and lowercase letters
   - Must contain at least one number
   - Must contain at least one special character (!@#$%^&*)
   - Real-time strength indicator during signup

3. **Account Security**
   - Account lockout after 5 failed login attempts
   - 30-minute lockout timer to prevent brute force attacks
   - Failed attempt tracking
   - Login timestamp recording

4. **Data Storage**
   - SQLite database with encrypted password hashes
   - Email uniqueness validation
   - User session management with Streamlit
   - Proper database indexing for performance

5. **Session Management**
   - Secure session state in Streamlit
   - Automatic logout functionality
   - User information tracking
   - Protected pages (only accessible after login)

---

## 📁 Project Structure

```
project-root/
├── frontend/
│   ├── app.py                 # Main legal AI assistant (protected)
│   └── authenticated_app.py   # Auth gateway (entry point)
├── backend/
│   ├── __init__.py
│   ├── database.py            # User database management
│   ├── auth.py                # Authentication logic
│   └── ...
├── legal_db/
│   ├── users.db              # User database (auto-created)
│   └── ...
├── run.py                     # Updated to use authenticated_app.py
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

Or directly with Streamlit:
```bash
streamlit run frontend/authenticated_app.py
```

### 3. First Access
1. Open your browser (typically http://localhost:8501)
2. Click **"📝 Create Account"** to sign up
3. Fill in your details:
   - Full Name
   - Email Address
   - Strong Password (with uppercase, lowercase, number, special char)
4. After signup, login with your credentials
5. Access the main legal AI assistant

---

## 🔑 Password Requirements

Users must create passwords with:
- ✅ At least **8 characters**
- ✅ **Uppercase** letters (A-Z)
- ✅ **Lowercase** letters (a-z)
- ✅ **Numbers** (0-9)
- ✅ **Special characters** (!@#$%^&*()_+-=[]{}|;:,.<>?)

**Example valid passwords:**
- `Legal@123Info`
- `NyayaSahay@1k`
- `SecurePass#456`

---

## 🗄️ Database Structure

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,          -- bcrypt hash
    created_at TIMESTAMP DEFAULT NOW,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0,   -- Brute force protection
    locked_until TIMESTAMP                -- Account lockout timer
)
```

**Indexes:**
- `email` - For fast login lookups

---

## 🔒 Security Details

### Password Hashing
- Algorithm: bcrypt
- Salt rounds: 12 (industry standard)
- Automatic salt generation
- One-way hashing (cannot be reversed)

### Attack Prevention
1. **Brute Force Protection:**
   - Account locks after 5 failed attempts
   - 30-minute lock duration
   - User notification on lockout

2. **SQL Injection Prevention:**
   - Parameterized queries throughout
   - No string concatenation in SQL

3. **Timing Attack Prevention:**
   - Constant-time password comparison
   - Consistent response times

4. **Session Security:**
   - Streamlit session state for user tracking
   - No sensitive data stored in browser
   - Automatic logout option

---

## 📖 API Documentation

### Backend Modules

#### `database.py` - User Database Management

```python
from backend.database import db

# Register new user
result = db.register_user(
    email="user@example.com",
    full_name="John Doe",
    password="SecurePass@123"
)
# Returns: {"success": bool, "message": str}

# Login user
result = db.login_user(
    email="user@example.com",
    password="SecurePass@123"
)
# Returns: {"success": bool, "message": str, "user_id": int, "email": str}

# Get user details
user = db.get_user(email="user@example.com")
# Returns: {"id": int, "email": str, "full_name": str, ...}

# Change password (requires old password)
result = db.change_password(
    email="user@example.com",
    old_password="SecurePass@123",
    new_password="NewSecure@456"
)
```

#### `auth.py` - Authentication Manager

```python
from backend.auth import AuthManager

# Initialize session (automatic in app)
AuthManager.init_session()

# Login
success, message = AuthManager.login(email, password)

# Signup
success, message = AuthManager.signup(email, name, password, confirm_password)

# Check authentication
is_auth = AuthManager.is_authenticated()

# Logout
AuthManager.logout()

# Get current user
user = AuthManager.get_current_user()
# Returns: {"id": int, "email": str, "name": str}
```

---

## 🎨 UI/UX Features

### Login Page
- Clean, professional design
- Email and password inputs
- Clear error messages
- Link to create account

### Signup Page
- Full name, email, password fields
- Real-time password strength indicator:
  - 🔴 Weak (0-60%)
  - 🟡 Medium (60-80%)
  - 🟢 Strong (80-100%)
- Password requirements displayed
- Confirmation password field
- Back button to login page

### Authenticated Sidebar
- Shows logged-in user name and email
- Logout button
- Visual indicator of authentication status

---

## 🛡️ Best Practices Used

1. **OWASP Compliance:**
   - Proper password hashing (bcrypt)
   - Account lockout mechanisms
   - Input validation
   - Secure session management

2. **Error Handling:**
   - Generic error messages to users (don't reveal DB structure)
   - Proper exception catching
   - Transaction integrity

3. **Performance:**
   - Database indexes on frequently queried fields
   - Connection pooling with SQLite
   - Efficient query execution

4. **Code Quality:**
   - Type hints throughout
   - Comprehensive docstrings
   - Clear error messages
   - Modular architecture

---

## 🚨 Important Security Notes

### For Production Deployment:
1. **Enable HTTPS** - All data transmitted encrypted
2. **Use environment variables** for sensitive config
3. **Implement database backups** for user data
4. **Add rate limiting** on login endpoint
5. **Use secure session cookies** with HTTPOnly flag
6. **Implement 2FA** (optional but recommended)
7. **Regular security audits** of the codebase
8. **Compliance check** with data protection laws (GDPR, etc.)

### Current Setup (Development):
- SQLite database (suitable for development)
- For production, consider PostgreSQL or MySQL
- Add OAuth2 integration for social login
- Implement JWT tokens for API security

---

## 🔄 User Flow Diagram

```
[Unauthenticated User Arrives]
           ↓
    [Login/Signup Page]
           ↓
    [User has account?]
      ↙        ↘
   YES         NO
    ↓          ↓
  LOGIN    SIGNUP
    ↓          ↓
    ← ← ← ← ← ←
           ↓
   [Credentials Valid?]
      ↙        ↘
    YES        NO
     ↓         ↓
   [Auth]   [Error]
     ↓         ↓
     ← ← ← ← ←
           ↓
  [Main Legal AI App]
  (authenticated user)
           ↓
    [Use Features]
           ↓
      [Logout]
           ↓
   [Back to Home]
```

---

## 📞 Troubleshooting

### "Email already registered"
- Use a different email address or reset your password

### "Account is locked"
- Wait 30 minutes after 5 failed login attempts
- Contact support if you forget your password

### "Password must contain..."
- Ensure password has uppercase, lowercase, number, and special character

### Database Connection Error
- Ensure `legal_db/` directory exists (auto-created)
- Check file permissions
- Verify SQLite is installed

---

## 📋 Future Enhancements

- [ ] Email verification for new accounts
- [ ] Password reset via email
- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, GitHub)
- [ ] User profile management
- [ ] Activity logging
- [ ] Admin panel for user management
- [ ] OAuth2 implementation
- [ ] Advanced analytics

---

## ✉️ Support

For issues or questions about the authentication system, please check:
1. Database permissions
2. Password requirements
3. Browser compatibility
4. Streamlit version compatibility (1.54+)

---

**Created with 🔐 Security in Mind**

Last Updated: February 7, 2026
