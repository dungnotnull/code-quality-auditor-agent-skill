// index.js - Node.js HR API Entry Point (Small codebase ~200 LOC, INTENTIONALLY MINOR FLAWS)

const express = require('express');
const { employeesRouter, leavesRouter } = require('./routes');
const { authMiddleware } = require('./middleware/auth');

const app = express();
app.use(express.json());

// Routes
app.use('/api/employees', authMiddleware, employeesRouter);
app.use('/api/leaves', authMiddleware, leavesRouter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(HR API running on port );
});

module.exports = app;
