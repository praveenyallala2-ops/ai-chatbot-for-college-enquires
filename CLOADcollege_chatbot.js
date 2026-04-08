/* ──────────────────────────────────────────────────────────────────────────
   CLOADcollege_chatbot.js
   Frontend logic for SREC Nandyal AI Chatbot.
   Sends user messages to the Flask backend (/chat) and displays responses.
   All UI (HTML + CSS) is unchanged — only the response source has changed
   from a local KB object to a real AI backend (TF-IDF + Naive Bayes).
   ────────────────────────────────────────────────────────────────────────── */

const API_URL = 'http://127.0.0.1:5000/chat';   // Flask backend endpoint

let chatOpen = false;

// ── Toggle chat window open / closed ─────────────────────────────────────────
function toggleChat() {
  chatOpen = !chatOpen;
  const win = document.getElementById('chat-window');
  const btn = document.getElementById('chat-toggle');
  win.classList.toggle('open', chatOpen);
  btn.innerHTML = chatOpen
    ? `<span style="font-size:22px">✕</span>`
    : `🎓<div class="badge"></div>`;

  if (chatOpen && document.getElementById('chat-messages').children.length === 0) {
    setTimeout(() =>
      addBotMsg(
        `👋 Hi! I'm **SREC Assistant** — powered by AI.\n\n` +
        `Ask me anything about admissions, fees, courses, placements, or campus life. ` +
        `I'm available 24/7! 🎓\n\nTap any quick question below or type your own.`
      ), 400
    );
  }
}

function openChat() {
  if (!chatOpen) toggleChat();
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function fmt(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
}

// ── Render a bot message (with typing animation) ──────────────────────────────
function addBotMsg(text) {
  const msgs = document.getElementById('chat-messages');

  // Show typing indicator
  const typing = document.createElement('div');
  typing.className = 'msg bot';
  typing.id = 'typing-ind';
  typing.innerHTML = `<div class="bot-avatar">🤖</div>
    <div class="typing-indicator"><span></span><span></span><span></span></div>`;
  msgs.appendChild(typing);
  msgs.scrollTop = msgs.scrollHeight;

  // Replace indicator with actual message after a natural delay
  const delay = 700 + Math.min(text.length * 1.2, 1200);
  setTimeout(() => {
    const t = document.getElementById('typing-ind');
    if (t) t.remove();
    const div = document.createElement('div');
    div.className = 'msg bot';
    div.innerHTML = `<div class="bot-avatar">🤖</div>
      <div class="bubble">${fmt(text)}<div class="meta">${getTime()}</div></div>`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }, delay);
}

// ── Render a user message ─────────────────────────────────────────────────────
function addUserMsg(text) {
  const msgs = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = 'msg user';
  div.innerHTML = `<div class="bubble">${text}<div class="meta">${getTime()}</div></div>`;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

// ── Send message to Flask AI backend ─────────────────────────────────────────
async function sendMessage() {
  const input = document.getElementById('chat-input');
  const text  = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = '42px';
  addUserMsg(text);

  const btn = document.getElementById('send-btn');
  btn.disabled = true;

  // Show placeholder typing indicator while we await the API
  const msgs = document.getElementById('chat-messages');
  const typing = document.createElement('div');
  typing.className = 'msg bot';
  typing.id = 'typing-ind';
  typing.innerHTML = `<div class="bot-avatar">🤖</div>
    <div class="typing-indicator"><span></span><span></span><span></span></div>`;
  msgs.appendChild(typing);
  msgs.scrollTop = msgs.scrollHeight;

  try {
    const res  = await fetch(API_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ message: text })
    });

    const data = await res.json();

    // Remove the indicator that was added above
    const t = document.getElementById('typing-ind');
    if (t) t.remove();

    // Display the AI response
    const reply = data.response ||
      '⚠️ Sorry, I could not get a response. Please try again.';
    const div = document.createElement('div');
    div.className = 'msg bot';
    div.innerHTML = `<div class="bot-avatar">🤖</div>
      <div class="bubble">${fmt(reply)}<div class="meta">${getTime()}</div></div>`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;

  } catch (err) {
    // Remove indicator on error
    const t = document.getElementById('typing-ind');
    if (t) t.remove();

    addBotMsg(
      `⚠️ **Connection Error**\n\nI'm having trouble reaching the server.\n` +
      `Please make sure the backend is running:\n\`python app.py\`\n\n` +
      `Or call us directly: **+91-8514-233933** 📞`
    );
    console.error('Chat API error:', err);
  } finally {
    btn.disabled = false;
  }
}

// ── Quick chip buttons ────────────────────────────────────────────────────────
function sendChip(el) {
  const text = el.textContent.replace(/^\S+\s/, '').trim();
  document.getElementById('chat-input').value = text;
  sendMessage();
}

// ── Enter key sends message (Shift+Enter = new line) ─────────────────────────
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

// ── Auto-resize textarea ──────────────────────────────────────────────────────
document.getElementById('chat-input').addEventListener('input', function () {
  this.style.height = '42px';
  this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});
