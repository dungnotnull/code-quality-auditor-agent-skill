// middleware/auth.js - Simple token-based auth middleware

const JWT_SECRET = 'INTENTIONALLY_FAKE_JWT_SECRET_FOR_AUDIT_TEST';  // FLAW: Hardcoded JWT secret

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  // FLAW: Not actually verifying the JWT - just checking it exists
  // FLAW: Should use jsonwebtoken.verify(token, JWT_SECRET)
  // This is a Critical security flaw - any string is accepted as a valid token
  req.userId = token;  // FLAW: Using raw token as user ID
  next();
}

module.exports = { authMiddleware, JWT_SECRET };
