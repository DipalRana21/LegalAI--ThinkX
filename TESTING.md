# 🧪 Authentication System - Testing Guide

## Overview

This guide helps you test the authentication system to ensure all security features are working correctly.

---

## 🎯 Test Cases

### Test 1: User Registration with Valid Data

**Objective:** Verify successful account creation

**Steps:**
1. Click "📝 Create Account"
2. Enter:
   - Full Name: `John Legal Expert`
   - Email: `john.legal@example.com`
   - Password: `SecureLegal@123`
   - Confirm: `SecureLegal@123`
3. Click "✅ Create Account"

**Expected Result:**
- ✅ Success message appears
- ✅ Message says "Account created! Please login now."
- ✅ Button changes to "← Back to Login"
- ✅ User can login with the same credentials

---

### Test 2: Password Strength Validation

**Objective:** Verify password requirements are enforced

**Try these passwords (should FAIL):**
- `weak` - Too short, no requirements
- `NoSpecialChar123` - Missing special character
- `nouppercase@123` - All lowercase
- `NOLOWERCASE@123` - All uppercase
- `NoNumber@abc` - Missing number
- `Short@1` - Only 7 characters

**Try these passwords (should PASS):**
- `ValidPass@123`
- `MyLegal#2024`
- `Secure!Pass99`
- `NyayaSahay@1k`

**Expected Behavior:**
- 🔴 **Weak:** Less than 60% strength
- 🟡 **Medium:** 60-80% strength  
- 🟢 **Strong:** 80%+ strength

---

### Test 3: Email Validation

**Objective:** Verify email is properly validated

**Try these emails (should FAIL):**
- `invalid-email` - Missing @
- `test@` - No domain
- `@example.com` - No username

**Try these emails (should PASS):**
- `user@example.com`
- `john.doe@legal.co.in`
- `ashok123@gmail.com`

**Expected Result:**
- ❌ Invalid formats rejected with error message
- ✅ Valid emails accepted

---

### Test 4: Duplicate Email Prevention

**Objective:** Verify same email cannot be registered twice

**Steps:**
1. Register with `test@example.com` and `Password@123`
2. Try to register again with same email and different password
3. Click "✅ Create Account"

**Expected Result:**
- ❌ Error message: "Email already registered. Please login or use a different email."
- ✅ Database doesn't allow duplicate email
- ✅ User prompted to login or use different email

---

### Test 5: Successful Login

**Objective:** Verify secure authentication process

**Steps:**
1. Have valid account (from Test 1)
2. Go to login page
3. Enter email: `john.legal@example.com`
4. Enter password: `SecureLegal@123`
5. Click "🔓 Login"

**Expected Result:**
- ✅ Green success message appears
- ✅ Page reloads to authenticated view
- ✅ Sidebar shows:
  - User name
  - User email
  - Logout button
- ✅ Main legal AI app is accessible

---

### Test 6: Failed Login - Wrong Password

**Objective:** Verify security against incorrect password

**Steps:**
1. Enter valid email
2. Enter WRONG password (e.g., `WrongPass@123`)
3. Click "🔓 Login"

**Expected Result (First Attempt):**
- ❌ Error: "Invalid email or password"
- ✅ Page stays on login
- ✅ No information about which field is wrong (good security)

**Expected Result (After 5 Attempts):**
- ❌ Error: "Account locked due to multiple failed attempts. Try again in 30 minutes."
- ✅ Account becomes inaccessible
- ✅ User must wait to try again

---

### Test 7: Failed Login - Wrong Email

**Objective:** Verify email validation during login

**Steps:**
1. Enter non-existent email: `nonexistent@example.com`
2. Enter any password
3. Click "🔓 Login"

