// routes/employees.js

const { Router } = require('express');
const db = require('../db');

const router = Router();

router.get('/', async (req, res) => {
  try {
    const employees = await db.query('SELECT id, name, email, department FROM employees');
    res.json(employees.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });  // FLAW: Leaks DB error details to client
  }
});

router.get('/:id', async (req, res) => {
  const { id } = req.params;
  // FLAW: No input validation on id parameter
  try {
    const result = await db.query('SELECT * FROM employees WHERE id = ', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Employee not found' });
    }
    res.json(result.rows[0]);  // FLAW: Returns all columns including potentially sensitive ones
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/', async (req, res) => {
  const { name, email, department } = req.body;
  // FLAW: No input validation (missing fields, email format, etc.)
  // FLAW: No duplicate email check
  try {
    const result = await db.query(
      'INSERT INTO employees (name, email, department) VALUES (, , ) RETURNING *',
      [name, email, department]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = { employeesRouter: router };
