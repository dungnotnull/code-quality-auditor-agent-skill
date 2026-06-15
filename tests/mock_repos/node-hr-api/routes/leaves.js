// routes/leaves.js

const { Router } = require('express');
const db = require('../db');

const router = Router();

router.get('/', async (req, res) => {
  try {
    const leaves = await db.query('SELECT * FROM leaves ORDER BY created_at DESC');
    res.json(leaves.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/', async (req, res) => {
  const { employee_id, start_date, end_date, reason } = req.body;
  // FLAW: No date validation (end before start, weekends, holidays, etc.)
  // FLAW: No overlapping leave check
  // FLAW: No balance check (remaining leave days)
  try {
    const result = await db.query(
      'INSERT INTO leaves (employee_id, start_date, end_date, reason, status) VALUES (, , , , ) RETURNING *',
      [employee_id, start_date, end_date, reason, 'pending']
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.put('/:id/approve', async (req, res) => {
  // FLAW: No authorization check - any authenticated user can approve
  try {
    const result = await db.query(
      'UPDATE leaves SET status =  WHERE id =  RETURNING *',
      ['approved', req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Leave request not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = { leavesRouter: router };
