'use strict';

/*
 * Hammer Head Group — 30-day social media approval server.
 *
 * Serves the public (unlisted) review page and stores every approval,
 * edit note, and overall comment centrally. When the client submits their
 * review, the agency is emailed a full summary. A protected /admin
 * dashboard shows the live state and every submission.
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const app = express();
app.use(express.json({ limit: '256kb' }));

const PORT = process.env.PORT || 3000;
const ADMIN_KEY = process.env.ADMIN_KEY || 'change-me';
const NOTIFY_EMAIL = process.env.NOTIFY_EMAIL || 'youraistarr@gmail.com';
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const DATA_FILE = path.join(DATA_DIR, 'review.json');

/* ---------- tiny JSON store ---------- */
function emptyData() {
  return { items: {}, reviewer: { name: '', overall: '' }, submissions: [], updatedAt: null };
}
let data = emptyData();
try {
  if (fs.existsSync(DATA_FILE)) data = Object.assign(emptyData(), JSON.parse(fs.readFileSync(DATA_FILE, 'utf8')));
} catch (e) {
  console.error('Could not read data file, starting fresh:', e.message);
}
function persist() {
  data.updatedAt = new Date().toISOString();
  try {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  } catch (e) {
    console.error('Could not persist data:', e.message);
  }
}

/* ---------- email ---------- */
let transporter = null;
if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
  transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT || 587),
    secure: String(process.env.SMTP_SECURE || 'false') === 'true',
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
  });
  console.log('Email notifications enabled ->', NOTIFY_EMAIL);
} else {
  console.log('SMTP not configured; submissions will be stored and shown on /admin but not emailed.');
}

async function sendNotification(subject, text) {
  if (!transporter) return { emailed: false, reason: 'smtp-not-configured' };
  try {
    await transporter.sendMail({
      from: process.env.SMTP_FROM || process.env.SMTP_USER,
      to: NOTIFY_EMAIL,
      subject,
      text
    });
    return { emailed: true };
  } catch (e) {
    console.error('Email send failed:', e.message);
    return { emailed: false, reason: e.message };
  }
}

/* ---------- API ---------- */
// Current review state for the public page.
app.get('/api/state', (req, res) => {
  res.json({ items: data.items, reviewer: data.reviewer });
});

// Save one item's decision + note.
app.put('/api/item/:id', (req, res) => {
  const id = String(req.params.id).slice(0, 64);
  const { status, note } = req.body || {};
  const cur = data.items[id] || {};
  if (status === 'ok' || status === 'no') cur.status = status;
  else delete cur.status;
  cur.note = typeof note === 'string' ? note.slice(0, 2000) : (cur.note || '');
  if (!cur.status && !cur.note) delete data.items[id];
  else data.items[id] = cur;
  persist();
  res.json({ ok: true });
});

// Save reviewer name + overall comment as they type.
app.post('/api/reviewer', (req, res) => {
  const { name, overall } = req.body || {};
  data.reviewer = {
    name: typeof name === 'string' ? name.slice(0, 200) : '',
    overall: typeof overall === 'string' ? overall.slice(0, 4000) : ''
  };
  persist();
  res.json({ ok: true });
});

function buildReport(labels) {
  const lines = [];
  let ok = 0, no = 0, pd = 0;
  (labels || []).forEach(({ id, label }) => {
    const s = data.items[id] || {};
    if (s.status === 'ok') { ok++; lines.push('[APPROVED]  ' + label); }
    else if (s.status === 'no') { no++; lines.push('[EDITS]     ' + label + (s.note && s.note.trim() ? '\n            -> ' + s.note.trim() : '\n            -> (no note added)')); }
    else { pd++; lines.push('[PENDING]   ' + label); }
  });
  const head = [
    'HAMMER HEAD GROUP — 30-DAY SOCIAL MEDIA REVIEW',
    'Reviewer: ' + (data.reviewer.name || '(not provided)'),
    'Submitted: ' + new Date().toLocaleString(),
    '',
    'SUMMARY: ' + ok + ' approved  |  ' + no + ' need edits  |  ' + pd + ' pending',
    '------------------------------------------------------------'
  ];
  if (data.reviewer.overall && data.reviewer.overall.trim()) {
    head.push('OVERALL COMMENTS:', data.reviewer.overall.trim(), '------------------------------------------------------------');
  }
  head.push('');
  return { text: head.concat(lines).join('\n'), ok, no, pd };
}

// Final submission: store + email the agency.
app.post('/api/submit', async (req, res) => {
  const { name, overall, labels } = req.body || {};
  data.reviewer = {
    name: typeof name === 'string' ? name.slice(0, 200) : data.reviewer.name,
    overall: typeof overall === 'string' ? overall.slice(0, 4000) : data.reviewer.overall
  };
  const report = buildReport(labels);
  const submittedAt = new Date().toISOString();
  data.submissions.push({
    at: submittedAt,
    name: data.reviewer.name,
    overall: data.reviewer.overall,
    counts: { approved: report.ok, edits: report.no, pending: report.pd },
    items: JSON.parse(JSON.stringify(data.items))
  });
  persist();
  const mail = await sendNotification(
    'HHG Social Review submitted' + (data.reviewer.name ? ' by ' + data.reviewer.name : ''),
    report.text
  );
  res.json({ ok: true, submittedAt, emailed: mail.emailed, report: report.text });
});

// Protected dashboard data.
app.get('/api/admin', (req, res) => {
  if ((req.query.key || '') !== ADMIN_KEY) return res.status(401).json({ error: 'unauthorized' });
  res.json(data);
});

app.get('/healthz', (req, res) => res.send('ok'));

/* ---------- static ---------- */
app.use(express.static(path.join(__dirname, 'public')));
app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'public', 'admin.html')));

app.listen(PORT, () => console.log('HHG approval site running on port ' + PORT));
