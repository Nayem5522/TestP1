# api/routes.py
import datetime
import json
import random
import aiohttp
import html
from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from bson import ObjectId
import copy

from config import (
    db, bot, OWNER_ID, BOT_USERNAME, DB_CHANNEL_ID,
    admin_cache, banned_cache, trending_cache, list_cache, category_cache,
    clear_app_cache, TOKEN, logger
)
from helpers import validate_tg_data, verify_admin, format_views
from html_template import HTML_CODE

api_router = APIRouter()

# ==========================================
# 🛑 Pydantic Models for API Requests
# ==========================================
class UserManageModel(BaseModel):
    user_id: int
    action: str
    value: int = 0

class UserActionModel(BaseModel):
    uid: int
    initData: str

class ViewRequestModel(BaseModel):
    title: str

class LikeRequestModel(BaseModel):
    uid: int
    title: str
    initData: str

class SendRequestModel(BaseModel):
    userId: int
    movieId: str
    initData: str

class ReqModel(BaseModel):
    uid: int
    uname: str
    movie: str
    initData: str

class AdCreateModel(BaseModel):
    uid: int
    initData: str
    title: str
    subtitle: str = "দেরি না করে এখনো সবাই নিয়ে নিন"
    link: str
    image_url: str
    package: int

class AdminAdModel(BaseModel):
    title: str
    subtitle: str = "দেরি না করে এখনো সবাই নিয়ে নিন"
    link: str
    image_url: str

class WatchlistModel(BaseModel):
    uid: int
    title: str
    initData: str

class ReviewModel(BaseModel):
    uid: int
    uname: str
    title: str
    rating: int = 0
    review: str = ""
    reply_to: str = ""
    initData: str

class CommentLikeModel(BaseModel):
    uid: int
    comment_id: str
    initData: str

# ==========================================
# 🛑 System Settings API
# ==========================================
@api_router.get("/api/admin/sys_settings")
async def get_sys_settings(auth: bool = Depends(verify_admin)):
    cost_cfg = await db.settings.find_one({"id": "vip_cost"})
    days_cfg = await db.settings.find_one({"id": "vip_days"})
    unlock_cfg = await db.settings.find_one({"id": "unlock_hours"})
    social_cfg = await db.settings.find_one({"id": "social_links"})
    interval_cfg = await db.settings.find_one({"id": "ad_interval"}) 
    
    return {
        "vip_cost": cost_cfg["amount"] if cost_cfg else 30,
        "vip_days": days_cfg["days"] if days_cfg else 1,
        "unlock_hours": unlock_cfg["hours"] if unlock_cfg else 24,
        "ad_interval": interval_cfg["interval"] if interval_cfg else 3, 
        "social_links": social_cfg.get("links", {}) if social_cfg else {}
    }

@api_router.post("/api/admin/sys_settings")
async def save_sys_settings(data: dict = Body(...), auth: bool = Depends(verify_admin)):
    await db.settings.update_one({"id": "vip_cost"}, {"$set": {"amount": int(data.get("vip_cost", 30))}}, upsert=True)
    await db.settings.update_one({"id": "vip_days"}, {"$set": {"days": int(data.get("vip_days", 1))}}, upsert=True)
    await db.settings.update_one({"id": "unlock_hours"}, {"$set": {"hours": int(data.get("unlock_hours", 24))}}, upsert=True)
    await db.settings.update_one({"id": "ad_interval"}, {"$set": {"interval": int(data.get("ad_interval", 3))}}, upsert=True) 
    
    social_links = data.get("social_links", {})
    await db.settings.update_one({"id": "social_links"}, {"$set": {"links": social_links}}, upsert=True)
    
    clear_app_cache()
    return {"ok": True}

