# main.py
import asyncio
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from config import (
    app, dp, bot as telegram_bot, pyro_app, PORT_NUMBER, logger, db,
    load_admins, load_banned_users, load_keyword_replies
)
from helpers import cleanup_temp_files
from api.routes import api_router

# 'bot' ফোল্ডারের হ্যান্ডলার এবং ওয়ার্কার্স ইম্পোর্ট
import bot.handlers
from bot.workers import video_queue_worker, auto_delete_worker

async def seed_categories():
    # ডেটাবেস থেকে যেকোনো পুরোনো ডেটা ক্লিন করে ক্রমানুসারে নতুন ক্যাটাগরি সেট করবে
    has_old_home = await db.categories.find_one({"name": "Home"})
    count = await db.categories.count_documents({})
    
    if has_old_home or count == 0:
        await db.categories.delete_many({}) # পুরোনো ডেটা ক্লিন করা হচ্ছে
        defaults = [
            {"name": "Latest", "icon": "fa-solid fa-clock", "order": 1},
            {"name": "For You", "icon": "✦", "order": 2}, # স্পেশাল ✦ ক্যারেক্টার আইকন
            {"name": "Trending", "icon": "fa-solid fa-fire", "order": 3},
            {"name": "Movies", "icon": "fa-solid fa-film", "order": 4},
            {"name": "Web-Series", "icon": "fa-solid fa-circle-play", "order": 5},
            {"name": "Hindi", "icon": "fa-solid fa-masks-theater", "order": 6},
            {"name": "Action", "icon": "fa-solid fa-hand-fist", "order": 7},
            {"name": "Anime", "icon": "fa-solid fa-ghost", "order": 8},
            {"name": "Bangla", "icon": "fa-solid fa-clapperboard", "order": 9},
            {"name": "Bangla Dubbed", "icon": "fa-solid fa-comment-dots", "order": 10},
            {"name": "Dual Audio", "icon": "fa-solid fa-headphones", "order": 11},
            {"name": "English", "icon": "fa-solid fa-video", "order": 12},
            {"name": "Hindi Dubbed", "icon": "fa-solid fa-comments", "order": 13},
            {"name": "Horror", "icon": "fa-solid fa-skull", "order": 14},
            {"name": "18+ Adult", "icon": "fa-solid fa-user-lock", "order": 15},
            {"name": "Korean", "icon": "fa-solid fa-tv", "order": 16}
        ]
        await db.categories.insert_many(defaults)
        logger.info("Database categories initialized in custom sequence.")

# CORS মিডেলওয়্যার কনফিগারেশন
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# এপিআই রাউটস রেজিস্টার
app.include_router(api_router)

# আপকামিং রাউটার রেজিস্টার
try:
    from upcoming_router import upcoming_router
    app.include_router(upcoming_router)
    logger.info("Upcoming router registered successfully.")
except ImportError:
    logger.warning("upcoming_router.py not found.")

# কাস্টম ইউভিকর্ন সার্ভার
class CustomUvicornServer(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        pass

# ডাটাবেস ইনডেক্সিং এবং ইনিশিয়ালাইজেশন
async def init_db():
    await db.movies.create_index([("title", "text")])
    await db.movies.create_index("created_at")
    await db.auto_delete.create_index("delete_at")
    try:
        await db.payments.create_index("trx_id", unique=True)
    except Exception: pass
    await db.ads.create_index("expires_at")
    await db.movie_views.create_index([("title", 1), ("viewed_at", -1)])
    try:
        await db.movie_views.create_index("viewed_at", expireAfterSeconds=2592000) 
    except Exception: pass

# 🚀 রেন্ডার পোর্ট-বাইন্ডিং সমস্যার সমাধান (FastAPI Startup Event)
@app.on_event("startup")
async def startup_event():
    cleanup_temp_files()
    
    try:
        await init_db()
        await seed_categories()
        await db.file_cache.delete_many({})
        logger.info("Database and static seeding initialized.")
    except Exception as e:
        logger.error(f"Database startup failed: {e}")
        
    try:
        await load_admins()
        await load_banned_users()
        await load_keyword_replies()
        logger.info("Caches loaded successfully.")
    except Exception as e:
        logger.error(f"Caches failed to load: {e}")

    # পাইরোগ্রাম ব্যাকগ্রাউন্ডে স্টার্ট করা হচ্ছে
    try:
        await pyro_app.start()
        logger.info("Pyrogram client started.")
    except Exception as e:
        logger.error(f"Pyrogram startup bypassed: {e}")
        
    # ব্যাকগ্রাউন্ড সিডিউলার ওয়ার্কার
    asyncio.create_task(auto_delete_worker())
    asyncio.create_task(video_queue_worker()) 
    
    # বট পোলিং ব্যাকগ্রাউন্ড টাস্ক হিসেবে রান হবে (Uvicorn-কে ব্লক করবে না)
    try:
        await telegram_bot.delete_webhook(drop_pending_updates=True)
        asyncio.create_task(dp.start_polling(telegram_bot))
        logger.info("Telegram Bot polling started concurrently.")
    except Exception as e:
        logger.error(f"Failed to clear webhook or start polling: {e}")

if __name__ == "__main__": 
    # সার্ভার সরাসরি রান করা হচ্ছে, যা রেন্ডারের পোর্টের সাথে সাথে বাইন্ড হবে
    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=PORT_NUMBER, 
        loop="asyncio"
    )
    server = CustomUvicornServer(config)
    server.run()
