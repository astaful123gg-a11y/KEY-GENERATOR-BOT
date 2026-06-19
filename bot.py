# ============================================================
# 🔥 ULTRA BOMBER KEY GENERATOR BOT 🔥
# ============================================================
# ✅ ONLY KEY GENERATOR — No Bombing
# ✅ REPLY KEYBOARD — Inline nahi
# ✅ BOLD + QUOTE STYLE Messages
# ✅ UNIQUE START MESSAGE
# ============================================================

from flask import Flask, request, jsonify
import requests
import json
import secrets
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# ====== CONFIG ======
BOT_TOKEN = "8426512063:AAEenIycdjgaXZLi-oz9HW_hbEY2f8UcSaI"  # <-- APNA TOKEN
OWNER_ID = "8600328303"  # <-- APNA TELEGRAM ID
API_URL = "https://ultra-bomber.onrender.com"  # Ultra Bomber API
ADMIN_KEY = "admin123"  # Master key for keygen

# ====== KEY DATABASE (Local) ======
keys_db = {}

def generate_key(duration_hours=24):
    """Generate a unique key"""
    key = secrets.token_hex(16)
    created = datetime.now()
    expires = created + timedelta(hours=duration_hours)
    keys_db[key] = {
        "created": created.isoformat(),
        "expires": expires.isoformat(),
        "active": True
    }
    return key

def validate_key(key):
    """Check if key is valid"""
    if key not in keys_db:
        return False
    if not keys_db[key]["active"]:
        return False
    if datetime.now() > datetime.fromisoformat(keys_db[key]["expires"]):
        keys_db[key]["active"] = False
        return False
    return True

def expire_key(key):
    """Expire a key"""
    if key in keys_db:
        keys_db[key]["active"] = False
        return True
    return False

# ====== TELEGRAM FUNCTIONS ======
def send_message(chat_id, text, reply_markup=None):
    """Send message with bold + quote style"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        return requests.post(url, json=payload, timeout=10).json()
    except:
        return None

def main_keyboard():
    """Reply keyboard — No inline buttons"""
    return {
        "keyboard": [
            ["🔑 Generate 1 Day Key", "🔑 Generate 7 Day Key"],
            ["🔑 Generate 30 Day Key", "📋 My Keys"],
            ["❌ Expire Key", "📊 Stats"],
            ["ℹ️ Help", "👑 Admin"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

def admin_keyboard():
    """Admin keyboard"""
    return {
        "keyboard": [
            ["🔑 Gen Key (Admin)", "📋 All Keys"],
            ["❌ Expire Key (Admin)", "👥 Add Admin"],
            ["🗑️ Remove Admin", "🔙 Back"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

# ====== STYLE HELPERS ======
def bold(text):
    return f"<b>{text}</b>"

def quote(text):
    return f"<blockquote>{text}</blockquote>"

def code(text):
    return f"<code>{text}</code>"

# ====== COMMAND HANDLERS ======

def handle_start(chat_id):
    message = f"""
{bold('🔥 ULTRA BOMBER — KEY GENERATOR 🔥')}

{quote('Welcome to the most brutal key generator bot!')}

{bold('⚡ What I do:')}
• Generate keys for Ultra Bomber API
• 5 APIs merged — Part1 + Part2 + Ultra + Bomber Pro + Bomber APIs 9ekv
• Infinite bombing — 150 threads — 0.003s delay

{bold('🔑 How to use:')}
• Click a button below to generate a key
• Use the key with the Ultra Bomber API
• Keys expire automatically

{bold('👑 Owner:')} {code(OWNER_ID)}

{bold('📡 API:')} {code(API_URL)}