# ==========================================
# 🛑 Render Web UI (Frontend Page)
# ==========================================
@api_router.get("/", response_class=HTMLResponse)
async def web_ui():
    tg_cfg = await db.settings.find_one({"id": "link_tg"})
    support_cfg = await db.settings.find_one({"id": "link_support"})
    b18_cfg = await db.settings.find_one({"id": "link_18"})
    dl_cfg = await db.settings.find_one({"id": "direct_links"})
    
    ad_time_cfg = await db.settings.find_one({"id": "ad_time"})
    ad_wait_seconds = ad_time_cfg['seconds'] if ad_time_cfg else 10
    
    interval_cfg = await db.settings.find_one({"id": "ad_interval"})
    ad_interval = interval_cfg["interval"] if interval_cfg else 3
    
    tg_url = tg_cfg['url'] if tg_cfg else "https://t.me/PrimeCineZone"
    support_link = support_cfg['url'] if support_cfg else "https://t.me/Prime_Support_Group"
    link_18 = b18_cfg['url'] if b18_cfg else "https://t.me/PrimeCineZone"
    direct_links = dl_cfg.get('links', []) if dl_cfg else []
    dl_json = json.dumps(direct_links)
    
    social_cfg = await db.settings.find_one({"id": "social_links"})
    social_links_dict = social_cfg.get('links', {}) if social_cfg else {}
    social_json = json.dumps(social_links_dict)

    compiled_html = HTML_CODE.replace(
        "{{DIRECT_LINKS}}", dl_json
    ).replace(
        "{{TG_LINK}}", tg_url
    ).replace(
        "{{SUPPORT_LINK}}", support_link
    ).replace(
        "{{LINK_18}}", link_18
    ).replace(
        "{{BOT_USER}}", BOT_USERNAME
    ).replace(
        "{{AD_TIME}}", str(ad_wait_seconds)
    ).replace(
        "{{AD_INTERVAL}}", str(ad_interval)
    ).replace(
        "{{SOCIAL_LINKS}}", social_json
    )
    return compiled_html

# ==========================================
# 🛑 Gamification & Check-in APIs
# ==========================================
@api_router.get("/api/user/{uid}")
async def get_user_info(uid: int):
    now = datetime.datetime.utcnow()
    await db.users.update_one({"user_id": uid}, {"$set": {"last_active": now}})
    
    user = await db.users.find_one({"user_id": uid})
    is_admin = uid in admin_cache
    
    cost_cfg = await db.settings.find_one({"id": "vip_cost"})
    days_cfg = await db.settings.find_one({"id": "vip_days"})
    
    cost = cost_cfg["amount"] if cost_cfg else 30
    days = days_cfg["days"] if days_cfg else 1

    if not user: return {"vip": False, "admin": is_admin, "coins": 0, "vip_cost": cost, "vip_days": days}
    return {
        "vip": user.get("vip_until", now) > now, 
        "admin": is_admin,
        "coins": user.get("coins", 0),
        "vip_cost": cost,
        "vip_days": days
    }

@api_router.post("/api/add_coin")
async def add_coin_api(d: UserActionModel):
    if d.uid == 0 or not validate_tg_data(d.initData): return {"ok": False}
    await db.users.update_one({"user_id": d.uid}, {"$inc": {"coins": 5}})
    return {"ok": True}

@api_router.post("/api/buy_vip")
async def buy_vip_api(d: UserActionModel):
    if d.uid == 0 or not validate_tg_data(d.initData): return {"ok": False}
    user = await db.users.find_one({"user_id": d.uid})
    coins = user.get("coins", 0)
    
    cost_cfg = await db.settings.find_one({"id": "vip_cost"})
    days_cfg = await db.settings.find_one({"id": "vip_days"})
    cost = cost_cfg["amount"] if cost_cfg else 30
    days = days_cfg["days"] if days_cfg else 1
    
    if coins < cost: return {"ok": False, "msg": f"Not enough points! Need {cost} points."}
    
    now = datetime.datetime.utcnow()
    current_vip = user.get("vip_until", now) if user.get("vip_until") else now
    if current_vip < now: current_vip = now
    new_vip = current_vip + datetime.timedelta(days=days)
    
    await db.users.update_one({"user_id": d.uid}, {"$inc": {"coins": -cost}, "$set": {"vip_until": new_vip}})
    return {"ok": True}

