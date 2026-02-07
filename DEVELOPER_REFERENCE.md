# 👨‍💻 Developer Quick Reference

Quick reference for developers working with the authentication system.

---

## 📁 Directory Structure

```
project/
├── backend/
│   ├── __init__.py
│   ├── auth.py              ← Authentication & UI
│   ├── database.py          ← User DB & password hashing
│   ├── config.py
│   ├── pdf_processor.py
│   └── ...
├── frontend/
│   ├── __init__.py
│   ├── app.py               ← Main legal AI app
│   └── authenticated_app.py ← Auth gateway (entry point)
├── legal_db/
│   ├── users.db             ← User database (auto-created)
│   └── ...
├── run.py                   ← Start here: python run.py
├── requirements.txt
├── SETUP.md                 ← Quick start guide
├── AUTHENTICATION.md         ← Full documentation
├── TESTING.md               ← Test cases
└── IMPLEMENTATION_SUMMARY.md← What was built
```

---

## 🔑 Core Imports

```python
# Authentication
from backend.auth import AuthManager, render_auth_page

# Database
from backend.database import db

# Session management
import streamlit as st
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│     frontend/authenticated_app.py        │ Entry point
│     (authentication gateway)             │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│  backend/auth.py │  │  frontend/app.py │
│  - Login UI      │  │  - Legal AI app  │
│  - Signup UI     │  │  - Chat features │
└────────┬─────────┘  └──────────────────┘
         │
         ▼
┌──────────────────────────┐
│  backend/database.py     │
│  - Password hashing      │
│  - User registration     │
│  - Login verification    │
│  - Account lockout       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   legal_db/users.db      │
│   (SQLite database)      │
└──────────────────────────┘
```

---

## 🔐 Password Hashing Flow

```python
# Registration
plain_password = "MyPassword@123"
  │
  ▼ hash_password()
  │ - Generate random salt
  │ - Apply bcrypt algorithm 12 rounds
  │ - Return hash string
  ▼
password_hash = "$2b$12$kFXnPjrHEW3y..."
  │
  ▼
[Saved to database]

# Login
plain_password = "MyPassword@123"
  │
  ▼ verify_password()
  │ - Compare with stored hash
  │ - Use constant-time comparison
  │ - Return True/False
  ▼
[Allow login if True]
```

---

## 🔄 Login Flow

```python
# frontend/authenticated_app.py
if not AuthManager.is_authenticated():
    render_auth_page()
else:
    from app import main
    main()
```

```python
# backend/auth.py - render_auth_page()
if show_signup:
    render_signup_page()
else:
    render_login_page()
```

```python
# backend/auth.py - render_login_page()
if st.button("Login"):
    success, message = AuthManager.login(email, password)
    if success:
        st.rerun()  # Refresh to go to main app
```

```python
# backend/auth.py - AuthManager.login()
result = db.login_user(email, password)
if result['success']:
    st.session_state.authenticated = True
    st.session_state.user_email = email
    return True, result['message']
```

```python
# backend/database.py - login_user()
# 1. Find user by email
# 2. Check account lockout
# 3. Verify password with verify_password()
# 4. Track failed attempts (increment on failure)
# 5. Reset on success & update last_login
```

---

## 📝 Common Code Snippets

### Check if User is Authenticated
```python
from backend.auth import AuthManager

if AuthManager.is_authenticated():
    user = AuthManager.get_current_user()
    print(f"User: {user['name']} ({user['email']})")
else:
    print("Not authenticated")
```

### Get Current User Details
```python
from backend.auth import AuthManager

user = AuthManager.get_current_user()
# Returns: {"id": 1, "email": "user@example.com", "name": "John Doe"}
```

### Register New User
```python
from backend.database import db

result = db.register_user(
    email="john@example.com",
    full_name="John Doe",
    password="Strong@Pass123"
)
if result['success']:
    print("User registered successfully")
else:
    print(f"Error: {result['message']}")
```

### Verify User Login
```python
from backend.database import db

result = db.login_user(
    email="john@example.com",
    password="Strong@Pass123"
)
if result['success']:
    print(f"User {result['user_id']} logged in")
else:
    print(f"Login failed: {result['message']}")
```

### Change User Password
```python
from backend.database import db

result = db.change_password(
    email="john@example.com",
    old_password="Strong@Pass123",
    new_password="NewPass@456"
)
```

---

## 🗄️ Database Queries Reference

### View All Users
```bash
sqlite3 legal_db/users.db
sqlite> SELECT id, email, full_name, created_at FROM users;
```

### Check User Login History
```bash
sqlite> SELECT email, last_login FROM users;
```

### Check Failed Attempts
```bash
sqlite> SELECT email, failed_attempts, locked_until FROM users;
```

### Reset User Account
```bash
sqlite> UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE email = 'user@example.com';
```

### Delete User
```bash
sqlite> DELETE FROM users WHERE email = 'user@example.com';
```

### Backup Database
```bash
cp legal_db/users.db legal_db/users.db.backup
```

