import os

class Config:
    API_ID = int(os.environ.get("API_ID", "12345"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    # Pyrogram session string for 4GB uploads
    ADMIN_SESSION_STRING = os.environ.get("ADMIN_SESSION_STRING", "")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://...")
    
    ADMINS = [12345678, 87654321] # List of Admin User IDs
    FORCE_SUB_CHANNELS = ["zerodev2", "mvxyoffcail"]
    MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024 
    DOWNLOAD_LOCATION = "./downloads"