# ==========================================
# 🛑 Movies Data APIs
# ==========================================
@api_router.get("/api/trending")
async def trending_movies(uid: int = 0):
    unlocked_ids = []
    cfg_unlock = await db.settings.find_one({"id": "unlock_hours"})
    unlock_hrs = cfg_unlock['hours'] if cfg_unlock else 24
    if uid != 0:
        time_limit = datetime.datetime.utcnow() - datetime.timedelta(hours=unlock_hrs)
        async for u in db.user_unlocks.find({"user_id": uid, "unlocked_at": {"$gt": time_limit}}):
            unlocked_ids.append(u["movie_id"])

    if "trending_list" in trending_cache:
        movies = copy.deepcopy(trending_cache["trending_list"])
    else:
        seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        pipeline = [
            {"$group": {
                "_id": "$title", 
                "photo_id": {"$first": "$photo_id"}, 
                "db_photo_id": {"$first": "$db_photo_id"},
                "badge": {"$first": "$badge"},
                "clicks": {"$sum": "$clicks"}, 
                "likes": {"$first": "$likes"},
                "downloads": {"$first": "$downloads"},
                "files": {"$push": {"id": {"$toString": "$_id"}, "quality": {"$ifNull": ["$quality", "HD"]}}}
            }},
            {"$lookup": {
                "from": "movie_views",
                "let": {"movie_title": "$_id"},
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": ["$title", "$$movie_title"]},
                                {"$gte": ["$viewed_at", seven_days_ago]}
                            ]
                        }
                    }},
                    {"$count": "count"}
                ],
                "as": "weekly"
            }},
            {"$addFields": {
                "weekly_clicks": {"$ifNull": [{"$arrayElemAt": ["$weekly.count", 0]}, 0]}
            }},
            {"$sort": {"weekly_clicks": -1, "clicks": -1}},
            {"$limit": 10}
        ]
        movies = await db.movies.aggregate(pipeline).to_list(10)
        for m in movies:
            m["photo_id"] = m.get("photo_id") or (f"db_{m['db_photo_id']}" if m.get("db_photo_id") else None)
        trending_cache["trending_list"] = movies
        movies = copy.deepcopy(movies)

    for m in movies:
        for f in m["files"]: f["is_unlocked"] = f["id"] in unlocked_ids
    return movies

@api_router.get("/api/categories")
async def get_categories():
    cursor = db.categories.find().sort("order", 1)
    categories = await cursor.to_list(length=100)
    result = []
    for c in categories:
        result.append({"name": c["name"], "icon": c.get("icon", "fa-solid fa-film")})
    return result

@api_router.get("/api/list")
async def list_movies(page: int = 1, q: str = "", uid: int = 0, cat: str = ""):
    unlocked_ids = []
    cfg_unlock = await db.settings.find_one({"id": "unlock_hours"})
    unlock_hrs = cfg_unlock['hours'] if cfg_unlock else 24
    if uid != 0:
        time_limit = datetime.datetime.utcnow() - datetime.timedelta(hours=unlock_hrs)
        async for u in db.user_unlocks.find({"user_id": uid, "unlocked_at": {"$gt": time_limit}}):
            unlocked_ids.append(u["movie_id"])

    cache_key = f"{page}_{q}_{cat}"
    if cache_key in list_cache:
        data = copy.deepcopy(list_cache[cache_key])
        movies = data["movies"]
        total_pages = data["total_pages"]
    else:
        limit = 100  
        skip = (page - 1) * limit
        match_stage = {}
        if q: match_stage["title"] = {"$regex": q, "$options": "i"}

        if cat == "For You":
            sort_stage = {"clicks": -1}
        else:
            sort_stage = {"created_at": -1}
            if cat: match_stage["categories"] = cat

        pipeline = [
            {"$match": match_stage},
            {"$group": {
                "_id": "$title", 
                "photo_id": {"$first": "$photo_id"}, 
                "db_photo_id": {"$first": "$db_photo_id"}, 
                "badge": {"$first": "$badge"}, 
                "clicks": {"$sum": "$clicks"}, 
                "likes": {"$first": "$likes"},
                "downloads": {"$first": "$downloads"},
                "created_at": {"$max": "$created_at"}, 
                "files": {"$push": {"id": {"$toString": "$_id"}, "quality": {"$ifNull": ["$quality", "HD"]}}}
            }},
            {"$sort": sort_stage}, {"$skip": skip}, {"$limit": limit}
        ]
        total_groups = (await db.movies.aggregate([{"$match": match_stage}, {"$group": {"_id": "$title"}}, {"$count": "total"}]).to_list(1))
        total_pages = (total_groups[0]["total"] + limit - 1) // limit if total_groups else 0
        movies = await db.movies.aggregate(pipeline).to_list(limit)
        for m in movies:
            m["photo_id"] = m.get("photo_id") or (f"db_{m['db_photo_id']}" if m.get("db_photo_id") else None)
        list_cache[cache_key] = {"movies": movies, "total_pages": total_pages}
        movies = copy.deepcopy(movies)

    for m in movies:
        for f in m["files"]: f["is_unlocked"] = f["id"] in unlocked_ids
    return {"movies": movies, "total_pages": total_pages}

