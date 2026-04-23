# Alternative Extractor Bot

Forward any UploadPilotBot message → Bot automatically delivers the **first quality** video/PDF. No wait, no clicking.

---

## 🧠 How It Works

```
Channel message (720p/480p buttons)
        ↓
Forward to any group/chat
        ↓
Bot detects first inline button URL
(t.me/UploadPilotbot?start=file_xxxx)
        ↓
Userbot sends /start file_xxxx to UploadPilotBot
        ↓
File delivered to your chat ⚡
```

---

## ⚙️ Setup (5 steps)

### Step 1 — Telegram Credentials

1. Go to https://my.telegram.org → **API development tools**
2. Create an app → copy `API_ID` and `API_HASH`
3. Create a bot via [@BotFather](https://t.me/BotFather) → copy `BOT_TOKEN`

---

### Step 2 — Fill API_ID & API_HASH in code

Open `bot/main.py` — line 14-15:
```python
API_ID   = 123456               # Apna API ID
API_HASH = "your_api_hash_here" # Apna API HASH
```

Open `utils/gen_session.py` — line 13-14 — same values dalo.

---

### Step 3 — Generate SESSION_STRING (ONCE, locally)

```bash
pip install -r requirements.txt
python utils/gen_session.py
```

- Apna phone number dalo (international format: +91xxxxxxxxxx)
- OTP dalo
- Terminal mein ek **lambi string** print hogi — wahi SESSION_STRING hai
- Isko copy karke safe rakh lo

> ⚠️ **SESSION_STRING = apne Telegram account ka access. Kisi ko mat dena!**

---

### Step 4 — Deploy on Render.com

1. Ye repo GitHub pe push karo
2. [render.com](https://render.com) → **New → Web Service**
3. GitHub repo connect karo
4. Settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. **Environment Variables** add karo:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | BotFather se mila token |
| `SESSION_STRING` | Step 3 se generate ki hui string |
| `PORT` | `8080` |

6. **Deploy** karo ✅

---

### Step 5 — Add Bot to Group

- Bot ko group mein add karo
- Admin banao with: **Read Messages + Send Messages + Delete Messages**
- Koi bhi group mein forward kare — bot serve karega (no restrictions!)

---

## 🤖 Commands

| Command | Description |
|---------|-------------|
| `/start` | Bot info |
| `/queue` | Queue status |

---

## 📌 Key Behaviors

- ✅ **Sirf pehla button** — 4 buttons mein se pehla (usually best quality) deliver hoga
- ✅ **No restrictions** — koi bhi group, koi bhi user use kar sakta hai
- ✅ **Super fast** — 3 second response time
- ✅ Userbot + Bot dono saath chalte hain

---

## 📁 Project Structure

```
Alternative/
├── app.py                  # Entry point
├── bot/
│   └── main.py             # All handlers & logic
├── utils/
│   └── gen_session.py      # Session string generator (run once)
├── requirements.txt
├── Dockerfile
├── render.yaml
└── README.md
```

---

## ⚠️ Important Notes

- `SESSION_STRING` = apna personal Telegram account — **kabhi share mat karo**
- Bot must be **Admin** in group
- Python **3.12+** required
