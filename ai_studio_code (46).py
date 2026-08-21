# html_template.py

HTML_CODE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Prime Flix</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
        body { background: #0b0f19; font-family: sans-serif; color: #fff; overflow-x: hidden; width: 100%; -webkit-overflow-scrolling: touch; padding-bottom: 80px; } 
        
        header { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 12px 10px; border-bottom: 1px solid #1e293b; position: sticky; top: 0; background: rgba(11, 15, 25, 0.95); backdrop-filter: blur(10px); z-index: 1000; width: 100%; gap: 8px; }
        .logo { font-size: 22px; font-weight: 900; white-space: nowrap; letter-spacing: 1px; }
        .logo span { background: #ef4444; color: #fff; padding: 2px 6px; border-radius: 4px; margin-left: 3px; font-size: 14px; }
        
        .home-btn { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.5); padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 11px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: 0.2s; white-space: nowrap; }
        .home-btn:active { transform: scale(0.95); background: rgba(59, 130, 246, 0.2); }

        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(11, 15, 25, 0.98); backdrop-filter: blur(15px); border-top: 1px solid #1e293b; display: flex; justify-content: space-around; align-items: center; padding: 10px 0; z-index: 2000; padding-bottom: calc(10px + env(safe-area-inset-bottom)); }
        .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #94a3b8; font-size: 11px; font-weight: bold; cursor: pointer; transition: 0.2s; width: 20%; gap: 4px; }
        .nav-item i { font-size: 20px; transition: transform 0.2s; }
        .nav-item.active { color: #38bdf8; }
        .nav-item.active i { transform: scale(1.15); }
        .nav-item:active { transform: scale(0.9); }
        
        .dropdown-menu { display: none; position: fixed; bottom: 85px; right: 15px; background: rgba(15, 23, 42, 0.98); backdrop-filter: blur(10px); border: 1px solid #334155; border-radius: 12px; overflow: hidden; box-shadow: 0 -5px 25px rgba(0,0,0,0.5); z-index: 2000; width: 250px; animation: slideUp 0.2s ease-out forwards; }
        @keyframes slideUp { 0% { opacity: 0; transform: translateY(15px); } 100% { opacity: 1; transform: translateY(0); } }
        
        .dropdown-menu a { display: flex; align-items: center; gap: 10px; padding: 12px 15px; color: white; text-decoration: none; font-weight: 600; font-size: 14px; cursor: pointer; transition: background 0.2s ease; border-bottom: 1px solid #334155; }
        .dropdown-menu a:hover, .dropdown-menu a:active { background: rgba(51, 65, 85, 0.5); }
        .dropdown-menu a i { font-size: 16px; width: 20px; text-align: center; }
        
        .coin-tag { background: #3b82f6; color: white; font-weight: 900; padding: 2px 8px; border-radius: 10px; margin-left: 2px; font-size: 12px; }
        .vip-tag { background: linear-gradient(45deg, #fbbf24, #f59e0b); color: #000; font-size: 12px; padding: 3px 8px; border-radius: 12px; font-weight: bold; display: none; margin-left:5px; }

        .search-box { padding: 15px; }
        .search-input { width: 100%; padding: 16px; border-radius: 25px; border: none; outline: none; text-align: center; background: #1e293b; color: #fff; font-size: 18px; font-weight: bold; }

        .category-container { display: flex; overflow-x: auto; flex-wrap: nowrap; gap: 12px; padding: 15px 15px 25px; scroll-behavior: smooth; width: 100%; }
        .category-container::-webkit-scrollbar { display: none; }
        
        .cat-btn { background: #e2e8f0; color: #0f172a; border: none; padding: 10px 22px; border-radius: 30px; font-size: 14px; font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; white-space: nowrap; transition: all 0.25s ease; animation: unselectedPulse 3s infinite ease-in-out; }
        .cat-btn i { font-size: 13px; color: #475569; }
        .cat-btn:active { transform: scale(0.95); }
        
        .cat-btn.active.active-latest { background: linear-gradient(135deg, #ff4e2a, #ff7300) !important; color: #ffffff !important; animation: activeLatestPulse 2s infinite ease-in-out !important; }
        .cat-btn.active.active-latest i { color: #ffffff !important; }
        .cat-btn.active.active-foryou { background: #ffffff !important; color: #7c3aed !important; animation: activeForYouPulse 2s infinite ease-in-out !important; }
        .cat-btn.active.active-foryou .sparkle-icon { color: #7c3aed !important; }
        .cat-btn.active { background: linear-gradient(135deg, #ff4e2a, #ff7300); color: #ffffff !important; animation: activeLatestPulse 2s infinite ease-in-out !important; }
        .cat-btn.active i { color: #ffffff !important; }

        .sparkle-icon { display: inline-block; font-size: 18px; font-family: serif; color: #7c3aed; animation: sparkleStar 2.2s ease-in-out infinite; line-height: 1; }

        .cat-btn i.fa-clock, .fa-clock-rotate-left { display: inline-block; animation: spinClock 6s linear infinite; }
        @keyframes spinClock { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes sparkleStar { 0%, 100% { transform: scale(1) rotate(0deg); } 50% { transform: scale(1.3) rotate(20deg); } }

        .fa-fire, .fa-fire-flame-curved { display: inline-block; animation: flickerFlame 0.8s ease-in-out infinite alternate; color: #ff4e2a !important; }
        @keyframes flickerFlame { 0% { transform: scale(1) rotate(-3deg); } 100% { transform: scale(1.18) rotate(4deg); } }

        @keyframes unselectedPulse { 0%, 100% { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15); transform: scale(1); } 50% { box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35); transform: scale(0.98); } }
        @keyframes activeLatestPulse { 0%, 100% { box-shadow: 0 0 8px 2px rgba(255, 78, 42, 0.4); transform: scale(1); } 50% { box-shadow: 0 0 25px 8px rgba(255, 78, 42, 0.85); transform: scale(1.03); } }
        @keyframes activeForYouPulse { 0%, 100% { box-shadow: 0 0 8px 2px rgba(124, 58, 237, 0.4); transform: scale(1); } 50% { box-shadow: 0 0 25px 8px rgba(124, 58, 237, 0.85); transform: scale(1.03); } }

        .section-title { padding: 5px 15px 15px; font-size: 20px; font-weight: 900; display: flex; align-items: center; gap: 8px; color:#ff416c; }
        
        .trending-container { display: flex; overflow-x: auto; gap: 15px; padding: 0 15px 20px; scroll-behavior: smooth; scroll-snap-type: x mandatory; }
        .trending-container::-webkit-scrollbar { display: none; }
        .trending-card { min-width: 280px; max-width: 280px; background: transparent; overflow: hidden; cursor: pointer; flex-shrink: 0; position: relative; transition: transform 0.2s; scroll-snap-align: start; }
        .trending-card:active { transform: scale(0.98); }

        .ad-carousel-container { width: 100%; margin: 5px 0 15px 0; display: flex; flex-direction: column; align-items: center; }
        .ad-carousel-track { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 12px; width: 100%; padding: 10px 0; scrollbar-width: none; }
        .ad-carousel-track::-webkit-scrollbar { display: none; }
        .ad-carousel-card { min-width: 250px; max-width: 250px; background: #ffffff; color: #1e293b; border-radius: 20px; overflow: hidden; display: flex; flex-direction: column; scroll-snap-align: start; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); flex-shrink: 0; text-decoration: none; }
        .ad-carousel-img-wrap { width: 100%; aspect-ratio: 16/10; background: #e2e8f0; overflow: hidden; }
        .ad-carousel-img-wrap img { width: 100%; height: 100%; object-fit: cover; }
        .ad-carousel-body { padding: 12px 15px 15px 15px; text-align: left; display: flex; flex-direction: column; align-items: flex-start; gap: 4px; background: #ffffff; }
        .ad-carousel-title { font-size: 16px; font-weight: 800; color: #0f172a; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; width: 100%; line-height: 1.2; }
        .ad-carousel-subtitle { font-size: 12px; color: #64748b; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; width: 100%; line-height: 1.4; margin-bottom: 8px; }
        .ad-carousel-btn { background: linear-gradient(135deg, #ff4e2a, #ff7300); color: #ffffff; font-size: 13px; font-weight: 800; padding: 6px 20px; border-radius: 20px; border: none; cursor: pointer; }

        .grid { padding: 0 15px 20px; display: flex; flex-direction: column; gap: 20px; }
        .card { background: transparent; overflow: hidden; cursor: pointer; transition: transform 0.2s; }
        .card:active { transform: scale(0.98); }
        
        .post-content { position: relative; padding: 3px; border-radius: 12px; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); background-size: 200%; }
        .post-content img { width: 100%; aspect-ratio: 16/9; height: auto; object-fit: cover; display: block; border-radius: 10px; }
        
        .card-footer { padding: 12px 5px 0; display: flex; align-items: flex-start; gap: 12px; text-align: left; }

        .channel-logo { width: 40px; height: 40px; border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden; box-shadow: 0 0 8px rgba(0,0,0,0.5); }
        .channel-logo::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(#ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); animation: spinRing 4s linear infinite; z-index: 1; }
        .channel-logo img { width: calc(100% - 4px); height: calc(100% - 4px); object-fit: cover; border-radius: 50%; position: relative; z-index: 2; background: #05070e; }
        
        .title-text { color: #f8fafc; font-size: 16px; font-weight: bold; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin-top: 2px; }

        .pagination { display: flex; justify-content: center; align-items: center; gap: 8px; padding: 10px 15px 30px; flex-wrap: wrap; }
        .page-btn { background: #1e293b; color: #fff; border: 1px solid #334155; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .page-btn:hover { background: #334155; }
        .page-btn.active { background: #f87171; border-color: #f87171; color: white; }

        .community-section { margin: 10px 15px 30px; padding: 15px; background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 16px; backdrop-filter: blur(10px); }
        .social-grid { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
        .social-btn { display: flex; align-items: center; gap: 8px; padding: 10px 15px; border-radius: 12px; font-weight: bold; font-size: 13px; text-decoration: none; flex-grow: 1; justify-content: center; min-width: 140px; }
        .fb-btn { background: rgba(24, 119, 242, 0.1); color: #1877f2; border: 1px solid rgba(24, 119, 242, 0.3); }
        .yt-btn { background: rgba(255, 0, 0, 0.1); color: #ff0000; border: 1px solid rgba(255, 0, 0, 0.3); }
        .tg-btn { background: rgba(36, 161, 222, 0.1); color: #24A1DE; border: 1px solid rgba(36, 161, 222, 0.3); }

        .developer-credit { margin: 10px 15px 130px; padding: 22px 15px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 16px; text-align: center; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); }
        .dev-title { font-size: 12px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }
        .dev-name { font-size: 22px; font-weight: 900; background: linear-gradient(45deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }
        .dev-desc { font-size: 13.5px; color: #cbd5e1; margin-bottom: 18px; line-height: 1.5; }
        .dev-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: linear-gradient(45deg, #0ea5e9, #2563eb); color: white; padding: 12px 24px; border-radius: 30px; font-size: 15px; font-weight: bold; border: none; cursor: pointer; }

        .floating-btn { position: fixed; right: 15px; color: white; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; z-index: 500; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .btn-18 { bottom: 205px; background: linear-gradient(45deg, #ff0000, #990000); font-weight: bold; font-size: 16px; border: 2px solid white; }
        .btn-tg { bottom: 145px; background: linear-gradient(45deg, #24A1DE, #1b7ba8); }
        .btn-req { bottom: 85px; background: linear-gradient(45deg, #10b981, #059669); }

        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: none; align-items: center; justify-content: center; z-index: 3000; backdrop-filter: blur(5px); }
        .modal-content { background: #1e293b; width: 92%; max-width: 400px; padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #334155; max-height: 85vh; overflow-y: auto; position: relative; }
        .close-icon { position: absolute; top: 12px; right: 15px; width: 32px; height: 32px; border-radius: 50%; background: #334155; color: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; }
        
        .rgb-border { position: relative; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); background-size: 200%; padding: 4px; border-radius: 14px; margin-bottom: 12px; cursor: pointer; width: 100%; }
        .rgb-inner { display: flex; justify-content: space-between; align-items: center; background: #0f172a; padding: 18px; border-radius: 10px; color: white; font-weight: 900; font-size: 17px; }

        .btn-submit { background: linear-gradient(45deg, #10b981, #059669); color: white; border: none; padding: 15px 20px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 18px; cursor: pointer; }

        .dl-rgb-wrap { position: relative; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); background-size: 200%; padding: 4px; border-radius: 16px; width: 100%; max-width: 350px; margin: auto; }
        .dl-inner-box { background: rgba(15, 23, 42, 0.98); border-radius: 12px; padding: 30px 20px; display: flex; flex-direction: column; align-items: center; gap: 15px; }
        
        .spinner-new { width: 65px; height: 65px; border: 5px solid rgba(255,255,255,0.1); border-left-color: #10b981; border-radius: 50%; animation: spin-fast 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin-fast { 100% { transform: rotate(360deg); } }
        .big-processing-text { font-size: 26px; font-weight: 900; color: #4ade80; }

        @keyframes spinRing { 0% { transform: rotate(0deg); filter: hue-rotate(0deg); } 100% { transform: rotate(360deg); filter: hue-rotate(360deg); } }
        @keyframes pulseGlow { from { text-shadow: 0 0 12px rgba(255, 0, 85, 0.5); } to { text-shadow: 0 0 25px rgba(255, 0, 85, 0.85); } }

        .top-badge, .ep-badge, .view-badge, .lang-card-badge { position: absolute; font-weight: bold; padding: 4px 8px; border-radius: 6px; font-size: 11px; z-index: 10; color: white; }
        .top-badge { top: 12px; left: 12px; background: linear-gradient(45deg, #ff0000, #cc0000); }
        .view-badge { bottom: 12px; left: 12px; background: rgba(0,0,0,0.75); }
        .ep-badge { bottom: 12px; right: 12px; background: #10b981; }

        .lang-card-badge { top: 12px; right: 12px; background: linear-gradient(135deg, #ef4444, #dc2626); color: #ffffff !important; font-size: 10px; font-weight: 900; padding: 4px 10px; text-transform: uppercase; }

        .top-badge-fire, .trending-fire-icon { display: inline-block; animation: flickerFlame 0.8s ease-in-out infinite alternate; }

        /* ========================================================== */
        /* 🎬 ULTRA-PREMIUM MOVIE DETAILS FULL SCREEN (EXACT REPLICA) */
        /* ========================================================== */
        #movieDetailScreen {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #080b12;
            z-index: 5000;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            padding-bottom: 90px;
        }

        .details-top-nav {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: rgba(8, 11, 18, 0.95);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
            gap: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .details-back-circle {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #192236;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }

        .details-nav-title {
            font-size: 18px;
            font-weight: 800;
            color: #f1f5f9;
        }

        .details-hero {
            position: relative;
            width: 100%;
            background: #000;
        }

        .details-hero img {
            width: 100%;
            aspect-ratio: 16/9;
            object-fit: cover;
            display: block;
        }

        .details-hd-tag {
            position: absolute;
            top: 12px;
            left: 12px;
            background: #eab308;
            color: #000;
            font-weight: 900;
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
        }

        .details-content-body {
            padding: 18px 16px;
        }

        .details-movie-title {
            font-size: 19px;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.4;
            margin-bottom: 20px;
        }

        /* 3-কাউন্টার স্ট্যাটাস বার */
        .stats-counter-bar {
            display: flex;
            align-items: center;
            justify-content: space-around;
            margin-bottom: 22px;
            padding: 0 10px;
        }

        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            gap: 4px;
        }

        .stat-item i {
            font-size: 22px;
        }

        .stat-item .stat-num {
            font-size: 16px;
            font-weight: 800;
            color: #f8fafc;
        }

        .stat-item .stat-lbl {
            font-size: 11px;
            color: #94a3b8;
            font-weight: 600;
        }

        .share-circle-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #182339;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #60a5fa;
            font-size: 18px;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.08);
        }

        /* ডাউনলোড গাইডলাইন নোটিস বার */
        .guide-notice-bar {
            background: #1e1b18;
            border: 1px solid #78350f;
            border-radius: 30px;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            color: #fbbf24;
            font-size: 13.5px;
            font-weight: bold;
            margin-bottom: 18px;
        }

        /* ৩টি প্রধান অ্যাকশন বাটন */
        .main-action-buttons {
            display: grid;
            grid-template-columns: 1fr 1.3fr 1fr;
            gap: 10px;
            margin-bottom: 18px;
        }

        .action-btn-pill {
            padding: 13px 5px;
            border-radius: 30px;
            font-weight: 800;
            font-size: 14.5px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.1);
            background: #161f30;
            color: #fff;
            transition: 0.2s;
        }

        .action-btn-pill.btn-download-main {
            background: #ffffff;
            color: #000000;
            font-weight: 900;
        }

        .action-btn-pill.liked {
            color: #ef4444;
            border-color: rgba(239, 68, 68, 0.4);
            background: rgba(239, 68, 68, 0.1);
        }

        .action-btn-pill.saved {
            color: #fbbf24;
            border-color: rgba(251, 191, 36, 0.4);
            background: rgba(251, 191, 36, 0.1);
        }

        /* রেটিং স্ট্রিপ */
        .rating-strip-box {
            background: #161b26;
            border: 1px solid #78350f;
            border-radius: 30px;
            padding: 10px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
        }

        .rating-stars-interactive {
            display: flex;
            gap: 6px;
            color: #475569;
            font-size: 18px;
            cursor: pointer;
        }

        .rating-stars-interactive i.active-star {
            color: #fbbf24;
        }

        .rating-score-display {
            color: #fbbf24;
            font-weight: 900;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* কমেন্টস সেকশন */
        .comments-section-wrap {
            margin-top: 10px;
        }

        .comments-header-title {
            font-size: 17px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 15px;
        }

        .comment-card-bubble {
            background: #111726;
            border-radius: 14px;
            padding: 14px;
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.04);
        }

        .comment-avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            object-fit: cover;
            flex-shrink: 0;
            background: #1e293b;
        }

        .comment-body-right {
            flex-grow: 1;
        }

        .comment-author-name {
            font-size: 14px;
            font-weight: 800;
            color: #ffffff;
        }

        .comment-time-ago {
            font-size: 11px;
            color: #94a3b8;
            margin-left: 6px;
            font-weight: normal;
        }

        .comment-text-msg {
            font-size: 13.5px;
            color: #cbd5e1;
            line-height: 1.5;
            margin-top: 4px;
            margin-bottom: 8px;
        }

        .comment-reply-bar {
            display: flex;
            align-items: center;
            gap: 14px;
            font-size: 12px;
            color: #94a3b8;
            font-weight: 700;
        }

        /* ফিক্সড কমেন্ট ইনপুট বক্স নিচে */
        .comment-input-bottom-dock {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #080b12;
            padding: 10px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-top: 1px solid #1e293b;
            z-index: 5500;
        }

        .comment-field-input {
            flex-grow: 1;
            background: #161f30;
            border: 1px solid #334155;
            padding: 12px 18px;
            border-radius: 25px;
            color: #fff;
            outline: none;
            font-size: 14px;
        }

        .comment-send-submit-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: #ffffff;
            color: #000;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            cursor: pointer;
            flex-shrink: 0;
        }

        /* কোয়ালিটি ড্রয়ার মডাল */
        #qualityDrawerModal {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 6000;
            display: none;
            align-items: flex-end;
            backdrop-filter: blur(5px);
        }

        .drawer-box {
            width: 100%;
            background: #111726;
            border-top: 2px solid #38bdf8;
            border-radius: 25px 25px 0 0;
            padding: 22px 18px 30px;
            max-height: 75vh;
            overflow-y: auto;
            animation: slideDrawer 0.25s ease-out;
        }
        @keyframes slideDrawer { from { transform: translateY(100%); } to { transform: translateY(0); } }
    </style>
</head>
<body onclick="closeMenu(event)">

    <!-- ======================== -->
    <!-- 🏠 HOME PAGE (MAIN VIEW) -->
    <!-- ======================== -->
    <div id="homePageMain">
        <header>
            <div class="logo"><span>𝑷𝑹𝑰𝑴𝑬 𝑪𝑰𝑵𝑬𝑭𝑳𝑰𝑿</span></div>
            <button onclick="goHome()" class="home-btn"><i class="fa-solid fa-house"></i> Home Page</button>
        </header>
        
        <div id="dropdownMenu" class="dropdown-menu">
            <div style="padding: 12px 15px; border-bottom: 1px solid #334155; display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: #3b82f6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; flex-shrink: 0;">
                    <i class="fa-solid fa-user"></i>
                </div>
                <div style="flex-grow: 1; text-align: left;">
                    <div style="font-size: 15px; font-weight: bold; color: white; line-height: 1.2;" id="menuUname">Guest</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 2px;" id="menuStatus">Free User</div>
                </div>
                <div style="text-align: right;">
                    <div id="coinDisplay" class="coin-tag" style="display:inline-block; margin-bottom:4px;"><i class="fa-solid fa-gem"></i> 0</div>
                    <div id="vipBadge" class="vip-tag" style="display:inline-block;">VIP</div>
                </div>
            </div>
            
            <a onclick="openReferModal()"><i class="fa-solid fa-share-nodes text-blue-400"></i> Refer & Earn</a>
            <a onclick="openRequestsTrackerModal()"><i class="fa-solid fa-code-pull-request text-green-400"></i> Request Movie & Track</a>
            <a onclick="openWatchlistModal()"><i class="fa-solid fa-bookmark text-red-400"></i> My Watchlist</a>
            <a onclick="openAdCampModal()"><i class="fa-solid fa-bullhorn text-yellow-400"></i> Promote Channel/Web</a>
            <div style="height: 1px; background: #334155; margin: 4px 0;"></div>
            <a onclick="tg.showAlert(`How to Download:\n1. Click Download button.\n2. Wait ${AD_WAIT_TIME} seconds on the link.\n3. Return to mini-app and movie is sent to your Telegram inbox!`)"><i class="fa-solid fa-circle-question text-red-400"></i> How to Download</a>
            <a onclick="window.open('{{TG_LINK}}')"><i class="fa-solid fa-bullhorn text-green-400"></i> Our Channel</a>
            <a onclick="window.open('{{SUPPORT_LINK}}')"><i class="fa-brands fa-telegram text-blue-400"></i> Support / Contact</a>
            <a onclick="window.open(window.location.origin + '/admin', '_blank')" id="adminMenuBtn" style="display: none; color: #ef4444;"><i class="fa-solid fa-screwdriver-wrench"></i> Admin Panel</a>
        </div>

        <div class="search-box">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search Movies or Series...">
        </div>

        <div id="categoryBox" class="category-container"></div>

        <div id="trendingWrapper">
            <div class="section-title"><span class="trending-fire-icon">🔥</span> Trending now</div>
            <div class="trending-container" id="trendingGrid"></div>
        </div>

        <div class="section-title" id="recentTitle"><i class="fa-solid fa-clock-rotate-left text-blue-400"></i> Recently Added</div>
        <div class="grid" id="movieGrid"></div>
        <div class="pagination" id="paginationBox"></div>
        
        <div id="communityBox"></div>

        <div class="developer-credit">
            <div class="dev-title"><i class="fa-solid fa-laptop-code"></i> Developer & Deployed By</div>
            <div class="dev-name">Bot Developer</div>
            <div class="dev-desc">Do you want to create a high-quality premium movie bot for your channel or group? Contact us today.</div>
            <button class="dev-btn" onclick="window.open('https://t.me/Prime_Admin_Support_ProBot', '_blank')">
                <i class="fa-brands fa-telegram"></i> Contact Developer
            </button>
        </div>

        <div class="floating-btn btn-18" onclick="window.open('{{LINK_18}}')">18+</div>
        <div class="floating-btn btn-tg" onclick="window.open('{{TG_LINK}}')"><i class="fa-brands fa-telegram"></i></div>
        <div class="floating-btn btn-req" onclick="openRequestsTrackerModal()"><i class="fa-solid fa-code-pull-request"></i></div>

        <div class="bottom-nav">
            <div class="nav-item active" id="navHome" onclick="goHome()">
                <i class="fa-solid fa-house"></i>
                <span>Home</span>
            </div>
            <div class="nav-item" id="navSearch" onclick="focusSearch()">
                <i class="fa-solid fa-magnifying-glass"></i>
                <span>Search</span>
            </div>
            <div class="nav-item" id="navUpcoming" onclick="window.location.href='/upcoming'">
                <i class="fa-solid fa-calendar-days"></i>
                <span>Upcoming</span>
            </div>
            <div class="nav-item" id="navVip" onclick="openVipModal()">
                <i class="fa-solid fa-gem"></i>
                <span>Premium</span>
            </div>
            <div class="nav-item" id="navProfile" onclick="toggleMenu(event)">
                <i class="fa-solid fa-user"></i>
                <span>Profile</span>
            </div>
        </div>
    </div>

    <!-- ========================================================== -->
    <!-- 🎬 ULTRA-PREMIUM MOVIE DETAILS FULL SCREEN (EXACT REPLICA) -->
    <!-- ========================================================== -->
    <div id="movieDetailScreen">
        <div class="details-top-nav">
            <div class="details-back-circle" onclick="closeMovieDetailScreen()">
                <i class="fa-solid fa-chevron-left"></i>
            </div>
            <div class="details-nav-title">ভিডিও ডিটেইলস</div>
        </div>

        <div class="details-hero">
            <span class="details-hd-tag">HD</span>
            <img id="detailHeroImg" src="" alt="Thumbnail">
        </div>

        <div class="details-content-body">
            <h1 class="details-movie-title" id="detailMovieTitle">Movie Title</h1>

            <div class="stats-counter-bar">
                <div class="stat-item" onclick="toggleLikeFromDetails()">
                    <i class="fa-solid fa-heart" id="statHeartIcon" style="color: #ef4444;"></i>
                    <span class="stat-num" id="detailLikesCount">0</span>
                    <span class="stat-lbl">Like</span>
                </div>
                <div class="stat-item" onclick="openDownloadDrawer()">
                    <i class="fa-solid fa-circle-down" style="color: #38bdf8;"></i>
                    <span class="stat-num" id="detailDownloadsCount">0</span>
                    <span class="stat-lbl">Download</span>
                </div>
                <div class="stat-item" onclick="document.getElementById('detailCommentInput').focus()">
                    <i class="fa-solid fa-comment-dots" style="color: #f8fafc;"></i>
                    <span class="stat-num" id="detailCommentsCount">0</span>
                    <span class="stat-lbl">Comments</span>
                </div>
                <div class="share-circle-btn" onclick="shareMovieDeepLink()">
                    <i class="fa-solid fa-share-nodes"></i>
                </div>
            </div>

            <div class="guide-notice-bar" onclick="openDownloadDrawer()">
                💡 নিচের বাটনে ক্লিক করে সহজেই Download করুন
            </div>

            <div class="main-action-buttons">
                <button class="action-btn-pill" id="detailLikePillBtn" onclick="toggleLikeFromDetails()">
                    <i class="fa-solid fa-heart"></i> Like
                </button>
                <button class="action-btn-pill btn-download-main" onclick="openDownloadDrawer()">
                    <i class="fa-solid fa-download"></i> Download
                </button>
                <button class="action-btn-pill" id="detailSavePillBtn" onclick="toggleWatchlistFromDetails()">
                    <i class="fa-solid fa-bookmark"></i> Save
                </button>
            </div>

            <div class="rating-strip-box">
                <span style="font-size: 13.5px; font-weight: 700; color: #cbd5e1;">রেটিং দিন:</span>
                <div class="rating-stars-interactive" id="detailInteractiveStars">
                    <i class="fa-solid fa-star" onclick="rateMovie(1)"></i>
                    <i class="fa-solid fa-star" onclick="rateMovie(2)"></i>
                    <i class="fa-solid fa-star" onclick="rateMovie(3)"></i>
                    <i class="fa-solid fa-star" onclick="rateMovie(4)"></i>
                    <i class="fa-solid fa-star" onclick="rateMovie(5)"></i>
                </div>
                <div class="rating-score-display">
                    <i class="fa-solid fa-star"></i> <span id="detailRatingAvg">0.0</span> (<span id="detailRatingCount">0</span>)
                </div>
            </div>

            <div class="comments-section-wrap">
                <div class="comments-header-title">Comments ( <span id="detailCommentsCountHeader">0</span> )</div>
                <div id="detailCommentsList"></div>
            </div>
        </div>

        <div class="comment-input-bottom-dock">
            <input type="text" id="detailCommentInput" class="comment-field-input" placeholder="Add a public comment...">
            <button class="comment-send-submit-btn" onclick="postDetailComment()">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>
    </div>

    <!-- ========================================================== -->
    <!-- 📦 QUALITY / EPISODE SELECTION DRAWER -->
    <!-- ========================================================== -->
    <div id="qualityDrawerModal" onclick="closeDownloadDrawer(event)">
        <div class="drawer-box" onclick="event.stopPropagation()">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                <h3 style="color:#38bdf8; font-size:18px; font-weight:800;"><i class="fa-solid fa-download"></i> Select Quality & Episode</h3>
                <div onclick="closeDownloadDrawer()" style="color:#94a3b8; font-size:20px; cursor:pointer;"><i class="fa-solid fa-xmark"></i></div>
            </div>
            <div id="drawerQualityList" style="display: flex; flex-direction: column; gap: 8px;"></div>
        </div>
    </div>

    <!-- ========================================================== -->
    <!-- 🔗 UNLOCK / DIRECT LINK WAITING MODAL -->
    <!-- ========================================================== -->
    <div id="directLinkModal" class="modal">
        <div class="modal-content" style="background: transparent; border: none; padding: 0;">
            <div class="close-icon" onclick="document.getElementById('directLinkModal').style.display='none'" style="top: -15px; right: 5px; z-index: 1000;"><i class="fa-solid fa-xmark"></i></div>
            <div class="dl-rgb-wrap">
                <div class="dl-inner-box">
                    <h2 style="color: #4ade80; font-size: 24px; font-weight: 900;"><i class="fa-solid fa-unlock-keyhole"></i> Unlock Video</h2>
                    <p id="dlDescText" style="color: #cbd5e1; font-size: 15px; font-weight: 600; text-align:center;">
                        To unlock this file, wait <b>{{AD_TIME}} seconds</b> on the link below.
                    </p>
                    <button id="dlClickBtn" class="btn-submit" style="background: linear-gradient(45deg, #ef4444, #f97316); margin-top: 10px;" onclick="executeDirectLink()">🔗 Click Here (Open Link)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- VIP / SPIN / REFERRAL MODALS -->
    <div id="vipModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('vipModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <div style="display: flex; gap: 5px; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 8px;">
                <button class="cat-btn active" id="btnTabVip" onclick="switchVipModalTab('vip')">💎 VIP & Buy</button>
                <button class="cat-btn" id="btnTabSpin" onclick="switchVipModalTab('spin')">🎡 Lucky Spin</button>
                <button class="cat-btn" id="btnTabLeader" onclick="switchVipModalTab('leader')">🏆 Leaders</button>
            </div>
            <div id="modalTabVipContent">
                <h2 style="color:#fbbf24; font-size: 22px; margin-bottom:12px;"><i class="fa-solid fa-gem"></i> Premium & Points</h2>
                <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #3b82f6; padding: 12px; border-radius: 12px; margin-bottom: 15px;">
                    <p style="color:#94a3b8; font-size: 13px; font-weight:bold;">Your Current Points:</p>
                    <h1 style="color:#38bdf8; font-size: 30px; font-weight:900; margin: 3px 0;"><span id="modalCoinText">0</span> <i class="fa-solid fa-gem"></i></h1>
                    <p style="color:#cbd5e1; font-size: 11px;">(<span id="vipDaysText">1</span> Days VIP = <span id="vipCostText">30</span> Points)</p>
                </div>
                <button id="dailyCheckinBtn" class="btn-submit" style="background: linear-gradient(45deg, #10b981, #3b82f6); margin-bottom: 12px;" onclick="claimDailyCheckin()">
                    📅 Daily Check-in (+5 Points)
                </button>
                <button class="btn-submit" style="background: linear-gradient(45deg, #3b82f6, #2563eb); margin-bottom: 12px;" onclick="window.open('{{SUPPORT_LINK}}')">
                    <i class="fa-brands fa-telegram"></i> Buy Points from Admin
                </button>
                <button id="coinAdBtn" class="btn-submit" style="background: linear-gradient(45deg, #ef4444, #f97316); margin-bottom: 12px;" onclick="executeCoinAd()">
                    <i class="fa-solid fa-play"></i> Watch Ad & Get 5 Points
                </button>
                <button class="btn-submit" style="background: linear-gradient(45deg, #10b981, #059669);" onclick="buyVipWithCoins()">
                    <i class="fa-solid fa-crown"></i> Get <span id="btnVipDays">1</span> Days VIP for <span id="btnVipCost">30</span> Points
                </button>
            </div>
            <div id="modalTabSpinContent" style="display: none;">
                <h2 style="color:#f59e0b; font-size: 22px; margin-bottom:10px;"><i class="fa-solid fa-circle-notch"></i> Lucky Spin Wheel</h2>
                <div style="position: relative; width: 180px; height: 180px; margin: 15px auto; border: 6px solid #334155; border-radius: 50%; overflow: hidden; background: #0f172a;" id="wheelOuter">
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 45px; height: 45px; background: white; border-radius: 50%; border: 4px solid #334155; z-index: 10; display:flex; align-items:center; justify-content:center; color:#0f172a; font-size:18px;"><i class="fa-solid fa-arrow-up"></i></div>
                    <div id="wheelInner" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; background: conic-gradient(#ef4444 0deg 60deg, #3b82f6 60deg 120deg, #10b981 120deg 180deg, #f59e0b 180deg 240deg, #8b5cf6 240deg 300deg, #ec4899 300deg 360deg); transition: transform 4s cubic-bezier(0.25, 0.1, 0.25, 1);"></div>
                </div>
                <button id="spinBtn" class="btn-submit" style="background: linear-gradient(45deg, #f59e0b, #ef4444);" onclick="spinWheel()">🎡 Spin (Cost: 5 Points)</button>
            </div>
            <div id="modalTabLeaderContent" style="display: none;">
                <h2 style="color:#60a5fa; font-size: 22px; margin-bottom:12px;"><i class="fa-solid fa-trophy"></i> Referrers Leaderboard</h2>
                <div id="leaderboardList" style="text-align: left; display: flex; flex-direction: column; gap: 8px; max-height: 250px; overflow-y: auto;"></div>
            </div>
        </div>
    </div>

    <div id="referModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('referModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <i class="fa-solid fa-share-nodes" style="font-size:60px; color:#38bdf8;"></i>
            <h2 style="margin:15px 0; color:white; font-size: 24px;">Refer & Earn</h2>
            <div style="background:#0f172a; padding:15px; border:1px dashed #3b82f6; margin-bottom:15px; word-break:break-all;" id="refLinkText">...</div>
            <button class="btn-submit" onclick="copyReferLink()">Copy Link</button>
        </div>
    </div>
    
    <div id="watchlistModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('watchlistModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:#38bdf8; font-size: 22px; margin-bottom:15px;"><i class="fa-solid fa-bookmark"></i> My Watchlist</h2>
            <div id="watchlistModalList" class="grid" style="padding:0; max-height: 60vh; overflow-y:auto; gap: 15px;"></div>
        </div>
    </div>

    <div id="requestsTrackerModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('requestsTrackerModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:#10b981; font-size: 22px; margin-bottom:10px;"><i class="fa-solid fa-code-pull-request"></i> Movie Request Status</h2>
            <div style="display:flex; gap:10px; margin-bottom: 20px;">
                <input type="text" id="reqTrackerInput" class="search-input" style="border-radius:12px; text-align:left; padding:10px 15px; font-size:15px;" placeholder="Enter Movie/Series name...">
                <button class="btn-submit" style="width: auto; padding:0 20px; font-size:14px;" onclick="submitReqTracker()">Request</button>
            </div>
            <div id="requestsTrackerList" style="text-align: left; display: flex; flex-direction: column; gap: 12px; max-height: 45vh; overflow-y: auto;"></div>
        </div>
    </div>

    <div id="adCampModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('adCampModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:#fcd34d; font-size: 22px; margin-bottom:10px;"><i class="fa-solid fa-bullhorn"></i> Promote Channel</h2>
            <input type="text" id="campTitle" class="search-input" style="border-radius:10px; margin-bottom:10px; font-size:15px;" placeholder="Ad Title">
            <input type="text" id="campSubtitle" class="search-input" style="border-radius:10px; margin-bottom:10px; font-size:15px;" placeholder="Ad Subtitle">
            <input type="url" id="campLink" class="search-input" style="border-radius:10px; margin-bottom:10px; font-size:15px;" placeholder="https://t.me/yourlink">
            <input type="url" id="campImg" class="search-input" style="border-radius:10px; margin-bottom:15px; font-size:15px;" placeholder="Image URL (Optional)">
            <select id="campPackage" class="search-input" style="border-radius:10px; margin-bottom:15px; font-size:15px; background:#1e293b; color:white;">
                <option value="1">1 Day - 500 Points</option>
                <option value="3">3 Days - 1200 Points</option>
                <option value="7">7 Days - 2500 Points</option>
            </select>
            <button class="btn-submit" style="background: linear-gradient(45deg, #f59e0b, #d97706);" onclick="submitAdCampaign()">Pay & Start</button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp; tg.expand();
        const DIRECT_LINKS = {{DIRECT_LINKS}};
        const SOCIAL_LINKS = {{SOCIAL_LINKS}};
        const INIT_DATA = tg.initData || "";
        const BOT_UNAME = "{{BOT_USER}}";
        const AD_WAIT_TIME = {{AD_TIME}}; 
        const AD_INTERVAL = {{AD_INTERVAL}}; 
        
        let uid = tg.initDataUnsafe?.user?.id || 0;
        let isUserVip = false;
        let userCoins = 0;
        let loadedMovies = {}; 
        let currentPage = 1; 
        let searchQuery = "";
        let activeCategory = "";
        let autoScrollInterval;
        let activeAds = [];
        
        let currentOpenMovie = null;
        let isCurrentLiked = false;
        let isCurrentSaved = false;

        function setNavActive(index) {
            const items = document.querySelectorAll('.nav-item');
            items.forEach((item, i) => {
                if(i === index) item.classList.add('active');
                else item.classList.remove('active');
            });
        }

        async function fetchUserInfo() {
            try {
                const res = await fetch('/api/user/' + uid);
                const data = await res.json();
                isUserVip = data.vip;
                userCoins = data.coins || 0;
                
                document.getElementById('vipDaysText').innerText = data.vip_days || 1;
                document.getElementById('vipCostText').innerText = data.vip_cost || 30;
                document.getElementById('btnVipDays').innerText = data.vip_days || 1;
                document.getElementById('btnVipCost').innerText = data.vip_cost || 30;

                let firstName = tg.initDataUnsafe?.user?.first_name || 'Guest';
                document.getElementById('menuUname').innerText = firstName;
                
                document.getElementById('coinDisplay').innerHTML = `<i class="fa-solid fa-gem"></i> ${userCoins}`;
                document.getElementById('modalCoinText').innerText = userCoins;
                
                if(isUserVip) {
                    document.getElementById('vipBadge').style.display = 'inline-block';
                    document.getElementById('menuStatus').innerText = '👑 VIP User';
                    document.getElementById('menuStatus').style.color = '#fbbf24';
                } else {
                    document.getElementById('vipBadge').style.display = 'none';
                    document.getElementById('menuStatus').innerText = 'Free User';
                    document.getElementById('menuStatus').style.color = '#94a3b8';
                }
                
                if(data.admin) document.getElementById('adminMenuBtn').style.display = 'flex';
                document.getElementById('refLinkText').innerText = `https://t.me/${BOT_UNAME}?start=ref_${uid}`;
            } catch(e) {}
        }

        async function fetchActiveAds() {
            try {
                const res = await fetch('/api/ads/active');
                activeAds = await res.json();
            } catch(e) {}
        }

        function getAdCarouselHTML(indexId) {
            if(activeAds.length === 0) return '';
            let sliderId = "slider_" + indexId;
            let adCards = activeAds.map(ad => {
                let imgHtml = ad.image_url ? `<img src="${ad.image_url}" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">` : `<div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#cbd5e1;"><i class="fa-solid fa-bullhorn text-slate-400" style="font-size:40px;"></i></div>`;
                return `
                <div class="ad-carousel-card" onclick="window.open('${ad.link}', '_blank')">
                    <div class="ad-carousel-img-wrap">${imgHtml}</div>
                    <div class="ad-carousel-body">
                        <div class="ad-carousel-title">${ad.title}</div>
                        <div class="ad-carousel-subtitle">${ad.subtitle || "দেরি না করে এখনো সবাই নিয়ে নিন"}</div>
                        <button class="ad-carousel-btn">Click Now</button>
                    </div>
                </div>`;
            }).join('');

            return `
            <div class="ad-carousel-container">
                <div class="ad-carousel-track" id="track_${sliderId}">${adCards}</div>
            </div>`;
        }

        function toggleMenu(e) { 
            e.stopPropagation(); 
            setNavActive(4);
            const m = document.getElementById('dropdownMenu'); 
            m.style.display = m.style.display === 'block' ? 'none' : 'block'; 
        }
        function closeMenu() { document.getElementById('dropdownMenu').style.display = 'none'; }
        
        function goHome() { 
            setNavActive(0);
            closeMovieDetailScreen();
            document.getElementById('searchInput').value = ""; 
            searchQuery = ""; 
            activeCategory = "";
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            let firstCatBtn = document.querySelector('.cat-btn');
            if(firstCatBtn) firstCatBtn.classList.add('active');
            
            document.getElementById('trendingWrapper').style.display = 'block';
            loadTrending();
            loadMovies(1); 
            closeMenu(); 
            window.scrollTo({ top: 0, behavior: 'smooth' }); 
        }
        
        function focusSearch() {
            setNavActive(1);
            closeMenu();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => document.getElementById('searchInput').focus(), 300);
        }
        
        function openVipModal() { 
            setNavActive(3);
            switchVipModalTab('vip');
            document.getElementById('vipModal').style.display = 'flex'; 
            closeMenu(); 
        }

        function switchVipModalTab(tab) {
            document.getElementById('modalTabVipContent').style.display = tab === 'vip' ? 'block' : 'none';
            document.getElementById('modalTabSpinContent').style.display = tab === 'spin' ? 'block' : 'none';
            document.getElementById('modalTabLeaderContent').style.display = tab === 'leader' ? 'block' : 'none';
            document.getElementById('btnTabVip').className = tab === 'vip' ? 'cat-btn active' : 'cat-btn';
            document.getElementById('btnTabSpin').className = tab === 'spin' ? 'cat-btn active' : 'cat-btn';
            document.getElementById('btnTabLeader').className = tab === 'leader' ? 'cat-btn active' : 'cat-btn';
            if (tab === 'leader') renderLeaderboard();
        }

        function openReferModal() { document.getElementById('referModal').style.display = 'flex'; closeMenu(); }
        function copyReferLink() { navigator.clipboard.writeText(document.getElementById('refLinkText').innerText); tg.showAlert("✅ Copied!"); }
        function openWatchlistModal() { document.getElementById('watchlistModal').style.display = 'flex'; closeMenu(); renderWatchlist(); }

        async function renderWatchlist() {
            try {
                const res = await fetch(`/api/watchlist/list/${uid}`);
                const data = await res.json();
                let html = '';
                if (!data.watchlist || data.watchlist.length === 0) {
                    html = '<p style="color: #cbd5e1; text-align:center; padding: 20px;">Your Watchlist is empty!</p>';
                } else {
                    data.watchlist.forEach(m => {
                        loadedMovies[m.title] = { _id: m.title, photo_id: m.photo_id, files: m.files, clicks: m.clicks || 0 };
                        html += `
                        <div class="card" onclick="openMovieDetailsPage('${encodeURIComponent(m.title)}')">
                            <div class="post-content">
                                <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                                <div class="ep-badge"><i class="fa-solid fa-bookmark text-yellow-400"></i> Saved</div>
                            </div>
                            <div class="card-footer">
                                <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg" alt="Logo"></div>
                                <div class="title-text">${m.title}</div>
                            </div>
                        </div>`;
                    });
                }
                document.getElementById('watchlistModalList').innerHTML = html;
            } catch(e) {}
        }

        function formatViews(n) { if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'; if (n >= 1000) return (n / 1000).toFixed(1) + 'K'; return n; }
        function makeSafeId(str) { return str.replace(/[^a-zA-Z0-9]/g, '_'); }

        async function loadCategories() {
            try {
                const res = await fetch('/api/categories');
                const cats = await res.json();
                if(cats.length === 0) return;
                
                let html = '';
                cats.forEach((c, idx) => {
                    let catQuery = c.name === "Latest" ? "" : c.name.replace(/'/g, "\\'");
                    let btnClass = "cat-btn" + (idx === 0 ? " active active-latest" : "");
                    let iconHtml = c.name === "For You" ? `<span class="sparkle-icon">✦</span>` : `<i class="${c.icon || 'fa-solid fa-film'}"></i>`;
                    html += `<button class="${btnClass}" onclick="setCategory('${catQuery}', this, '${c.name}')"><span style="display:flex; align-items:center; gap:8px;">${iconHtml} ${c.name}</span></button>`;
                });
                document.getElementById('categoryBox').innerHTML = html;
            } catch(e) {}
        }

        function setCategory(cat, btn, catName) {
            activeCategory = cat;
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active', 'active-latest', 'active-foryou'));
            if (catName === "Latest") btn.classList.add('active', 'active-latest');
            else if (catName === "For You") btn.classList.add('active', 'active-foryou');
            else btn.classList.add('active');
            
            let titleEl = document.getElementById('recentTitle');
            if (cat === "") titleEl.innerHTML = `<i class="fa-solid fa-clock text-blue-400"></i> Discover Latest Blockbusters`;
            else if (catName === "For You") titleEl.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles text-purple-400"></i> Handpicked For You`;
            else if (catName === "Trending") titleEl.innerHTML = `<i class="fa-solid fa-fire text-orange-500"></i> Trending Worldwide`;
            else titleEl.innerHTML = `<i class="fa-solid fa-film text-red-500"></i> Explored ${catName} Collection`;

            searchQuery = ""; 
            document.getElementById('searchInput').value = "";
            document.getElementById('trendingWrapper').style.display = cat === "" ? 'block' : 'none';
            loadMovies(1);
        }

        function startAutoScroll() {
            if(autoScrollInterval) clearInterval(autoScrollInterval);
            autoScrollInterval = setInterval(() => {
                let grid = document.getElementById('trendingGrid');
                if(grid) {
                    if (grid.scrollLeft >= (grid.scrollWidth - grid.clientWidth - 10)) grid.scrollTo({ left: 0, behavior: 'smooth' });
                    else grid.scrollBy({ left: 295, behavior: 'smooth' });
                }
            }, 3000);
        }

        async function loadTrending() {
            try {
                const r = await fetch(`/api/trending?uid=${uid}`);
                const data = await r.json();
                const grid = document.getElementById('trendingGrid');
                if(data.length === 0) return document.getElementById('trendingWrapper').style.display = 'none';
                grid.innerHTML = data.map(m => {
                    loadedMovies[m._id] = m;
                    return `<div class="trending-card" onclick="openMovieDetailsPage('${encodeURIComponent(m._id)}')">
                        <div class="post-content">
                            <div class="top-badge"><span class="top-badge-fire">🔥</span> TOP</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                            <div class="ep-badge"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="view-badge" id="trend-view-${makeSafeId(m._id)}"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg" alt="Logo"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                }).join('');
                setTimeout(startAutoScroll, 1000);
            } catch(e) {}
        }

        async function loadMovies(page = 1) {
            currentPage = page;
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = "<p style='color:white; text-align:center;'>Loading...</p>";
            try {
                const r = await fetch(`/api/list?page=${currentPage}&q=${encodeURIComponent(searchQuery)}&uid=${uid}&cat=${encodeURIComponent(activeCategory)}`);
                const data = await r.json();
                if(data.movies.length === 0) return grid.innerHTML = `<p style='text-align:center; color:#fbbf24;'>No movies found!</p>`;
                
                let htmlContent = "";
                data.movies.forEach((m, index) => {
                    loadedMovies[m._id] = m; 
                    let langBadge = m.badge ? m.badge : detectLanguage(m._id);
                    
                    htmlContent += `<div class="card" onclick="openMovieDetailsPage('${encodeURIComponent(m._id)}')">
                        <div class="post-content">
                            <div class="lang-card-badge">${langBadge}</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                            <div class="ep-badge"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="view-badge" id="list-view-${makeSafeId(m._id)}"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg" alt="Logo"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                    
                    let visualIndex = index + 1;
                    if (activeAds.length > 0 && visualIndex % AD_INTERVAL === 0) {
                        htmlContent += getAdCarouselHTML(visualIndex);
                    }
                });
                
                grid.innerHTML = htmlContent;
                
                let html = "";
                if(data.total_pages > 1) {
                    html += `<button class="page-btn" ${currentPage === 1 ? 'disabled style="opacity:0.5;"' : 'onclick="loadMovies(' + (currentPage - 1) + ')"'}>Prev</button>`;
                    html += `<span class="page-info" style="font-weight:bold; font-size:14px; color:#cbd5e1; margin: 0 10px;">Page ${currentPage} of ${data.total_pages}</span>`;
                    html += `<button class="page-btn" ${currentPage === data.total_pages ? 'disabled style="opacity:0.5;"' : 'onclick="loadMovies(' + (currentPage + 1) + ')"'}>Next</button>`;
                }
                document.getElementById('paginationBox').innerHTML = html;
            } catch(e) {}
        }

        let timeout = null;
        document.getElementById('searchInput').addEventListener('input', function(e) {
            clearTimeout(timeout); 
            searchQuery = e.target.value.trim();
            const elementsToToggle = [
                document.getElementById('categoryBox'),
                document.getElementById('trendingWrapper'),
                document.getElementById('recentTitle'),
                document.getElementById('communityBox'),
                document.querySelector('.developer-credit')
            ];

            if(searchQuery !== "") { 
                elementsToToggle.forEach(el => { if(el) el.style.display = 'none'; });
                activeCategory = ""; 
                document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active')); 
            } else { 
                if(document.getElementById('categoryBox')) document.getElementById('categoryBox').style.display = 'flex';
                if(document.getElementById('trendingWrapper')) document.getElementById('trendingWrapper').style.display = 'block';
                if(document.getElementById('recentTitle')) document.getElementById('recentTitle').style.display = 'flex';
                if(document.getElementById('communityBox')) document.getElementById('communityBox').style.display = 'block';
                if(document.querySelector('.developer-credit')) document.querySelector('.developer-credit').style.display = 'block';
            }
            timeout = setTimeout(() => loadMovies(1), 500); 
        });

        // ==========================================================
        // 🎬 ULTRA-PREMIUM MOVIE DETAILS LOGIC & INTERACTIONS
        // ==========================================================
        async function openMovieDetailsPage(encodedTitle) {
            let title = decodeURIComponent(encodedTitle);
            const movie = loadedMovies[title];
            if (!movie) return;
            currentOpenMovie = movie;

            document.getElementById('detailMovieTitle').innerText = title;
            document.getElementById('detailHeroImg').src = `/api/image/${movie.photo_id}`;
            document.getElementById('detailCommentInput').value = '';

            // ভিউ বৃদ্ধি
            fetch('/api/view_movie', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: title})
            }).catch(e => {});

            // মেটাডাটা ফেচ (লাইক, ডাউনলোড, রেটিং)
            fetchMovieMetaData(title);
            fetchMovieComments(title);

            // ওয়াচলিস্ট স্টেট চেক
            fetch(`/api/watchlist/list/${uid}`)
                .then(res => res.json())
                .then(wlData => {
                    isCurrentSaved = wlData.watchlist.some(w => w.title === title);
                    updateSaveButtonUI();
                }).catch(e => {});

            document.getElementById('homePageMain').style.display = 'none';
            document.getElementById('movieDetailScreen').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            tg.BackButton.show();
        }

        function closeMovieDetailScreen() {
            document.getElementById('movieDetailScreen').style.display = 'none';
            document.getElementById('homePageMain').style.display = 'block';
            tg.BackButton.hide();
        }

        tg.BackButton.onClick(function() {
            if (document.getElementById('qualityDrawerModal').style.display === 'flex') {
                closeDownloadDrawer();
            } else if (document.getElementById('movieDetailScreen').style.display === 'block') {
                closeMovieDetailScreen();
            } else {
                history.back();
            }
        });

        async function fetchMovieMetaData(title) {
            try {
                const res = await fetch(`/api/movie/meta/${encodeURIComponent(title)}?uid=${uid}`);
                const data = await res.json();
                
                document.getElementById('detailLikesCount').innerText = data.likes || 0;
                document.getElementById('detailDownloadsCount').innerText = data.downloads || 0;
                document.getElementById('detailCommentsCount').innerText = data.comments_count || 0;
                document.getElementById('detailCommentsCountHeader').innerText = data.comments_count || 0;
                document.getElementById('detailRatingAvg').innerText = data.avg_rating > 0 ? data.avg_rating.toFixed(1) : '0.0';
                document.getElementById('detailRatingCount').innerText = data.ratings_count || 0;
                
                isCurrentLiked = data.is_liked;
                updateLikeButtonUI();
                setInteractiveStarsUI(data.user_rating || 0);
            } catch(e) {}
        }

        function updateLikeButtonUI() {
            const btn = document.getElementById('detailLikePillBtn');
            const heart = document.getElementById('statHeartIcon');
            if (isCurrentLiked) {
                btn.className = "action-btn-pill liked";
                btn.innerHTML = `<i class="fa-solid fa-heart"></i> Liked`;
                heart.style.color = "#ef4444";
            } else {
                btn.className = "action-btn-pill";
                btn.innerHTML = `<i class="fa-regular fa-heart"></i> Like`;
                heart.style.color = "#94a3b8";
            }
        }

        function updateSaveButtonUI() {
            const btn = document.getElementById('detailSavePillBtn');
            if (isCurrentSaved) {
                btn.className = "action-btn-pill saved";
                btn.innerHTML = `<i class="fa-solid fa-bookmark"></i> Saved`;
            } else {
                btn.className = "action-btn-pill";
                btn.innerHTML = `<i class="fa-regular fa-bookmark"></i> Save`;
            }
        }

        async function toggleLikeFromDetails() {
            if (!currentOpenMovie) return;
            try {
                const res = await fetch('/api/movie/like', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, title: currentOpenMovie._id, initData: INIT_DATA })
                });
                const data = await res.json();
                if (data.ok) {
                    isCurrentLiked = data.is_liked;
                    document.getElementById('detailLikesCount').innerText = data.total_likes;
                    updateLikeButtonUI();
                }
            } catch(e) {}
        }

        async function toggleWatchlistFromDetails() {
            if (!currentOpenMovie) return;
            const title = currentOpenMovie._id;
            let endpoint = isCurrentSaved ? '/api/watchlist/remove' : '/api/watchlist/add';
            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, title: title, initData: INIT_DATA })
                });
                const d = await res.json();
                if (d.ok) {
                    isCurrentSaved = !isCurrentSaved;
                    updateSaveButtonUI();
                    tg.showAlert(isCurrentSaved ? "💾 Saved to Watchlist!" : "❌ Removed from Watchlist!");
                }
            } catch(e) {}
        }

        function setInteractiveStarsUI(rating) {
            const stars = document.querySelectorAll('#detailInteractiveStars i');
            stars.forEach((star, index) => {
                if (index < rating) star.className = "fa-solid fa-star active-star";
                else star.className = "fa-solid fa-star";
            });
        }

        async function rateMovie(rating) {
            if (!currentOpenMovie) return;
            const title = currentOpenMovie._id;
            const uname = tg.initDataUnsafe?.user?.first_name || 'Guest';
            setInteractiveStarsUI(rating);
            try {
                await fetch('/api/reviews/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, uname: uname, title: title, rating: rating, initData: INIT_DATA })
                });
                tg.showAlert(`⭐ You rated this ${rating} Stars!`);
                fetchMovieMetaData(title);
            } catch(e) {}
        }

        async function fetchMovieComments(title) {
            try {
                const res = await fetch(`/api/reviews/get/${encodeURIComponent(title)}`);
                const data = await res.json();
                let html = '';
                
                if (data.reviews.length === 0) {
                    html = `
                    <div class="comment-card-bubble">
                        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop" class="comment-avatar" alt="Avatar">
                        <div class="comment-body-right">
                            <div class="comment-author-name">MRM <span class="comment-time-ago">4 দিন আগে</span></div>
                            <div class="comment-text-msg">অনেক ধন্যবাদ এই মুভিটা অনেক জায়গায় খুজেছি। অবশেষে এখানে পাইলাম 💥</div>
                            <div class="comment-reply-bar">
                                <span><i class="fa-solid fa-thumbs-up text-yellow-400"></i> 1</span>
                                <span>Reply</span>
                            </div>
                        </div>
                    </div>`;
                } else {
                    const avatarList = [
                        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop",
                        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop"
                    ];
                    data.reviews.forEach((r, idx) => {
                        let av = avatarList[idx % avatarList.length];
                        html += `
                        <div class="comment-card-bubble">
                            <img src="${av}" class="comment-avatar" alt="Avatar">
                            <div class="comment-body-right">
                                <div class="comment-author-name">${r.uname} <span class="comment-time-ago">${r.time_ago}</span></div>
                                <div class="comment-text-msg">${r.review}</div>
                                <div class="comment-reply-bar">
                                    <span><i class="fa-solid fa-thumbs-up text-yellow-400"></i> ${r.rating || 1}</span>
                                    <span>Reply</span>
                                </div>
                            </div>
                        </div>`;
                    });
                }
                document.getElementById('detailCommentsList').innerHTML = html;
            } catch(e) {}
        }

        async function postDetailComment() {
            const input = document.getElementById('detailCommentInput');
            const text = input.value.trim();
            if (!text || !currentOpenMovie) return;
            const uname = tg.initDataUnsafe?.user?.first_name || 'Guest';

            try {
                const res = await fetch('/api/reviews/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        uid: uid,
                        uname: uname,
                        title: currentOpenMovie._id,
                        rating: 5,
                        review: text,
                        initData: INIT_DATA
                    })
                });
                input.value = '';
                fetchMovieComments(currentOpenMovie._id);
                fetchMovieMetaData(currentOpenMovie._id);
            } catch(e) {}
        }

        function shareMovieDeepLink() {
            if (!currentOpenMovie) return;
            const title = currentOpenMovie._id;
            const botShareLink = `https://t.me/${BOT_UNAME}?start=new`;
            const text = `🍿 *${title}* - এখন আমাদের বটে পাওয়া যাচ্ছে! সরাসরি দেখতে ও ডাউনলোড করতে ক্লিক করুন: 👇\n\n🔗 ${botShareLink}`;
            window.open(`https://t.me/share/url?url=&text=${encodeURIComponent(text)}`);
        }

        function openDownloadDrawer() {
            if (!currentOpenMovie) return;
            document.getElementById('drawerQualityList').innerHTML = currentOpenMovie.files.map(f => {
                let isFree = f.is_unlocked || isUserVip;
                let icon = isFree ? '<i class="fa-solid fa-paper-plane text-green-400"></i>' : '<i class="fa-solid fa-lock text-red-400"></i>';
                let cls = isFree ? 'border-left: 5px solid #10b981;' : 'border-left: 5px solid #ef4444;';
                return `<div class="rgb-border" onclick="handleQualityClick('${f.id}', ${f.is_unlocked})"><div class="rgb-inner" style="${cls}"><span><i class="fa-solid fa-download"></i> ${f.quality}</span> ${icon}</div></div>`;
            }).join('');
            document.getElementById('qualityDrawerModal').style.display = 'flex';
        }

        function closeDownloadDrawer() {
            document.getElementById('qualityDrawerModal').style.display = 'none';
        }

        // ==========================================================
        // 📥 SEND / UNLOCK FILE LOGIC
        // ==========================================================
        let currentFileId = null;
        function handleQualityClick(fileId, isUnlocked) {
            closeDownloadDrawer();
            if(isUnlocked || isUserVip) { 
                sendFileAndClose(fileId); 
            } else { 
                currentFileId = fileId; 
                document.getElementById('directLinkModal').style.display = 'flex';
                resetDlButton();
            }
        }

        let linkOpenedAt = 0;
        let isWaitingForReturn = false;
        let dlTimerInterval = null;

        function resetDlButton() {
            const btn = document.getElementById('dlClickBtn');
            btn.onclick = executeDirectLink;
            btn.innerText = "🔗 Click Here (Open Link) 🚀✅";
            btn.style.background = "linear-gradient(45deg, #ef4444, #f97316)";
            btn.disabled = false;
        }

        function executeDirectLink() {
            if (!DIRECT_LINKS || DIRECT_LINKS.length === 0) { 
                document.getElementById('directLinkModal').style.display = 'none'; 
                if (currentFileId) sendFileAndClose(currentFileId); 
                return; 
            }
            
            tg.openLink(DIRECT_LINKS[Math.floor(Math.random() * DIRECT_LINKS.length)]);
            linkOpenedAt = Date.now(); 
            isWaitingForReturn = true;
            
            const btn = document.getElementById('dlClickBtn');
            btn.disabled = true; 
            let timeLeft = AD_WAIT_TIME; 
            btn.style.background = "#475569";
            
            dlTimerInterval = setInterval(() => {
                timeLeft--; 
                if(timeLeft > 0) {
                    btn.innerText = `⏳ Please wait... (${timeLeft}s)`;
                } else {
                    clearInterval(dlTimerInterval);
                    if(isWaitingForReturn) {
                        isWaitingForReturn = false;
                        document.getElementById('directLinkModal').style.display = 'none';
                        if (currentFileId) sendFileAndClose(currentFileId);
                    }
                }
            }, 1000);
        }

        let coinLinkOpenedAt = 0; 
        let isWaitingForCoinReturn = false; 
        let coinTimerInterval = null;

        function resetCoinButton() {
            const btn = document.getElementById('coinAdBtn');
            btn.disabled = false;
            btn.onclick = executeCoinAd;
            btn.innerHTML = '<i class="fa-solid fa-play"></i> Watch Ad & Get 5 Points';
            btn.style.background = "linear-gradient(45deg, #ef4444, #f97316)";
        }

        function executeCoinAd() {
            if (!DIRECT_LINKS || DIRECT_LINKS.length === 0) { tg.showAlert("⚠️ No ads available right now!"); return; }
            tg.openLink(DIRECT_LINKS[Math.floor(Math.random() * DIRECT_LINKS.length)]);
            
            coinLinkOpenedAt = Date.now(); 
            isWaitingForCoinReturn = true;
            
            const btn = document.getElementById('coinAdBtn');
            btn.disabled = true; 
            let timeLeft = AD_WAIT_TIME; 
            btn.style.background = "#475569";
            
            coinTimerInterval = setInterval(() => {
                timeLeft--; 
                if(timeLeft > 0) {
                    btn.innerHTML = `<i class="fa-solid fa-play"></i> Please wait... (${timeLeft}s)`;
                } else {
                    clearInterval(coinTimerInterval);
                    if(isWaitingForCoinReturn) {
                        isWaitingForCoinReturn = false;
                        claimAdCoin();
                        resetCoinButton();
                    }
                }
            }, 1000);
        }

        document.addEventListener("visibilitychange", function() {
            if (document.visibilityState === 'visible') {
                let now = Date.now();
                if (isWaitingForReturn) {
                    isWaitingForReturn = false; 
                    clearInterval(dlTimerInterval);
                    let elapsedSeconds = (now - linkOpenedAt) / 1000;
                    if (elapsedSeconds < AD_WAIT_TIME - 1) { 
                        tg.showAlert(`⚠️ You must wait full ${AD_WAIT_TIME} seconds on the link.`);
                        resetDlButton();
                    } else { 
                        document.getElementById('directLinkModal').style.display = 'none'; 
                        if (currentFileId) sendFileAndClose(currentFileId); 
                    }
                }
                if (isWaitingForCoinReturn) {
                    isWaitingForCoinReturn = false; 
                    clearInterval(coinTimerInterval);
                    let elapsedSeconds = (now - coinLinkOpenedAt) / 1000;
                    if (elapsedSeconds < AD_WAIT_TIME - 1) {
                        tg.showAlert(`⚠️ You must wait full ${AD_WAIT_TIME} seconds on the link.`);
                        resetCoinButton();
                    } else { 
                        claimAdCoin(); 
                        resetCoinButton();
                    }
                }
            }
        });

        async function claimAdCoin() {
            try {
                const res = await fetch('/api/add_coin', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({uid: uid, initData: INIT_DATA}) });
                const data = await res.json();
                if(data.ok) { 
                    tg.showAlert("🎉 Congratulations! You received 5 Points.");
                    fetchUserInfo(); 
                }
            } catch (e) {}
        }

        async function buyVipWithCoins() {
            const vCost = parseInt(document.getElementById('btnVipCost').innerText) || 30;
            const vDays = parseInt(document.getElementById('btnVipDays').innerText) || 1;
            
            if(userCoins < vCost) {
                tg.showAlert(`⚠️ Not enough points! You need ${vCost} points.`);
                return;
            }
            if(confirm(`Do you want to buy ${vDays} Days VIP for ${vCost} points?`)) {
                try {
                    const res = await fetch('/api/buy_vip', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({uid: uid, initData: INIT_DATA}) });
                    const data = await res.json();
                    if(data.ok) { 
                        document.getElementById('vipModal').style.display = 'none';
                        tg.showAlert("🎉 Success! Your VIP has been activated.");
                        fetchUserInfo(); 
                    } else { tg.showAlert(data.msg); }
                } catch (e) {}
            }
        }

        function showProcessingUI() {
            let procModal = document.getElementById('processingModalCustom');
            if(!procModal) {
                procModal = document.createElement('div');
                procModal.id = 'processingModalCustom';
                procModal.style.cssText = 'position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:9999; display:flex; align-items:center; justify-content:center; flex-direction:column; backdrop-filter: blur(5px);';
                procModal.innerHTML = `
                    <div class="spinner-new"></div>
                    <div class="big-processing-text">Sending File...</div>
                    <div style="color:#cbd5e1; margin-top:15px; font-size:16px; font-weight:bold;">Please wait, video is going to your bot inbox!</div>
                `;
                document.body.appendChild(procModal);
            }
            procModal.style.display = 'flex';
        }

        function hideProcessingUI() {
            let procModal = document.getElementById('processingModalCustom');
            if(procModal) procModal.style.display = 'none';
        }

        async function sendFileAndClose(id) {
            showProcessingUI(); 
            try {
                const res = await fetch('/api/send', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({userId: uid, movieId: id, initData: INIT_DATA}) });
                const data = await res.json();
                if(data.ok) { 
                    setTimeout(() => tg.close(), 500);
                } else {
                    hideProcessingUI();
                    tg.showAlert("⚠️ Session expired! Please close and reopen the mini app.");
                }
            } catch (e) {
                hideProcessingUI();
                tg.showAlert("⚠️ Network error! Please try again.");
            }
        }

        async function claimDailyCheckin() {
            try {
                const res = await fetch('/api/gamification/daily_checkin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, initData: INIT_DATA })
                });
                const d = await res.json();
                if (d.ok) {
                    tg.showAlert(`🎉 Checked-in Successfully! You received +5 Points.`);
                    fetchUserInfo();
                } else { tg.showAlert(`⚠️ ${d.msg}`); }
            } catch(e) {}
        }

        let isSpinning = false;
        async function spinWheel() {
            if (isSpinning) return;
            try {
                const res = await fetch('/api/gamification/spin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, initData: INIT_DATA })
                });
                const data = await res.json();
                if (!data.ok) { tg.showAlert(`⚠️ ${data.msg}`); return; }

                isSpinning = true;
                const inner = document.getElementById('wheelInner');
                const degMap = { 0: 25, 2: 75, 5: 125, 10: 175, 20: 225, 50: 275, vip: 325 };
                let prizeKey = data.reward.type === 'points' ? data.reward.amount : 'vip';
                let targetDeg = degMap[prizeKey] || 25;
                let finalRotation = (5 * 360) + (360 - targetDeg);

                inner.style.transform = `rotate(${finalRotation}deg)`;

                setTimeout(() => {
                    tg.showAlert(data.msg);
                    isSpinning = false;
                    inner.style.transition = 'none';
                    inner.style.transform = `rotate(${360 - targetDeg}deg)`;
                    setTimeout(() => { inner.style.transition = 'transform 4s cubic-bezier(0.25, 0.1, 0.25, 1)'; }, 50);
                    fetchUserInfo();
                }, 4100);
            } catch(e) { isSpinning = false; }
        }

        async function renderLeaderboard() {
            try {
                const res = await fetch('/api/gamification/leaderboard');
                const d = await res.json();
                let html = '';
                d.leaderboard.forEach((user, idx) => {
                    let rankMedal = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : `[${idx+1}]`;
                    html += `
                    <div style="background: rgba(30,41,59,0.5); padding: 10px 15px; border-radius: 12px; border:1px solid #334155; display:flex; justify-content:space-between; align-items:center;">
                        <div style="display:flex; align-items:center; gap: 10px;">
                            <span>${rankMedal}</span>
                            <span style="font-weight:bold; color:white;">${user.name}</span>
                        </div>
                        <span style="color:#fbbf24; font-weight:bold; font-size:13px;"><i class="fa-solid fa-share-nodes"></i> ${user.refer_count} Ref</span>
                    </div>`;
                });
                document.getElementById('leaderboardList').innerHTML = html || '<p class="text-gray-500">No leaderboard entries.</p>';
            } catch(e) {}
        }

        function openRequestsTrackerModal() { document.getElementById('requestsTrackerModal').style.display = 'flex'; closeMenu(); renderRequestsTracker(); }
        async function submitReqTracker() {
            const val = document.getElementById('reqTrackerInput').value.trim();
            if (!val) return;
            const uname = tg.initDataUnsafe?.user?.first_name || 'Guest';
            try {
                await fetch('/api/request', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, uname: uname, movie: val, initData: INIT_DATA })
                });
                document.getElementById('reqTrackerInput').value = '';
                tg.showAlert('🎉 Request queued!');
                renderRequestsTracker();
            } catch(e) {}
        }

        async function renderRequestsTracker() {
            try {
                const res = await fetch(`/api/requests/user_list/${uid}`);
                const d = await res.json();
                let html = '';
                d.requests.forEach(req => {
                    let statusText = req.status === 'pending' ? '⏳ Pending' : req.status === 'processing' ? '⚙️ Processing' : '✅ Uploaded';
                    let pct = req.status === 'pending' ? 30 : req.status === 'processing' ? 70 : 100;
                    let barColor = req.status === 'pending' ? '#f59e0b' : req.status === 'processing' ? '#3b82f6' : '#10b981';
                    html += `
                    <div style="background: rgba(30,41,59,0.5); padding: 15px; border-radius: 12px; border:1px solid #334155;">
                        <div style="display:flex; justify-content:space-between; margin-bottom: 6px;">
                            <span style="font-weight:bold; color:white;">${req.movie}</span>
                            <span style="font-size:11px; font-weight:bold; color:${barColor};">${statusText}</span>
                        </div>
                        <div style="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
                            <div style="height:100%; width:${pct}%; background:${barColor}; border-radius:10px;"></div>
                        </div>
                    </div>`;
                });
                document.getElementById('requestsTrackerList').innerHTML = html || '<p style="color: #64748b; text-align:center;">No movie requests yet.</p>';
            } catch(e) {}
        }

        function openAdCampModal() { document.getElementById('adCampModal').style.display = 'flex'; closeMenu(); }
        async function submitAdCampaign() {
            const title = document.getElementById('campTitle').value;
            const subtitle = document.getElementById('campSubtitle').value || "দেরি না করে এখনো সবাই নিয়ে নিন";
            const link = document.getElementById('campLink').value;
            const img = document.getElementById('campImg').value;
            const packageDays = parseInt(document.getElementById('campPackage').value);
            let cost = packageDays === 3 ? 1200 : packageDays === 7 ? 2500 : 500;
            
            if(!title || !link) { tg.showAlert("Title and Link are required!"); return; }
            if(confirm(`Cost is ${cost} Points for ${packageDays} Days. Proceed?`)) {
                try {
                    const res = await fetch('/api/ads/create', { 
                        method: 'POST', 
                        headers: {'Content-Type': 'application/json'}, 
                        body: JSON.stringify({uid: uid, initData: INIT_DATA, title: title, subtitle: subtitle, link: link, image_url: img, package: packageDays}) 
                    });
                    const data = await res.json();
                    if(data.ok) {
                        tg.showAlert("🎉 Campaign Started Successfully!");
                        document.getElementById('adCampModal').style.display = 'none';
                        fetchUserInfo(); fetchActiveAds(); 
                    } else { tg.showAlert("⚠️ " + data.msg); }
                } catch(e) {}
            }
        }

        function renderCommunitySection() {
            let html = '';
            if(SOCIAL_LINKS.fb_group) html += `<a href="${SOCIAL_LINKS.fb_group}" target="_blank" class="social-btn fb-btn"><i class="fa-brands fa-facebook"></i> FB Group</a>`;
            if(SOCIAL_LINKS.fb_page) html += `<a href="${SOCIAL_LINKS.fb_page}" target="_blank" class="social-btn fb-btn"><i class="fa-brands fa-facebook-f"></i> FB Page</a>`;
            if(SOCIAL_LINKS.youtube) html += `<a href="${SOCIAL_LINKS.youtube}" target="_blank" class="social-btn yt-btn"><i class="fa-brands fa-youtube"></i> YouTube</a>`;
            if(SOCIAL_LINKS.review_channel) html += `<a href="${SOCIAL_LINKS.review_channel}" target="_blank" class="social-btn tg-btn"><i class="fa-solid fa-film"></i> Movie Review</a>`;
            
            if(html !== '') {
                document.getElementById('communityBox').innerHTML = `
                <div class="community-section">
                    <div class="section-title" style="justify-content: center; font-size: 18px;"><i class="fa-solid fa-users" style="color: #38bdf8;"></i> Join Our Community</div>
                    <div class="social-grid">${html}</div>
                </div>`;
            }
        }

        function detectLanguage(title) {
            let t = title.toLowerCase();
            let hasBangla = t.includes("bangla") || t.includes("বাংলা");
            let hasHindi = t.includes("hindi") || t.includes("হিন্দি");
            let hasEnglish = t.includes("english") || t.includes("ইংরেজি") || t.includes("eng");
            let hasKorean = t.includes("korean") || t.includes("কোরিয়ান");
            let hasTamil = t.includes("tamil") || t.includes("তামিল");
            let hasTelugu = t.includes("telugu") || t.includes("তেলেগু");
            let hasDual = t.includes("dual") || t.includes("ডুয়েল") || t.includes("multi");

            let count = (hasBangla?1:0) + (hasHindi?1:0) + (hasEnglish?1:0) + (hasKorean?1:0) + (hasTamil?1:0) + (hasTelugu?1:0);
            if (hasDual || count > 1) return "Dual Audio";
            if (hasBangla) return "Bangla";
            if (hasHindi) return "Hindi";
            if (hasEnglish) return "English";
            if (hasKorean) return "Korean";
            if (hasTamil) return "Tamil";
            if (hasTelugu) return "Telugu";
            return "Movie";
        }

        async function initApp() {
            try {
                await Promise.all([
                    fetchUserInfo(),
                    fetchActiveAds(),
                    loadCategories(),
                    loadTrending(),
                    loadMovies(1)
                ]);
                renderCommunitySection();
            } catch(e) {}
        }

        initApp();
    </script>
</body>
</html>
"""