# 🛑 AUTO-REPAIRING SYSTEM FOR PORTED THUMBNAILS
@api_router.get("/api/image/{photo_id}")
async def get_image(photo_id: str):
    try:
        cache = await db.file_cache.find_one({"photo_id": photo_id})
        now = datetime.datetime.utcnow()
        file_path = None
        
        if cache and cache.get("expires_at", now) > now: 
            file_path = cache["file_path"]
        else:
            actual_file_id = photo_id
            db_msg_id = None
            
            if photo_id.startswith("db_"):
                parts = photo_id.split("_")
                if len(parts) > 1 and parts[1].isdigit():
                    db_msg_id = int(parts[1])
                movie = await db.movies.find_one({"db_photo_id": db_msg_id})
                if movie and movie.get("photo_id"): 
                    actual_file_id = movie["photo_id"]
            else:
                movie = await db.movies.find_one({"photo_id": photo_id})
                if movie and movie.get("db_photo_id"):
                    db_msg_id = movie["db_photo_id"]
            
            try:
                file_path = (await bot.get_file(actual_file_id)).file_path
            except Exception:
                if db_msg_id and DB_CHANNEL_ID:
                    try:
                        forwarded = await bot.forward_message(
                            chat_id=DB_CHANNEL_ID,
                            from_chat_id=DB_CHANNEL_ID,
                            message_id=db_msg_id
                        )
                        if forwarded.photo:
                            new_photo_id = forwarded.photo[-1].file_id
                            await bot.delete_message(chat_id=DB_CHANNEL_ID, message_id=forwarded.message_id)
                            await db.movies.update_many(
                                {"db_photo_id": db_msg_id}, 
                                {"$set": {"photo_id": new_photo_id}}
                            )
                            file_path = (await bot.get_file(new_photo_id)).file_path
                    except Exception as err:
                        logger.error(f"Image auto-repair failed: {err}")
                    
        if file_path:
            await db.file_cache.update_one(
                {"photo_id": photo_id}, 
                {"$set": {"file_path": file_path, "expires_at": now + datetime.timedelta(minutes=50)}}, 
                upsert=True
            )
            
        if not file_path: return {"error": "not found"}
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        async def stream_image():
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as resp:
                    if resp.status != 200:
                        await db.file_cache.delete_one({"photo_id": photo_id})
                        yield b""
                        return
                    async for chunk in resp.content.iter_chunked(1024): yield chunk
        return StreamingResponse(stream_image(), media_type="image/jpeg")
    except Exception as e: 
        logger.error(f"get_image error: {e}")
        return {"error": "error"}

@api_router.post("/api/view_movie")
async def increment_movie_view(d: ViewRequestModel):
    try:
        await db.movies.update_many({"title": d.title}, {"$inc": {"clicks": 1}})
        await db.movie_views.insert_one({"title": d.title, "viewed_at": datetime.datetime.utcnow()})
    except Exception: pass
    return {"ok": True}

