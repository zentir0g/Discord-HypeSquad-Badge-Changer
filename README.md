<div align="center">

# 🎭 Discord HypeSquad Badge Changer

### *Mass Change HypeSquad Badges on Multiple Discord Accounts*

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join-7289DA.svg)](https://discord.gg/zUN5DE6CrW)

</div>

---

## 📺 Video Tutorial

<div align="center">
  
[![Click to Watch Tutorial](https://img.youtube.com/vi/NJ4y_el5iG4/0.jpg)](https://www.youtube.com/watch?v=NJ4y_el5iG4)

**Click the image to watch the full tutorial**

</div>

---

## ✨ Features

- ⚡ **Lightning Fast** - Process hundreds of tokens in seconds
- 🎲 **Random Mode** - Assign random badges to each account
- 🎯 **Specific Mode** - Assign same badge to all accounts
- 🔄 **Auto Rate Limit** - Handles Discord rate limits automatically
- 📊 **Live Progress** - Real-time progress tracking
- 💾 **Save Results** - Exports results to `results.txt`
- 🚀 **Multi-threaded** - Optimized for maximum performance

---

## 🎮 Badge Options

| Option | Badge | Emoji |
|--------|-------|-------|
| 1 | Bravery | 🦁 |
| 2 | Brilliance | 💡 |
| 3 | Balance | ⚖️ |
| 4 | Leave HypeSquad | 🚪 |

---

## 📋 Requirements

- Python 3.8 or higher
- Discord accounts with valid tokens

---

## 🚀 Quick Start

### 1. Install Requirements

```bash
pip install requests colorama
```

### 2. Get Your Discord Tokens

**Browser Method:**
1. Open Discord in your browser
2. Press `F12` → Go to **Application** tab
3. Click **Local Storage** → `https://discord.com`
4. Find `token` and copy the value

### 3. Create `tokens.txt`

Create a file named `tokens.txt` in the script folder:

```txt
# Add your tokens here (one per line)
your_discord_token_here
another_token_here
third_token_here
```

### 4. Run the Script

```bash
python hypesquad_changer.py
```

---

## 📖 How to Use

1. **Launch the script** - It will load all tokens from `tokens.txt`

2. **Choose mode:**
   - `1` - Same badge for all tokens
   - `2` - Random badge for each token

3. **If using Specific Mode:** Choose badge number (1-4)

4. **Type `yes`** to confirm and start

5. **Watch the magic happen** ✨

### Example Output

```
[✓] ...vo48fiCH7g | 🦁 Joined Bravery
[✓] ...k9dR_jMGnk | 💡 Joined Brilliance  
[✓] ...Jx0GHBrdjk | ⚖️ Joined Balance
[12/16] ✓ ...jfzOh92Tx4 | 🦁 Joined Bravery
```

---

## 📊 Results

After completion, check `results.txt` for detailed output:

```
HypeSquad Badge Changer Results
==================================================
Mode: Random - Random Badge
Total Tokens: 16
Successful: 16
Failed: 0
==================================================
```

---

## ⚡ Performance

| Tokens | Time |
|--------|------|
| 10 | ~2 seconds |
| 50 | ~5 seconds |
| 100 | ~10 seconds |
| 500 | ~45 seconds |

---

## ⚠️ Warning

> **This tool is for educational purposes only**

- Using self-bots violates Discord's Terms of Service
- Your accounts may be banned if detected
- Never share your tokens with anyone
- Use at your own risk

---

## 🐛 Common Issues

**"No tokens found"**
- Make sure `tokens.txt` exists and has valid tokens

**"HTTP 401 / Unauthorized"**
- Your token is invalid or expired
- Get a fresh token from Discord

**"Rate limited"**
- Normal behavior, script will wait automatically
- Discord is limiting your requests

---

## 📁 Files

```
hypesquad-changer/
├── hypesquad_changer.py   # Main script
├── tokens.txt              # Your tokens (create this)
├── results.txt             # Auto-generated results
└── README.md               # This file
```

---

## 👨‍💻 Credits

**Created by Harry Uchiha (vvoh)**

[![Discord](https://img.shields.io/badge/Join_Our_Discord_Server-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/zUN5DE6CrW)

---

## 📜 License

MIT License - Free for personal and educational use

---

<div align="center">

### ⭐ Star this repo if you found it useful!

**Made with ❤️ by Harry Uchiha (vvoh)**

</div>