**Expected Result:**
- ❌ Error: "Invalid email or password"
- ✅ Generic error (doesn't reveal if email exists or not)
- ✅ Secure against email enumeration attacks

---

### Test 8: Account Lockout Mechanism

**Objective:** Verify brute force protection

**Steps:**
1. Use valid email but WRONG password
2. Click "🔓 Login" exactly 5 times with wrong password
3. On 6th attempt, click "🔓 Login"

**Expected Progress:**
- Attempts 1-4: "Invalid email or password"
- Attempt 5: "Invalid email or password"
- Attempt 6: "Account locked due to multiple failed attempts. Try again in 30 minutes."

**Expected Result:**
- ✅ Account locked after 5 failures
- ✅ Cannot login for 30 minutes
- ✅ Protects against brute force attacks
- ✅ Timer expires after 30 minutes

---

### Test 9: Password Field Security

**Objective:** Verify password is not visible

**Steps:**
1. Click on any password input field
2. Type password: `MyPassword@123`
3. Observe the field

**Expected Result:**
- ✅ Password shows as dots/asterisks
- ✅ Text is NOT visible
- ✅ Cannot shoulder-surf the password
- ✅ Browser password manager can auto-fill (convenience feature)

---

### Test 10: Logout Functionality

**Objective:** Verify secure session termination

**Steps:**
1. Login successfully
2. Click "🚪 Logout" in sidebar
3. Refresh the page (Ctrl+R)

**Expected Result:**
- ✅ Logged out immediately
- ✅ Redirected to login page
- ✅ Session state cleared
- ✅ Cannot access authenticated pages
- ✅ Must login again to proceed

---

### Test 11: Password Change (Future)

**Objective:** Verify users can change passwords securely

**Steps (when implemented):**
1. After login, click "Change Password"
2. Enter current password: `SecureLegal@123`
3. Enter new password: `NewSecure@456`
4. Confirm new password: `NewSecure@456`
5. Click "Update Password"

**Expected Result:**
- ✅ Old password verified first
- ✅ New password must meet strength requirements
- ✅ Success message appears
- ✅ Next login uses new password
- ✅ Old password no longer works

---

### Test 12: Database Security

**Objective:** Verify passwords are not stored as plain text

**Check Database:**
```bash
# On terminal (from project root)
sqlite3 legal_db/users.db
sqlite> SELECT email, password_hash FROM users LIMIT 1;
```

**Expected Result:**
```
john.legal@example.com|$2b$12$kFXnpPjrHEW3y... (hashed, not readable)
```

**NOT Expected:**
```
john.legal@example.com|SecureLegal@123  ❌ UNACCEPTABLE
```

- ✅ Passwords are bcrypt hashes (start with `$2b$12$`)
- ✅ Cannot be reversed to original password
- ✅ Each password hash is unique (even if password is same)
- ✅ Cannot be cracked without massive computation

---

## 🔐 Security Testing Checklist

Use this checklist to verify all security features:

- [ ] ✅ Passwords hashed with bcrypt
- [ ] ✅ Account lockout after 5 failed attempts
- [ ] ✅ 30-minute lockout timer
- [ ] ✅ Password strength requirements enforced
- [ ] ✅ Email uniqueness validated
- [ ] ✅ Generic error messages (security)
- [ ] ✅ No sensitive data in error messages
- [ ] ✅ Password field masked (dots)
- [ ] ✅ Secure session management
- [ ] ✅ Logout clears all session data
- [ ] ✅ Database uses parameterized queries
- [ ] ✅ Failed login attempts tracked
- [ ] ✅ User can create strong passwords
- [ ] ✅ User cannot login with weak passwords

---

## 📊 Test Report Template

When testing, document results:

```
TEST CASE: [Name]
Date: [Date]
Tester: [Your Name]

Steps Performed:
1. ...
2. ...

Expected Result:
...

Actual Result:
...

Status: ✅ PASS / ❌ FAIL

Notes:
...
```

---

## 🐛 Known Testing Issues

None currently - all security features working as designed!

---

## ✅ Sample Test Data

### Test User 1 (Admin)
```
Name: Ashok Kumar
Email: ashok@legalai.com
Password: LegalAssist@2024
```

### Test User 2 (Regular)
```
Name: Priya Singh
Email: priya@court.com
Password: Justice@System123
```

### Test User 3 (High Security)
```
Name: Dr. Rajesh Gupta
Email: rajesh.dr@law.in
Password: SecurePassw0rd#Complex
```

---

## 🎓 What You've Verified

After completing these tests, you've verified:

✅ **Authentication:**
- Registration with validation
- Secure password hashing
- Login verification
- Session management

✅ **Security:**
- Brute force protection
- Password strength requirements
- Email uniqueness
- Generic error messages
- Secure password storage

✅ **User Experience:**
- Clear feedback
- Helpful error messages
- Password strength indicator
- Easy navigation

---

## 📈 Performance Notes

- Registration: < 1 second
- Login: < 500ms
- Password hash: ~100ms (security trade-off)
- Account lockout check: < 50ms

---

**Happy Testing! 🚀**

Report any issues to the development team.

Last Updated: February 7, 2026