# 🛑 লাইভ লাইক এন্ডপয়েন্ট
@api_router.post("/api/movie/like")
async def toggle_like_movie(d: LikeRequestModel):
    if d.uid == 0 or not validate_tg_data(d.initData): return {"ok": False}
    try:
        existing = await db.movie_likes.find_one({"uid": d.uid, "title": d.title})
        if existing:
            await db.movie_likes.delete_one({"_id": existing["_id"]})
            await db.movies.update_many({"title": d.title}, {"$inc": {"likes": -1}})
            is_liked = False
        else:
            await db.movie_likes.insert_one({"uid": d.uid, "title": d.title, "created_at": datetime.datetime.utcnow()})
            await db.movies.update_many({"title": d.title}, {"$inc": {"likes": 1}})
            is_liked = True
            
        total_likes = await db.movie_likes.count_documents({"title": d.title})
        return {"ok": True, "is_liked": is_liked, "total_likes": total_likes}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# 🛑 মুভি ফুল ডিটেইলস মেটাডাটা
@api_router.get("/api/movie/meta/{title}")
async def get_movie_meta(title: str, uid: int = 0):
    try:
        movie = await db.movies.find_one({"title": title})
        total_likes = await db.movie_likes.count_documents({"title": title})
        is_liked = False
        if uid != 0:
            is_liked = (await db.movie_likes.find_one({"uid": uid, "title": title})) is not None
            
        total_downloads = movie.get("downloads", 0) if movie else 0
        total_comments = await db.reviews.count_documents({"movie_title": title, "review": {"$ne": ""}})
        
        # রেটিং
        reviews = await db.reviews.find({"movie_title": title, "rating": {"$gt": 0}}).to_list(100)
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0.0
        total_ratings_count = len(reviews)

        user_rating = 0
        if uid != 0:
            u_rev = await db.reviews.find_one({"movie_title": title, "user_id": uid})
            if u_rev: user_rating = u_rev.get("rating", 0)

        return {
            "likes": total_likes,
            "is_liked": is_liked,
            "downloads": total_downloads,
            "comments_count": total_comments,
            "avg_rating": round(avg_rating, 1),
            "ratings_count": total_ratings_count,
            "user_rating": user_rating
        }
    except Exception:
        return {"likes": 0, "is_liked": False, "downloads": 0, "comments_count": 0, "avg_rating": 0.0, "ratings_count": 0, "user_rating": 0}

