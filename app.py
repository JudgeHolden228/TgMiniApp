import hashlib
import hmac
import base64

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

def verify_telegram_signature(init_data):
    secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
    check_string = "\n".join(f"{key}={value}" for key, value in sorted(init_data.items()) if key != "hash")
    hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    return hash == init_data.get("hash")
