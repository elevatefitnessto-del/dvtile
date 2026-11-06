// Cloudflare Pages Function: POST /api/appointment
// Sends the appointment request to the showroom inbox through Cloudflare Email Routing.
// Setup (see README): enable Email Routing on dvtile.ca, verify the destination address,
// and add a `send_email` binding named APPOINTMENTS in wrangler.toml / Pages settings.
import { EmailMessage } from 'cloudflare:email';

const FROM = 'website@dvtile.ca';

const clean = (v, max = 2000) => String(v ?? '').replace(/[\r\0]/g, '').trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  let data;
  try { data = await request.json(); } catch { return json({ error: 'Invalid request.' }, 400); }

  if (clean(data.company)) return json({ ok: true }); // honeypot: silently accept bots

  const name = clean(data.name, 120);
  const email = clean(data.email, 200);
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: 'Name and a valid email are required.' }, 422);
  }
  const fields = {
    Name: name,
    Email: email,
    Phone: clean(data.phone, 40),
    Project: clean(data.project, 80),
    'Preferred date': clean(data.date, 20),
    Message: clean(data.message),
  };

  if (!env.APPOINTMENTS || !env.APPOINTMENTS_TO) {
    console.error('Appointment email not configured', fields);
    return json({ error: 'Email delivery is not configured.' }, 503);
  }

  const body = Object.entries(fields).map(([k, v]) => `${k}: ${v || '—'}`).join('\n');
  const subject = `Appointment request: ${name} (${fields.Project})`.replace(/[\n]/g, ' ');
  const raw = [
    `From: DVTile website <${FROM}>`,
    `To: ${env.APPOINTMENTS_TO}`,
    `Reply-To: ${name.replace(/[<>"\n]/g, '')} <${email}>`,
    `Subject: ${subject}`,
    `Message-ID: <${crypto.randomUUID()}@dvtile.ca>`,
    `Date: ${new Date().toUTCString()}`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    '',
    body,
  ].join('\r\n');

  try {
    await env.APPOINTMENTS.send(new EmailMessage(FROM, env.APPOINTMENTS_TO, raw));
  } catch (err) {
    console.error('send failed', err);
    return json({ error: 'Could not send.' }, 502);
  }
  return json({ ok: true });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json' } });
}