{quote('Press a button to get started!')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

def handle_genkey(chat_id, duration_hours, duration_text):
    """Generate key with specified duration"""
    key = generate_key(duration_hours)
    message = f"""
{bold('✅ KEY GENERATED SUCCESSFULLY!')}

{quote('Your new API key is ready.')}

🔑 {bold('Key:')} {code(key)}
⏰ {bold('Duration:')} {duration_text}
⏳ {bold('Expires:')} {keys_db[key]['expires']}

📡 {bold('API Endpoint:')}
{code(f'{API_URL}/bomb?phone=9876543210&key={key}')}

⚠️ {bold('Store this key securely!')}
{quote('Keys are not stored after expiry.')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

def handle_mykeys(chat_id):
    """Show user's active keys"""
    active_keys = [k for k, v in keys_db.items() if v["active"]]
    if not active_keys:
        message = f"""
{bold('📋 MY KEYS')}

{quote('You have no active keys.')}

🔑 Generate a key using the buttons below!
"""
        send_message(chat_id, message, reply_markup=main_keyboard())
        return
    
    key_list = "\n".join([f"🔑 {code(k)} — Exp: {keys_db[k]['expires'][:10]}" for k in active_keys[:5]])
    more = f"\n... and {len(active_keys)-5} more" if len(active_keys) > 5 else ""
    
    message = f"""
{bold('📋 MY KEYS')}

{quote(f'You have {len(active_keys)} active keys.')}

{key_list}{more}

📡 {bold('Use with:')}
{code(f'{API_URL}/bomb?phone=9876543210&key=YOUR_KEY')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

def handle_expire(chat_id):
    """Ask for key to expire"""
    active_keys = [k for k, v in keys_db.items() if v["active"]]
    if not active_keys:
        message = f"""
{bold('❌ EXPIRE KEY')}

{quote('No active keys to expire.')}

🔑 Generate a key first!
"""
        send_message(chat_id, message, reply_markup=main_keyboard())
        return
    
    message = f"""
{bold('❌ EXPIRE KEY')}

{quote('Type the key you want to expire:')}

📋 {bold('Active keys:')}
{chr(10).join([f'• {code(k)}' for k in active_keys[:5]])}

{quote('Type /expire KEY to expire a specific key.')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

def handle_expire_key(chat_id, key_to_expire):
    """Expire a specific key"""
    if key_to_expire in keys_db and keys_db[key_to_expire]["active"]:
        keys_db[key_to_expire]["active"] = False
        message = f"""
{bold('✅ KEY EXPIRED!')}

{quote(f'Key {code(key_to_expire)} has been expired.')}

🔑 {bold('Status:')} ❌ Inactive
"""
        send_message(chat_id, message, reply_markup=main_keyboard())
    else:
        message = f"""
{bold('❌ KEY NOT FOUND!')}

{quote(f'Key {code(key_to_expire)} does not exist or is already expired.')}

🔑 {bold('Please check the key and try again.')}
"""
        send_message(chat_id, message, reply_markup=main_keyboard())

def handle_stats(chat_id):
    """Show statistics"""
    total = len(keys_db)
    active = len([k for k, v in keys_db.items() if v["active"]])
    expired = total - active
    
    message = f"""
{bold('📊 ULTRA BOMBER STATS')}

{quote('Key generator statistics:')}

🔑 {bold('Total Keys:')} {total}
✅ {bold('Active:')} {active}
❌ {bold('Expired:')} {expired}

👑 {bold('Owner:')} {code(OWNER_ID)}
📡 {bold('API:')} {code(API_URL)}
🚀 {bold('APIs Merged:')} 5 (Part1 + Part2 + Ultra + Bomber Pro + Bomber APIs 9ekv)

{quote('Brutal bombing — 150 threads — 0.003s delay')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

def handle_help(chat_id):
    message = f"""
{bold('ℹ️ HELP — ULTRA BOMBER KEY GENERATOR')}

{quote('How to use this bot:')}

🔑 {bold('Generate Key:')} Click any duration button
📋 {bold('My Keys:')} View your active keys
❌ {bold('Expire Key:')} Deactivate a key
📊 {bold('Stats:')} View key statistics
👑 {bold('Admin:')} Manage keys and admins

{bold('📡 API Usage:')}
{code(f'{API_URL}/bomb?phone=9876543210&key=YOUR_KEY')}

{bold('👑 Owner:')} {code(OWNER_ID)}

{quote('Keys expire automatically after the selected duration.')}
"""
    send_message(chat_id, message, reply_markup=main_keyboard())

# ====== ADMIN HANDLERS ======
admin_list = [OWNER_ID]

def is_admin(user_id):
    return str(user_id) in admin_list

def handle_admin_panel(chat_id, user_id):
    if not is_admin(user_id):
        message = f"""
{bold('❌ ADMIN ACCESS DENIED!')}

{quote('You are not authorized to access the admin panel.')}

👑 {bold('Contact Owner:')} {code(OWNER_ID)}
"""
        send_message(chat_id, message, reply_markup=main_keyboard())
        return
    
    message = f"""
{bold('👑 ADMIN PANEL')}

{quote('Manage keys and admins:')}

👥 {bold('Admins:')} {', '.join(admin_list)}
🔑 {bold('Total Keys:')} {len(keys_db)}
✅ {bold('Active:')} {len([k for k, v in keys_db.items() if v["active"]])}

{quote('Use the buttons below to manage.')}
"""
    send_message(chat_id, message, reply_markup=admin_keyboard())

def handle_admin_genkey(chat_id):
    """Admin generate key with custom duration"""
    message = f"""
{bold('🔑 ADMIN — GENERATE KEY')}

{quote('Type /genkey DURATION')}

📝 {bold('Examples:')}
• {code('/genkey 1h')} — 1 hour
• {code('/genkey 1d')} — 1 day
• {code('/genkey 7d')} — 7 days
• {code('/genkey 30d')} — 30 days

{quote('Default is 24 hours if no duration specified.')}
"""
    send_message(chat_id, message, reply_markup=admin_keyboard())

def handle_admin_allkeys(chat_id):
    """Show all keys (admin only)"""
    if not keys_db:
        message = f"""
{bold('📋 ALL KEYS')}

{quote('No keys in database.')}
"""
        send_message(chat_id, message, reply_markup=admin_keyboard())
        return
    
    key_list = "\n".join([f"🔑 {code(k)} | {'✅ Active' if v['active'] else '❌ Expired'} | Exp: {v['expires'][:10]}" for k, v in list(keys_db.items())[:10]])
    more = f"\n... and {len(keys_db)-10} more" if len(keys_db) > 10 else ""
    
    message = f"""
{bold('📋 ALL KEYS')}

{quote(f'Total: {len(keys_db)} keys')}

{key_list}{more}
"""
    send_message(chat_id, message, reply_markup=admin_keyboard())

def handle_admin_expire(chat_id):
    """Admin expire key"""
    message = f"""
{bold('❌ ADMIN — EXPIRE KEY')}

{quote('Type /expire KEY to expire a specific key.')}

📋 {bold('Active keys:')}
{chr(10).join([f'• {code(k)}' for k, v in list(keys_db.items()) if v['active']][:5])}
"""
    send_message(chat_id, message, reply_markup=admin_keyboard())

# ====== WEBHOOK ======
@app.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"status": "ok"})
    
    message = data['message']
    chat_id = str(message['chat']['id'])
    text = message.get('text', '').strip()
    user_id = str(message['from']['id'])
    
    # ====== COMMAND HANDLING ======
    
    # START
    if text == '/start':
        handle_start(chat_id)
        return jsonify({"status": "ok"})
    
    # GENKEY BUTTONS
    if text == '🔑 Generate 1 Day Key':
        handle_genkey(chat_id, 24, '1 Day')
        return jsonify({"status": "ok"})
    
    if text == '🔑 Generate 7 Day Key':
        handle_genkey(chat_id, 168, '7 Days')
        return jsonify({"status": "ok"})
    
    if text == '🔑 Generate 30 Day Key':
        handle_genkey(chat_id, 720, '30 Days')
        return jsonify({"status": "ok"})
    
    # MY KEYS
    if text == '📋 My Keys':
        handle_mykeys(chat_id)
        return jsonify({"status": "ok"})
    
    # EXPIRE KEY
    if text == '❌ Expire Key':
        handle_expire(chat_id)
        return jsonify({"status": "ok"})
    
    # STATS
    if text == '📊 Stats':
        handle_stats(chat_id)
        return jsonify({"status": "ok"})
    
    # HELP
    if text == 'ℹ️ Help':
        handle_help(chat_id)
        return jsonify({"status": "ok"})
    
    # ADMIN
    if text == '👑 Admin':
        handle_admin_panel(chat_id, user_id)
        return jsonify({"status": "ok"})
    
    if text == '🔙 Back':
        handle_start(chat_id)
        return jsonify({"status": "ok"})
    
    # ADMIN PANEL BUTTONS
    if text == '🔑 Gen Key (Admin)':
        if is_admin(user_id):
            handle_admin_genkey(chat_id)
        else:
            send_message(chat_id, f"{bold('❌ Access Denied!')}")
        return jsonify({"status": "ok"})
    
    if text == '📋 All Keys':
        if is_admin(user_id):
            handle_admin_allkeys(chat_id)
        else:
            send_message(chat_id, f"{bold('❌ Access Denied!')}")
        return jsonify({"status": "ok"})
    
    if text == '❌ Expire Key (Admin)':
        if is_admin(user_id):
            handle_admin_expire(chat_id)
        else:
            send_message(chat_id, f"{bold('❌ Access Denied!')}")
        return jsonify({"status": "ok"})
    
    if text == '👥 Add Admin':
        if user_id == OWNER_ID:
            send_message(chat_id, f"{bold('👥 ADD ADMIN')}\n\n{quote('Type /addadmin USER_ID')}", reply_markup=admin_keyboard())
        else:
            send_message(chat_id, f"{bold('❌ Only Owner can add admins!')}")
        return jsonify({"status": "ok"})
    
    if text == '🗑️ Remove Admin':
        if user_id == OWNER_ID:
            send_message(chat_id, f"{bold('🗑️ REMOVE ADMIN')}\n\n{quote('Type /removeadmin USER_ID')}\n\n👥 {bold('Current admins:')} {', '.join(admin_list)}", reply_markup=admin_keyboard())
        else:
            send_message(chat_id, f"{bold('❌ Only Owner can remove admins!')}")
        return jsonify({"status": "ok"})
    
    # ====== TEXT COMMANDS ======
    
    # GENKEY COMMAND
    if text.startswith('/genkey'):
        parts = text.split()
        duration_str = parts[1] if len(parts) > 1 else '24h'
        
        # Parse duration
        hours = 24
        if duration_str.endswith('h'):
            hours = int(duration_str[:-1])
        elif duration_str.endswith('d'):
            hours = int(duration_str[:-1]) * 24
        else:
            try:
                hours = int(duration_str)
            except:
                hours = 24
        
        key = generate_key(hours)
        message = f"""
{bold('✅ KEY GENERATED!')}

{quote(f'Duration: {duration_str}')}

🔑 {code(key)}
⏳ Expires: {keys_db[key]['expires']}

📡 {bold('API:')} {code(f'{API_URL}/bomb?phone=9876543210&key={key}')}
"""
        send_message(chat_id, message, reply_markup=admin_keyboard() if is_admin(user_id) else main_keyboard())
        return jsonify({"status": "ok"})
    
    # EXPIRE COMMAND
    if text.startswith('/expire'):
        parts = text.split()
        if len(parts) >= 2:
            key_to_expire = parts[1]
            handle_expire_key(chat_id, key_to_expire)
        else:
            send_message(chat_id, f"{bold('⚠️ Usage:')} {code('/expire KEY')}", reply_markup=main_keyboard())
        return jsonify({"status": "ok"})
    
    # ADD ADMIN
    if text.startswith('/addadmin'):
        if user_id != OWNER_ID:
            send_message(chat_id, f"{bold('❌ Only Owner can add admins!')}")
            return jsonify({"status": "ok"})
        parts = text.split()
        if len(parts) >= 2:
            new_admin = parts[1]
            if new_admin not in admin_list:
                admin_list.append(new_admin)
                send_message(chat_id, f"{bold('✅ Admin Added!')}\n\n{quote(f'{new_admin} is now an admin.')}\n👥 {bold('Admins:')} {', '.join(admin_list)}", reply_markup=admin_keyboard())
            else:
                send_message(chat_id, f"{bold('❌ Already admin!')}", reply_markup=admin_keyboard())
        else:
            send_message(chat_id, f"{bold('⚠️ Usage:')} {code('/addadmin USER_ID')}", reply_markup=admin_keyboard())
        return jsonify({"status": "ok"})
    
    # REMOVE ADMIN
    if text.startswith('/removeadmin'):
        if user_id != OWNER_ID:
            send_message(chat_id, f"{bold('❌ Only Owner can remove admins!')}")
            return jsonify({"status": "ok"})
        parts = text.split()
        if len(parts) >= 2:
            remove_admin = parts[1]
            if remove_admin in admin_list and remove_admin != OWNER_ID:
                admin_list.remove(remove_admin)
                send_message(chat_id, f"{bold('✅ Admin Removed!')}\n\n{quote(f'{remove_admin} is no longer an admin.')}\n👥 {bold('Admins:')} {', '.join(admin_list)}", reply_markup=admin_keyboard())
            elif remove_admin == OWNER_ID:
                send_message(chat_id, f"{bold('❌ Cannot remove owner!')}", reply_markup=admin_keyboard())
            else:
                send_message(chat_id, f"{bold('❌ Not an admin!')}", reply_markup=admin_keyboard())
        else:
            send_message(chat_id, f"{bold('⚠️ Usage:')} {code('/removeadmin USER_ID')}", reply_markup=admin_keyboard())
        return jsonify({"status": "ok"})
    
    # UNKNOWN
    send_message(chat_id, f"{bold('❌ Unknown Command')}\n\n{quote('Use /start to see available options.')}", reply_markup=main_keyboard())
    return jsonify({"status": "ok"})

# ====== HEALTH CHECK ======
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "bot": "Ultra Bomber Key Generator", "owner": OWNER_ID})

@app.route('/')
def home():
    return {
        "status": "🔥 ULTRA BOMBER KEY GENERATOR BOT 🔥",
        "owner": OWNER_ID,
        "admins": admin_list,
        "keys": len(keys_db),
        "webhook": "/telegram/webhook"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
