# 🤖 Advanced Video Stream Editor Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pyrogram-Framework-26A69A?style=for-the-badge&logo=telegram&logoColor=white" alt="Pyrogram">
  <img src="https://img.shields.io/badge/FFmpeg-Multimedia-007808?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg">
  <img src="https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## 🎬 Overview
**Advanced Video Stream Editor Bot** is a high-performance Telegram bot built with **Pyrogram**. It utilizes a dual-client system (Bot + User Session) to bypass standard API limits, allowing users to upload and process video files up to **4GB**.

Whether you need to strip audio tracks, extract subtitles, or remux metadata, this bot handles it all using the power of **FFmpeg**.

---

## ✨ Key Features
* 🚀 **4GB Support:** Process large files using an Admin Session string.
* 🔄 **Stream Mapping:** Selectively keep or remove Video, Audio, and Subtitle streams.
* 🖼️ **Thumbnail Extraction:** Grab high-quality frames from any timestamp.
* 📋 **Metadata Editor:** Modify video titles, authors, and global tags.
* 📤 **Stream Extraction:** Extract internal subtitles (.srt) or audio (.m4a/.mp3) as separate files.
* 🛡️ **Force Subscription:** Built-in membership verification for channel growth.
* 📊 **Admin Dashboard:** Broadcast messages and track user statistics.

---

## 🛠️ Technical Stack
- **Framework:** [Pyrogram](https://github.com/pyrogram/pyrogram) (Asynchronous Telegram Framework)
- **Engine:** [FFmpeg](https://ffmpeg.org/) (Multimedia processing)
- **Database:** [MongoDB](https://www.mongodb.com/) (User management & stats)
- **Storage:** [Motor](https://motor.readthedocs.io/) (Async MongoDB driver)
- **Environment:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Installation & Setup

### 1️⃣ Local Deployment
```bash
# Clone the repository
git clone [https://github.com/yourusername/stream-editor-bot.git](https://github.com/yourusername/stream-editor-bot.git)
cd stream_editor_bot

# Install dependencies
pip install -r requirements.txt

# Configure .env or config.py with your credentials
python3 main.py

```
### 2️⃣ Docker Deployment (Recommended)
```bash
# Build and run the container
docker-compose up -d --build

```
## 🔐 Configuration (config.py)
| Variable | Description |
|---|---|
| API_ID | Your Telegram API ID from my.telegram.org |
| API_HASH | Your Telegram API Hash |
| BOT_TOKEN | Your Bot Token from @BotFather |
| ADMIN_SESSION_STRING | Pyrogram String Session for 4GB uploads |
| MONGO_URI | Your MongoDB connection string |
| FORCE_SUB_CHANNELS | List of channel usernames (without @) |
## 🤝 Credits
 * **Developer:** @Zerodev
 * **Support:** @venuboyy_
 * **Base:** Powered by Pyrogram
## 📜 License
Distributed under the **MIT License**. See LICENSE for more information.
<p align="center">
Built with ❤️ and 🐍 by <b>ZeroDev</b>
</p>
