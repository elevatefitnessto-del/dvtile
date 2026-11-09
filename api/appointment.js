// Vercel serverless function: POST /api/appointment
// Emails the request to the showroom through Resend when RESEND_API_KEY is set.
// Env vars: RESEND_API_KEY, APPOINTMENTS_TO (showroom inbox), APPOINTMENTS_FROM (verified sender, e.g. "DVTile <website@dvtile.ca>").
const clean = (v, max = 2000) => String(v ?? '').replace(/[\r\0]/g, '').trim().slice(0, max);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed.' });

  let data = req.body;
  if (typeof data === 'string') { try { data = JSON.parse(data); } catch { data = null; } }
  if (!data || typeof data !== 'object') return res.status(400).json({ error: 'Invalid request.' });

  if (clean(data.company)) return res.status(200).json({ ok: true }); // honeypot: accept silently

  const name = clean(data.name, 120);
  const email = clean(data.email, 200);
  if (!name || !EMAIL.test(email)) return res.status(422).json({ error: 'Name and a valid email are required.' });

  const fields = {
    Name: name,
    Email: email,
    Phone: clean(data.phone, 40),
    Project: clean(data.project, 80),
    'Preferred date': clean(data.date, 20),
    Message: clean(data.message),
  };

  const { RESEND_API_KEY, APPOINTMENTS_TO, APPOINTMENTS_FROM } = process.env;
  if (!RESEND_API_KEY || !APPOINTMENTS_TO || !APPOINTMENTS_FROM) {
    console.error('Appointment email not configured');
    return res.status(503).json({ error: 'Email delivery is not configured.' });
  }

  const text = Object.entries(fields).map(([k, v]) => `${k}: ${v || '—'}`).join('\n');
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: APPOINTMENTS_FROM,
        to: [APPOINTMENTS_TO],
        reply_to: email,
        subject: `Appointment request: ${name} (${fields.Project || 'no project'})`.replace(/[\r\n]/g, ' '),
        text,
      }),
    });
    if (!r.ok) throw new Error(`Resend ${r.status}`);
  } catch (err) {
    console.error('send failed', err);
    return res.status(502).json({ error: 'Could not send.' });
  }
  return res.status(200).json({ ok: true });
};
