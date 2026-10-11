// Vercel Serverless Function: recebe o formulário de orçamento e envia por e-mail (Resend).
// Variáveis de ambiente (Vercel > Settings > Environment Variables):
//   RESEND_API_KEY  chave da conta Resend (obrigatória)
//   LEAD_TO         destinatário (padrão: deck@newenglandcarpenters.com)
//   LEAD_FROM       remetente com domínio verificado no Resend, ex.: "New England Snow Removal <leads@snowremoval-ne.com>"

const MAX = { name: 120, email: 160, phone: 40, address: 200, type: 20, message: 3000 };

function clean(v, max) {
  return String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max);
}
function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  // honeypot: robôs preenchem este campo
  if (body.website) return res.status(200).json({ ok: true });

  const lead = {
    name: clean(body.name, MAX.name),
    email: clean(body.email, MAX.email),
    phone: clean(body.phone, MAX.phone),
    address: clean(body.address, MAX.address),
    type: clean(body.type, MAX.type),
    message: clean(body.message, MAX.message),
    page: clean(body.page, 200),
    utm: ['utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'fbclid']
      .map(k => body[k] ? k + '=' + clean(body[k], 100) : '').filter(Boolean).join(' · ')
  };
  if (!lead.name || !/^\S+@\S+\.\S+$/.test(lead.email) || lead.phone.replace(/\D/g, '').length < 7) {
    return res.status(400).json({ ok: false, error: 'invalid_input' });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, error: 'not_configured' });

  const to = process.env.LEAD_TO || 'deck@newenglandcarpenters.com';
  const from = process.env.LEAD_FROM || 'New England Snow Removal <onboarding@resend.dev>';
  const rows = [
    ['Name', lead.name], ['Email', lead.email], ['Phone', lead.phone],
    ['Property address', lead.address], ['Property type', lead.type], ['Message', lead.message],
    ['Page', lead.page], ['Tracking', lead.utm]
  ].filter(r => r[1]);
  const html = '<h2>New quote request</h2><table cellpadding="6">' +
    rows.map(r => '<tr><td><b>' + r[0] + '</b></td><td>' + esc(r[1]).replace(/\n/g, '<br>') + '</td></tr>').join('') + '</table>';

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: [to], reply_to: lead.email, subject: 'New quote request: ' + lead.name, html })
    });
    if (!r.ok) return res.status(502).json({ ok: false, error: 'send_failed' });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(502).json({ ok: false, error: 'send_failed' });
  }
};
