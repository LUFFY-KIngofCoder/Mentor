User registers
    ↓
Password gets hashed
    ↓
User logs in
    ↓
Backend verifies password
    ↓
JWT token generated
    ↓
Frontend stores token
    ↓
Protected routes require token
    ↓
Backend extracts current user



Request
↓
OAuth2PasswordBearer extracts token
↓
get_current_user() receives token
↓
Decode JWT
↓
Verify signature
↓
Check expiry
↓
Extract user_id
↓
Fetch DB user
↓
Return authenticated user