---

## 🧪 Testing Functions

### Test Registration
```python
from backend.database import db

# Valid registration
result = db.register_user("test@example.com", "Test User", "Valid@Pass123")
print(result)  # {"success": True, "message": "..."}

# Test duplicate email
result = db.register_user("test@example.com", "Test User 2", "Valid@Pass456")
print(result)  # {"success": False, "message": "Email already registered"}
```

### Test Login
```python
from backend.database import db

# Test successful login
result = db.login_user("test@example.com", "Valid@Pass123")
print(result)  # {"success": True, "user_id": 1, ...}

# Test wrong password
result = db.login_user("test@example.com", "Wrong@Pass999")
print(result)  # {"success": False, "message": "Invalid..."}
```

### Test Password Strength
```python
from backend.database import db

# This is internal but you can test via signup
# password requirements enforced in db._check_password_strength()
```

---

## 🚀 Development Workflow

### 1. Start Development
```bash
cd project-root
python run.py
```

### 2. Edit Auth Code
Edit in these files:
- `backend/auth.py` - Change auth flow/UI
- `backend/database.py` - Change security logic
- `frontend/authenticated_app.py` - Change main gate

### 3. Test Changes
- Streamlit auto-reloads on save
- Test signup/login
- Check `legal_db/users.db` with sqlite3

### 4. Debug
```bash
# Enable verbose logging
streamlit run frontend/authenticated_app.py --logger.level=debug
```

### 5. Reset for Clean Test
```bash
# Delete database to start fresh
rm legal_db/users.db
# Restart app - new db will be created
```

---

## 🔍 Session State Variables

```python
st.session_state.authenticated    # bool - Is user logged in?
st.session_state.user_id          # int - User's database ID
st.session_state.user_email       # str - User's email
st.session_state.user_name        # str - User's full name
st.session_state.show_signup      # bool - Show signup page?
```

---

## 🐛 Debugging Tips

### Check Authentication Status
```python
print(st.session_state.authenticated)
print(st.session_state.user_email)
```

### Check Database
```bash
sqlite3 legal_db/users.db ".tables"
sqlite3 legal_db/users.db "SELECT COUNT(*) FROM users;"
```

### View Error Logs
```bash
# Streamlit writes to console
# Check terminal for detailed error messages
```

### Reset Session (in app)
```python
# Clear all session state
for key in st.session_state.keys():
    del st.session_state[key]
```

---

## 📦 Dependencies

**Required for Auth:**
- `bcrypt` - Password hashing
- `streamlit` - Web framework
- `sqlite3` - Database (built-in)

**Optional (in requirements.txt):**
- `chromadb` - Vector store
- `langchain` - LLM workflows
- `openai` - LLM API

---

## 🔐 Security Checklist for Developers

When adding features, ensure:
- [ ] All passwords are hashed (not plain text)
- [ ] Parameterized SQL queries (no string concat)
- [ ] Input validation before DB insert
- [ ] No sensitive data in logs
- [ ] No secrets in code (use environment vars)
- [ ] SQL injection prevention
- [ ] XSS prevention (Streamlit handles this)
- [ ] CSRF tokens (if needed)
- [ ] Rate limiting (if needed)

---

## 🚢 Deployment Checklist

Before going to production:
- [ ] Change SQLite to PostgreSQL/MySQL
- [ ] Setup HTTPS/SSL
- [ ] Configure environment variables
- [ ] Setup database backups
- [ ] Enable audit logging
- [ ] Add rate limiting
- [ ] Setup error monitoring
- [ ] Load test the system
- [ ] Security audit
- [ ] Add 2FA support
- [ ] Setup email notifications

---

## 📚 File Purpose Reference

| File | Purpose | Key Classes |
|------|---------|------------|
| `backend/database.py` | User DB & passwords | `UserDatabase` |
| `backend/auth.py` | Auth & UI | `AuthManager` |
| `frontend/authenticated_app.py` | Auth gateway | None (main script) |
| `frontend/app.py` | Legal AI app | `main()` function |
| `legal_db/users.db` | User data | SQLite tables |

---

## 🎓 Learning Path

1. **Understand the Architecture**
   - Read `IMPLEMENTATION_SUMMARY.md`
   - Study the flow diagram above

2. **Learn the Database**
   - Read `backend/database.py` comments
   - Explore schema in `AUTHENTICATION.md`

3. **Study Authentication**
   - Read `backend/auth.py` comments
   - Understand `AuthManager` class

4. **Test Everything**
   - Follow `TESTING.md` test cases
   - Verify all features work

5. **Extend the System**
   - Add password reset
   - Add email verification
   - Add 2FA

---

## 🆘 Getting Help

- Check `SETUP.md` for setup issues
- Check `TESTING.md` for test cases
- Check `AUTHENTICATION.md` for API details
- Check `IMPLEMENTATION_SUMMARY.md` for overview
- Check comments in source files

---

**Keep your code secure! 🔐**

Last Updated: February 7, 2026
