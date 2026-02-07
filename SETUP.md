# 🚀 Quick Setup Guide - NyayaSahayak with Authentication

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

---

## Step 1: Install Dependencies

From the project root directory, run:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- streamlit (frontend framework)
- bcrypt (password hashing)
- chromadb (vector database)
- langchain (LLM workflows)
- And all other dependencies

**Expected output:** No errors, all packages installed successfully

---

## Step 2: Start the Application

From the project root, run:

```bash
python run.py
```

Or alternatively:

```bash
streamlit run frontend/authenticated_app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Step 3: Access the Application

1. Open your web browser
2. Go to: **http://localhost:8501**
3. You should see the **Login/Signup Page**

---

## Step 4: Create Your First Account

### Option A: Sign Up (New User)

1. Click **"📝 Create Account"** button
2. Fill in the form:
   - **Full Name:** Your name (e.g., "John Doe")
   - **Email:** Your email (e.g., "john@example.com")
   - **Password:** Create a strong password
     - Must be 8+ characters
     - Include uppercase (A-Z)
     - Include lowercase (a-z)
     - Include number (0-9)
     - Include special character (!@#$%^&*)
   - **Confirm Password:** Re-enter your password

3. Watch the password strength indicator:
   - 🔴 Weak (less than 60%)
   - 🟡 Medium (60-80%)
   - 🟢 Strong (80%+)

4. Click **"✅ Create Account"**
5. See success message
6. Click **"← Back to Login"**
7. Now login with your credentials

### Option B: Login (Existing User)

1. Enter your registered email
2. Enter your password
3. Click **"🔓 Login"**
4. You're now authenticated! ✅

---

## Step 5: Use the Application

Once logged in:

1. **Sidebar Info** - Shows your name and email
2. **Logout Button** - Securely log out anytime
3. **Main App** - Full access to Legal AI Assistant
   - Ask legal questions
   - Get Indian law references
   - Learn about your rights
   - Voice input (Hindi/English)
   - Download chat history

---

## 📝 Example Test Credentials

After signup, you can use these as templates:

**Test Account 1:**
```
Email: legal@test.com
Password: LegalTest@123
Full Name: Legal User
```

**Test Account 2:**
```
Email: justice@test.com
Password: Justice@456
Full Name: Justice Seeker
```

---

## 🔑 Important: Password Security

### ✅ GOOD Passwords (Will be accepted)
- `MyLegal@123`
- `Ashok#2024`
- `Secure!Pass99`
- `NyayaSahay@1k`

### ❌ BAD Passwords (Will be rejected)
- `password` (no uppercase, number, special char)
- `Pass123` (no special character)
- `ALLUPPERCASE@1` (no lowercase)
- `short` (too short, no requirements met)
- `12345678` (only numbers)

---

## 🛡️ Security Features You Have

✅ **Passwords are hashed** - Never stored as plain text  
✅ **Account lockout** - After 5 failed attempts (30 min timeout)  
✅ **Strong encryption** - bcrypt with 12-round salt  
✅ **Session protection** - Secure session management  
✅ **Input validation** - All data validated before storage  
✅ **Unique emails** - Can't register twice with same email  

---

## 📂 Database Location

The user database is stored at:
```
legal_db/users.db
```

This is created automatically on first run. It contains:
- User emails (unique)
- User names
- Password hashes (cannot be reversed)
- Login timestamps
- Account lock status
- Failed attempt counters

**Note:** Don't delete or modify this file manually!

---

## 🚨 Troubleshooting

### Issue: "Port 8501 already in use"
**Solution:** Kill the existing Streamlit process or use different port:
```bash
streamlit run frontend/authenticated_app.py --server.port 8502
```

### Issue: "Module not found: backend.auth"
**Solution:** Ensure you're running from project root:
```bash
# Wrong (from frontend folder):
cd frontend && python authenticated_app.py

# Correct (from project root):
python run.py
```

### Issue: "Email already registered"
**Solution:** Use a different email address or check if you already have an account

### Issue: "Password doesn't meet requirements"
**Solution:** Ensure your password has:
- At least 8 characters
- Uppercase letter
- Lowercase letter
- One number
- One special character

### Issue: "Account is locked"
**Solution:** Wait 30 minutes or restart the app (resets temporary lock)

### Issue: Database permission error
**Solution:** Ensure write permissions on `legal_db/` directory:
```bash
chmod -R 755 legal_db/  # On macOS/Linux
```

---

## 📱 Application Features

Once logged in, try these:

1. **Ask Legal Questions**
   - "What is IPC 420?"
   - "What are my rights during arrest?"
   - "Consumer protection act details"

2. **Use Voice Input** 🎤
   - Click microphone in sidebar
   - Speak in Hindi or English
   - Auto-transcription

3. **View Chat History**
   - All conversations stored in session
   - Download as text file

4. **Learn About Laws**
   - IPC sections
   - CrPC procedures
   - Constitutional rights
   - Consumer protection
   - Domestic violence laws

---

## 🔄 Development Commands

### Run with specific port:
```bash
streamlit run frontend/authenticated_app.py --server.port 8502
```

### Run in developer mode:
```bash
streamlit run frontend/authenticated_app.py --logger.level=debug
```

### Reset database (delete all users):
```bash
rm legal_db/users.db
```

### Check database contents (Linux/Mac):
```bash
sqlite3 legal_db/users.db
sqlite> SELECT email, full_name FROM users;
```

---

## 📧 Next Steps

1. ✅ Install dependencies
2. ✅ Start the app
3. ✅ Create your account
4. ✅ Login
5. ✅ Ask legal questions
6. ✅ Explore features
7. ✅ Logout securely

---

## 🎓 What's Different Now?

### Before Authentication:
- Anyone could access the app
- No user tracking
- No personalization
- Shared conversation history

### After Authentication:
- ✅ Secure login required
- ✅ Individual user accounts
- ✅ Per-user conversation history
- ✅ Account security features
- ✅ Password protection
- ✅ Brute force prevention
- ✅ Professional authentication UI

---

## 📚 For More Information

See the detailed documentation:
- [AUTHENTICATION.md](AUTHENTICATION.md) - Complete auth system documentation
- [README.md](README.md) - Main project documentation
- [requirements.txt](requirements.txt) - All dependencies listed

---

**Last Updated:** February 7, 2026  
**Status:** ✅ Ready for Development and Testing

Happy coding! 🚀⚖️
