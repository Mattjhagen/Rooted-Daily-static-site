/**
 * Rooted Daily — AI Scripture Guide Proxy Worker
 * Deploy at: https://dash.cloudflare.com → Workers & Pages → Create Worker
 *
 * Add secret: Settings → Variables and Secrets → Add (Encrypted)
 *   Name:  GROQ_KEY
 *   Value: (paste your key from console.groq.com — never put it in code)
 */

const ALLOWED_ORIGINS = [
  'https://app.vibecodes.space',
  'https://rootedapp.space',
  'http://localhost:5500',   // local dev
  'http://127.0.0.1:5500',
];

export default {
  async fetch(request, env) {

    const origin = request.headers.get('Origin') || '';
    // Native apps (Android/iOS) don't send Origin — allow with wildcard
    const allowedOrigin = !origin ? '*' : (ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0]);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders(allowedOrigin),
      });
    }

    // Only allow POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const body = await request.json();
      const { messages } = body;

      if (!messages || !Array.isArray(messages)) {
        return new Response(JSON.stringify({ error: 'Invalid request: messages required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...corsHeaders(allowedOrigin) }
        });
      }

      // Forward to Groq — key is env variable, never in client code
      const groqRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${env.GROQ_KEY}`,
        },
        body: JSON.stringify({
          model: 'llama-3.3-70b-versatile',
          messages,
          temperature: 0.7,
          max_tokens: 600,
        }),
      });

      const data = await groqRes.json();

      return new Response(JSON.stringify(data), {
        status: groqRes.status,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders(allowedOrigin),
        },
      });

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders(allowedOrigin) },
      });
    }
  },
};

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}