# ==========================================
# 🛑 PREMIUM MOVIE DELIVERY & REFERRAL SYSTEM
# ==========================================
@api_router.post("/api/send")
async def send_file(d: SendRequestModel):
    if d.userId == 0 or not validate_tg_data(d.initData): return {"ok": False}
    try:
        m = await db.movies.find_one({"_id": ObjectId(d.movieId)})
        if m:
            now = datetime.datetime.utcnow()
            user = await db.users.find_one({"user_id": d.userId})
            is_vip = user and user.get("vip_until", now) > now
            
            time_cfg = await db.settings.find_one({"id": "del_time"})
            del_minutes = time_cfg['minutes'] if time_cfg else 60
            protect_cfg = await db.settings.find_one({"id": "protect_content"})
            is_protected = protect_cfg['status'] if protect_cfg else True
            
            escaped_name = html.escape(user.get("first_name", "User") if user else "User")
            m_title = html.escape(m['title'])
            ref_link = f"https://t.me/{BOT_USERNAME}?start=ref_{d.userId}"
            
            delivery_wishes = [
                f"🍿 <b>Hey {escaped_name}!</b> Here is your movie '<b>{m_title}</b>' 🎬\n\nমুভিটা দেখার সময় বন্ধুদের ভুলো না কিন্তু! নিচে তোমার স্পেশাল শেয়ার লিংকটি দিলাম, বন্ধুদের সাথে শেয়ার করলেই পেয়ে যাবে ফ্রি Gems। একসাথে দেখার মজাই আলাদা! 😍\n\n🔗 <b>Your Invite Link:</b> <code>{ref_link}</code>",
                f"🍿 <b>আরে {escaped_name}!</b> তোমার কাঙ্ক্ষিত মুভি '<b>{m_title}</b>' নিয়ে আমি হাজির! 🎬\n\nমুভিটা কেমন লাগলো আমাকে জানাতে ভুলো না কিন্তু! আর হ্যাঁ, নিচের ইনভাইট লিংকটি বন্ধুদের পাঠিয়ে ফ্রিতে Gems নিয়ে নাও, একসাথে দেখলে আনন্দ দ্বিগুণ হবে! 😉❤️\n\n🔗 <b>Your Invite Link:</b> <code>{ref_link}</code>",
                f"🍿 <b>রিল্যাক্স {escaped_name}!</b> তোমার পছন্দের মুভি '<b>{m_title}</b>' এসে গেছে! 🎬\n\nপপকর্ন নিয়ে রেডি তো? মুভিটা বন্ধুদের সাথে শেয়ার করতে চাইলে নিচের লিংকটি কপি করে পাঠিয়ে দাও। শেয়ার করলেই পাবে ফ্রিতে Gems! 🍿✨\n\n🔗 <b>Your Invite Link:</b> <code>{ref_link}</code>"
            ]
            maya_wish = random.choice(delivery_wishes)
            
            caption = f"{maya_wish}\n\n📥 Join: @PrimeCineZone"
            if not is_vip: caption += f"\n\n⏳ <i>সতর্কতা: সিকিউরিটির জন্য এই ভিডিওটি <b>{del_minutes} মিনিট</b> পর অটোমেটিক ডিলিট হয়ে যাবে!</i>"
            
            db_file_id = m.get("db_file_id")
            sent_msg = None
            if db_file_id and DB_CHANNEL_ID:
                sent_msg = await bot.copy_message(chat_id=d.userId, from_chat_id=DB_CHANNEL_ID, message_id=db_file_id, caption=caption, parse_mode="HTML", protect_content=is_protected)
            else:
                if m.get("file_type") == "video": sent_msg = await bot.send_video(d.userId, m['file_id'], caption=caption, parse_mode="HTML", protect_content=is_protected)
                else: sent_msg = await bot.send_document(d.userId, m['file_id'], caption=caption, parse_mode="HTML", protect_content=is_protected)
            
            # ডাউনলোড কাউন্টার বাড়ানো
            await db.movies.update_many({"title": m["title"]}, {"$inc": {"downloads": 1}})
            await db.user_unlocks.update_one({"user_id": d.userId, "movie_id": d.movieId}, {"$set": {"unlocked_at": now}}, upsert=True)
            if sent_msg and not is_vip: await db.auto_delete.insert_one({"chat_id": d.userId, "message_id": sent_msg.message_id, "delete_at": now + datetime.timedelta(minutes=del_minutes)})
    except Exception: pass
    return {"ok": True}

@api_router.post("/api/request")
async def handle_request(data: ReqModel):
    if not validate_tg_data(data.initData): return {"ok": False}
    user = await db.users.find_one({"user_id": data.uid})
    is_vip = False
    if user and user.get("vip_until", datetime.datetime.utcnow()) > datetime.datetime.utcnow(): is_vip = True
    vip_tag = "🔥 <b>[VIP PRIORITY]</b>\n" if is_vip else ""
    now = datetime.datetime.utcnow()
    await db.requests.insert_one({"user_id": data.uid, "uname": data.uname, "movie": data.movie, "status": "pending", "created_at": now, "is_vip": is_vip})
    all_admins = set([OWNER_ID])
    async for a in db.admins.find(): all_admins.add(a["user_id"])
    for admin_id in all_admins:
        try: await bot.send_message(admin_id, f"{vip_tag}🔔 <b>নতুন মুভি রিকোয়েস্ট!</b>\n👤 ইউজার: {data.uname} (<code>{data.uid}</code>)\n🎬 মুভি: <b>{data.movie}</b>", parse_mode="HTML")
        except Exception: pass
    return {"ok": True}

# ==========================================
# 🛑 Watchlist & Review/Comment System APIs (ADMIN ANONYMITY + REPLIES)
# ==========================================
@api_router.post("/api/watchlist/add")
async def add_to_watchlist(d: WatchlistModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    await db.users.update_one({"user_id": d.uid}, {"$addToSet": {"watchlist": d.title}})
    return {"ok": True}

@api_router.post("/api/watchlist/remove")
async def remove_from_watchlist(d: WatchlistModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    await db.users.update_one({"user_id": d.uid}, {"$pull": {"watchlist": d.title}})
    return {"ok": True}

@api_router.get("/api/watchlist/list/{uid}")
async def get_watchlist(uid: int):
    user = await db.users.find_one({"user_id": uid})
    if not user: return {"watchlist": []}
    watchlist = user.get("watchlist", [])
    if not watchlist: return {"watchlist": []}
    pipeline = [{"$match": {"title": {"$in": watchlist}}}, {"$group": {"_id": "$title", "photo_id": {"$first": "$photo_id"}, "db_photo_id": {"$first": "$db_photo_id"}, "clicks": {"$sum": "$clicks"}, "likes": {"$first": "$likes"}, "downloads": {"$first": "$downloads"}, "created_at": {"$max": "$created_at"}, "files": {"$push": {"id": {"$toString": "$_id"}, "quality": {"$ifNull": ["$quality", "HD"]}}}}}, {"$sort": {"created_at": -1}}]
    movies = await db.movies.aggregate(pipeline).to_list(len(watchlist))
    formatted_movies = []
    for m in movies:
        p_id = m.get("photo_id") or (f"db_{m['db_photo_id']}" if m.get("db_photo_id") else None)
        formatted_movies.append({"title": m["_id"], "photo_id": p_id, "files": m["files"], "clicks": m.get("clicks", 0)})
    return {"watchlist": formatted_movies}

# 💬 কমেন্ট ও রিপ্লাই সাবমিট
@api_router.post("/api/reviews/add")
async def add_review(d: ReviewModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    now = datetime.datetime.utcnow()
    
    # অ্যাডমিন চেক: অ্যাডমিন হলে পরিচয় গোপন করে 'Admin' দেখাবে
    is_admin = (d.uid == OWNER_ID) or (d.uid in admin_cache)
    display_name = "Admin" if is_admin else (d.uname.strip() or "User")

    new_comment = {
        "user_id": d.uid,
        "uname": display_name,
        "is_admin": is_admin,
        "movie_title": d.title,
        "rating": d.rating if d.rating > 0 else 5,
        "review": d.review.strip(),
        "reply_to": d.reply_to.strip(),
        "likes": 0,
        "created_at": now
    }
    
    if d.review.strip():
        await db.reviews.insert_one(new_comment)
    elif d.rating > 0:
        await db.reviews.update_one(
            {"user_id": d.uid, "movie_title": d.title},
            {"$set": {"user_id": d.uid, "uname": display_name, "is_admin": is_admin, "movie_title": d.title, "rating": d.rating, "created_at": now}},
            upsert=True
        )
    return {"ok": True}

# 💬 কমেন্টে লাইক দেওয়া
@api_router.post("/api/comments/like")
async def like_comment(d: CommentLikeModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    try:
        await db.reviews.update_one({"_id": ObjectId(d.comment_id)}, {"$inc": {"likes": 1}})
        c = await db.reviews.find_one({"_id": ObjectId(d.comment_id)})
        return {"ok": True, "likes": c.get("likes", 1)}
    except Exception:
        return {"ok": False}

@api_router.get("/api/reviews/get/{title}")
async def get_reviews(title: str):
    reviews = await db.reviews.find({"movie_title": title, "review": {"$ne": ""}}).sort("created_at", -1).to_list(50)
    all_ratings = await db.reviews.find({"movie_title": title, "rating": {"$gt": 0}}).to_list(100)
    avg_r = sum(r["rating"] for r in all_ratings) / len(all_ratings) if all_ratings else 0
    
    now = datetime.datetime.utcnow()
    formatted = []
    for r in reviews:
        diff = now - r.get("created_at", now)
        if diff.days > 0: time_str = f"{diff.days} দিন আগে"
        elif diff.seconds // 3600 > 0: time_str = f"{diff.seconds // 3600} ঘণ্টা আগে"
        elif diff.seconds // 60 > 0: time_str = f"{diff.seconds // 60} মিনিট আগে"
        else: time_str = "এইমাত্র"
        
        formatted.append({
            "_id": str(r["_id"]),
            "uname": r.get("uname", "User"),
            "is_admin": r.get("is_admin", False),
            "review": r.get("review", ""),
            "reply_to": r.get("reply_to", ""),
            "rating": r.get("rating", 5),
            "likes": r.get("likes", 0),
            "time_ago": time_str
        })
        
    return {"reviews": formatted, "avg_rating": round(avg_r, 1), "total_ratings": len(all_ratings)}

# ==========================================
# 🛑 Gamification Daily Activity & Wheel
# ==========================================
@api_router.post("/api/gamification/daily_checkin")
async def daily_checkin(d: UserActionModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    user = await db.users.find_one({"user_id": d.uid})
    if not user: return {"ok": False, "msg": "User not found"}
    now = datetime.datetime.utcnow()
    last_c = user.get("last_check_in")
    if last_c and last_c.date() == now.date(): return {"ok": False, "msg": "Already checked in today!"}
    await db.users.update_one({"user_id": d.uid}, {"$set": {"last_check_in": now}, "$inc": {"coins": 5}})
    return {"ok": True, "coins": user.get("coins", 0) + 5}

@api_router.post("/api/gamification/spin")
async def spin_wheel(d: UserActionModel):
    if not validate_tg_data(d.initData): return {"ok": False}
    user = await db.users.find_one({"user_id": d.uid})
    
    if not user or user.get("coins", 0) < 5: 
        user_name = user.get("first_name", "User") if user else "User"
        return {
            "ok": False, 
            "msg": f"আরে {user_name}! 🥺 স্পিন করতে ৫ Gems প্রয়োজন। তোমার ব্যালেন্স কম আছে। বন্ধুদের ইনভাইট লিংক শেয়ার করে Gems বাড়িয়ে নাও! 😉✨"
        }
        
    rewards = [{"type": "points", "amount": 0, "weight": 35}, {"type": "points", "amount": 2, "weight": 25}, {"type": "points", "amount": 5, "weight": 20}, {"type": "points", "amount": 10, "weight": 12}, {"type": "points", "amount": 20, "weight": 5}, {"type": "points", "amount": 50, "weight": 2}, {"type": "vip", "days": 1, "weight": 1}]
    choices = []
    for r in rewards: choices.extend([r] * r["weight"])
    reward = random.choice(choices)
    await db.users.update_one({"user_id": d.uid}, {"$inc": {"coins": -5}})
    msg = ""
    if reward["type"] == "points":
        if reward["amount"] > 0:
            await db.users.update_one({"user_id": d.uid}, {"$inc": {"coins": reward["amount"]}})
            msg = f"You won {reward['amount']} Points!"
        else: msg = "Better luck next time!"
    elif reward["type"] == "vip":
        now = datetime.datetime.utcnow()
        cv = user.get("vip_until", now) if user.get("vip_until") else now
        if cv < now: cv = now
        await db.users.update_one({"user_id": d.uid}, {"$set": {"vip_until": cv + datetime.timedelta(days=1)}})
        msg = "Congratulations! You won 1 Day VIP Pass!"
    return {"ok": True, "reward": reward, "msg": msg}

@api_router.get("/api/gamification/leaderboard")
async def get_leaderboard():
    tops = await db.users.find().sort("refer_count", -1).limit(10).to_list(10)
    lead = []
    for u in tops: 
        lead.append({"name": u.get("first_name", "User"), "refer_count": u.get("refer_count", 0), "coins": u.get("coins", 0)})
    return {"leaderboard": lead}

@api_router.get("/api/requests/user_list/{uid}")
async def user_requests(uid: int):
    reqs = await db.requests.find({"user_id": uid}).sort("created_at", -1).to_list(50)
    for r in reqs:
        r["_id"] = str(r["_id"])
        r["created_at"] = r["created_at"].isoformat()
    return {"requests": reqs}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.utcnow().isoformat()}
