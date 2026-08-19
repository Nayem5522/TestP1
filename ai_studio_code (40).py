# html_template.py

HTML_CODE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Prime Flix</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Poppins:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-red: #E50914;
            --neon-cyan: #00f2ff;
            --neon-green: #00ffa3;
            --gold-accent: #f5c518;
            --bg-dark: #070a13;
            --card-bg: #0f172a;
            --card-border: rgba(255, 255, 255, 0.08);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
        body { background: var(--bg-dark); font-family: 'Poppins', sans-serif; color: #fff; overflow-x: hidden; width: 100%; -webkit-overflow-scrolling: touch; padding-bottom: 80px; } 
        
        header { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 12px 10px; border-bottom: 1px solid #1e293b; position: sticky; top: 0; background: rgba(7, 10, 19, 0.95); backdrop-filter: blur(10px); z-index: 1000; width: 100%; gap: 8px; }
        .logo { font-size: 22px; font-weight: 900; white-space: nowrap; letter-spacing: 1px; }
        .logo span { background: #ef4444; color: #fff; padding: 2px 6px; border-radius: 4px; margin-left: 3px; font-size: 14px; }
        
        .home-btn { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.5); padding: 5px 14px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 5px; transition: 0.2s; white-space: nowrap; }
        .home-btn:active { transform: scale(0.95); background: rgba(59, 130, 246, 0.2); }

        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(7, 10, 19, 0.98); backdrop-filter: blur(15px); border-top: 1px solid #334155; display: flex; justify-content: space-around; align-items: center; padding: 10px 0; z-index: 2000; padding-bottom: calc(10px + env(safe-area-inset-bottom)); }
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
        .search-input { width: 100%; padding: 16px; border-radius: 25px; border: 1px solid #334155; outline: none; text-align: center; background: #13192b; color: #fff; font-size: 17px; font-weight: bold; }
        
        /* 🎨 DYNAMIC CATEGORIES */
        .category-container { display: flex; overflow-x: auto; flex-wrap: nowrap; gap: 12px; padding: 15px 15px 25px; scroll-behavior: smooth; -webkit-overflow-scrolling: touch; width: 100%; }
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

        @keyframes spinClock { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes sparkleStar { 0%, 100% { transform: scale(1) rotate(0deg); } 50% { transform: scale(1.3) rotate(20deg); } }
        @keyframes flickerFlame { 0% { transform: scale(1) rotate(-3deg); } 100% { transform: scale(1.18) rotate(4deg); } }
        @keyframes unselectedPulse { 0%, 100% { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15); transform: scale(1); } 50% { box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35); transform: scale(0.98); } }
        @keyframes activeLatestPulse { 0%, 100% { box-shadow: 0 0 8px 2px rgba(255, 78, 42, 0.4); transform: scale(1); } 50% { box-shadow: 0 0 25px 8px rgba(255, 78, 42, 0.85); transform: scale(1.03); } }
        @keyframes activeForYouPulse { 0%, 100% { box-shadow: 0 0 8px 2px rgba(124, 58, 237, 0.4); transform: scale(1); } 50% { box-shadow: 0 0 25px 8px rgba(124, 58, 237, 0.85); transform: scale(1.03); } }

        .section-title { padding: 5px 15px 15px; font-size: 20px; font-weight: 900; display: flex; align-items: center; gap: 8px; color:#ff416c; }
        
        .trending-container { display: flex; overflow-x: auto; gap: 15px; padding: 0 15px 20px; scroll-behavior: smooth; scroll-snap-type: x mandatory; }
        .trending-container::-webkit-scrollbar { display: none; }
        .trending-card { min-width: 280px; max-width: 280px; background: transparent; overflow: hidden; cursor: pointer; flex-shrink: 0; position: relative; transition: transform 0.2s; scroll-snap-align: start; }
        .trending-card:active { transform: scale(0.98); }

        .grid { padding: 0 15px 20px; display: flex; flex-direction: column; gap: 20px; }
        .card { background: transparent; overflow: hidden; cursor: pointer; transition: transform 0.2s; border-radius: 0; }
        .card:active { transform: scale(0.98); }
        
        .post-content { position: relative; padding: 3px; border-radius: 12px; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); background-size: 200%; }
        .post-content img { width: 100%; aspect-ratio: 16/9; height: auto; object-fit: cover; display: block; border-radius: 10px; }
        .card-footer { padding: 12px 5px 0; display: flex; align-items: flex-start; gap: 12px; text-align: left; }

        .channel-logo { width: 40px; height: 40px; border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden; box-shadow: 0 0 8px rgba(0,0,0,0.5); }
        .channel-logo::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(#ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); animation: spinRing 4s linear infinite; z-index: 1; }
        .channel-logo img { width: calc(100% - 4px); height: calc(100% - 4px); object-fit: cover; border-radius: 50%; position: relative; z-index: 2; background: #05070e; }
        
        .title-text { color: #f8fafc; font-size: 16px; font-weight: bold; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin-top: 2px; }

        .pagination { display: flex; justify-content: center; align-items: center; gap: 8px; padding: 10px 15px 30px; flex-wrap: wrap; }
        .page-btn { background: #1e293b; color: #fff; border: 1px solid #334155; padding: 8px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; outline: none; transition: 0.2s;}
        .page-btn:hover { background: #334155; }
        .page-btn.active { background: #f87171; border-color: #f87171; color: white; }

        /* =========================================================
           🍿 ULTRA-PREMIUM FULL-SCREEN MOVIE DETAIL VIEW (MOBILE OTT)
           ========================================================= */
        #detailScreen {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #050711;
            z-index: 4000;
            overflow-y: auto;
            padding-bottom: 90px;
            animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes slideIn { 0% { transform: translateX(100%); } 100% { transform: translateX(0); } }

        .detail-top-nav {
            position: sticky; top: 0;
            background: rgba(7, 10, 19, 0.9);
            backdrop-filter: blur(15px);
            padding: 12px 15px;
            display: flex; align-items: center; justify-content: space-between;
            z-index: 50; border-bottom: 1px solid rgba(255,255,255,0.08);
        }

        .back-nav-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff; padding: 7px 15px; border-radius: 30px;
            font-size: 13px; font-weight: 700; cursor: pointer;
            display: flex; align-items: center; gap: 6px;
        }

        .hero-banner-wrap {
            position: relative;
            width: 100%; aspect-ratio: 16/9;
            background: #000;
            overflow: hidden;
        }
        .hero-banner-img {
            width: 100%; height: 100%;
            object-fit: cover;
            filter: brightness(0.85);
        }
        .hero-banner-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, transparent 40%, rgba(5, 7, 17, 0.95) 100%);
        }

        .poster-meta-dock {
            display: flex; gap: 15px; padding: 0 15px;
            margin-top: -65px; position: relative; z-index: 10;
        }
        .dock-poster-card {
            width: 110px; aspect-ratio: 2/3;
            border-radius: 12px; overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 25px rgba(0,0,0,0.8);
            flex-shrink: 0; background: #13192b;
        }
        .dock-poster-card img { width: 100%; height: 100%; object-fit: cover; }
        
        .dock-title-info {
            display: flex; flex-direction: column; justify-content: flex-end;
            padding-bottom: 5px;
        }
        .detail-movie-title {
            font-size: 21px; font-weight: 900; line-height: 1.25; color: #fff;
            margin-bottom: 6px;
        }

        .badge-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 15px 0; }
        .chip {
            padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;
            display: inline-flex; align-items: center; gap: 5px;
        }
        .chip-rating { background: rgba(245, 197, 24, 0.15); color: #fbbf24; border: 1px solid rgba(245, 197, 24, 0.3); }
        .chip-genre { background: rgba(0, 242, 255, 0.1); color: #00f2ff; border: 1px solid rgba(0, 242, 255, 0.25); }
        .chip-lang { background: rgba(0, 255, 163, 0.1); color: #00ffa3; border: 1px solid rgba(0, 255, 163, 0.25); }
        .chip-year { background: rgba(255, 255, 255, 0.08); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.15); }

        /* RGB Dynamic Gateway Download Box */
        .gateway-hub-card {
            margin: 20px 0;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
            border-radius: 18px; padding: 20px 15px;
            border: 2px solid transparent;
            background-image: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), 
                              linear-gradient(135deg, #ff0055, #00f2ff, #00ffa3);
            background-origin: border-box; background-clip: padding-box, border-box;
            box-shadow: 0 10px 30px rgba(0, 242, 255, 0.15);
            text-align: center;
        }

        .rgb-border-action {
            position: relative;
            background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
            background-size: 200%; padding: 3px; border-radius: 14px; margin-bottom: 10px; cursor: pointer; width: 100%;
        }
        .rgb-inner-action {
            display: flex; justify-content: space-between; align-items: center;
            background: #090e1b; padding: 14px 16px; border-radius: 11px;
            color: white; font-weight: 800; font-size: 15px;
        }

        .cast-tile-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 12px;
        }
        .cast-tile {
            background: rgba(19, 25, 43, 0.6); padding: 8px; border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; gap: 10px;
        }
        .cast-tile img { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; border: 1.5px solid var(--neon-cyan); }
        .cast-tile-name { font-size: 12px; font-weight: bold; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .cast-tile-char { font-size: 10px; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: none; align-items: center; justify-content: center; z-index: 5000; backdrop-filter: blur(5px); }
        .modal-content { background: #1e293b; width: 92%; max-width: 400px; padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #334155; max-height: 85vh; overflow-y: auto; position: relative; }
        .close-icon { position: absolute; top: 12px; right: 15px; width: 32px; height: 32px; border-radius: 50%; background: #334155; color: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; }
        
        .dl-rgb-wrap { position: relative; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); background-size: 200%; padding: 4px; border-radius: 16px; width: 100%; max-width: 350px; margin: auto; }
        .dl-inner-box { background: rgba(15, 23, 42, 0.98); border-radius: 12px; padding: 30px 20px; display: flex; flex-direction: column; align-items: center; gap: 15px; }
        .btn-submit { background: linear-gradient(45deg, #10b981, #059669); color: white; border: none; padding: 15px 20px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 16px; cursor: pointer; }
        
        .spinner-new { width: 65px; height: 65px; border: 5px solid rgba(255,255,255,0.1); border-left-color: #10b981; border-radius: 50%; animation: spin-fast 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin-fast { 100% { transform: rotate(360deg); } }
        .big-processing-text { font-size: 24px; font-weight: 900; color: #4ade80; }

        .top-badge, .ep-badge, .view-badge, .lang-card-badge { position: absolute; font-weight: bold; padding: 4px 8px; border-radius: 6px; font-size: 11px; z-index: 10; color: white; }
        .top-badge { top: 12px; left: 12px; background: linear-gradient(45deg, #ff0000, #cc0000); }
        .view-badge { bottom: 12px; left: 12px; background: rgba(0,0,0,0.75); }
        .ep-badge { bottom: 12px; right: 12px; background: #10b981; }
        .lang-card-badge { top: 12px; right: 12px; background: linear-gradient(135deg, #ef4444, #dc2626); font-size: 10px; font-weight: 900; text-transform: uppercase; }

        @keyframes spinRing { 0% { transform: rotate(0deg); filter: hue-rotate(0deg); } 100% { transform: rotate(360deg); filter: hue-rotate(360deg); } }
    </style>
</head>
<body onclick="closeMenu(event)">

    <!-- হেডার -->
    <header>
        <div class="logo"><span>𝑷𝑹𝑰𝑴𝑬 𝑪𝑰𝑵𝑬𝑭𝑳𝑰𝑿</span></div>
        <button onclick="goHome()" class="home-btn"><i class="fa-solid fa-house"></i> Home Page</button>
    </header>

    <!-- প্রোফাইল ও সেটিংস ড্রপডাউন মেনু -->
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
        <a onclick="window.open('{{TG_LINK}}')"><i class="fa-solid fa-bullhorn text-green-400"></i> Our Channel</a>
        <a onclick="window.open('{{SUPPORT_LINK}}')"><i class="fa-brands fa-telegram text-blue-400"></i> Support / Contact</a>
    </div>

    <!-- মূল হোম পেজ কন্টেন্ট -->
    <div id="mainHomeScreen">
        <div class="search-box">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search Movies or Series...">
        </div>

        <div id="categoryBox" class="category-container"></div>

        <div id="trendingWrapper">
            <div class="section-title"><span style="color:#ff4e2a; margin-right:5px;">🔥</span> Trending now</div>
            <div class="trending-container" id="trendingGrid"></div>
        </div>

        <div class="section-title" id="recentTitle"><i class="fa-solid fa-clock-rotate-left text-blue-400"></i> Recently Added</div>
        <div class="grid" id="movieGrid"></div>
        <div class="pagination" id="paginationBox"></div>
        
        <div id="communityBox"></div>
    </div>

    <!-- =========================================================
         🍿 ULTRA-PREMIUM CINEMATIC MOVIE DETAIL FULL-PAGE VIEW
         ========================================================= -->
    <div id="detailScreen">
        <!-- স্টিকি ব্যাক হেডার -->
        <div class="detail-top-nav">
            <button onclick="closeDetails()" class="back-nav-btn"><i class="fa-solid fa-arrow-left"></i> Back</button>
            <div style="display: flex; gap: 8px;">
                <button id="detailBookmarkBtn" onclick="toggleWatchlist()" class="back-nav-btn" style="border-color: #f59e0b; color: #fbbf24;"><i class="fa-regular fa-bookmark"></i> Save</button>
            </div>
        </div>

        <!-- হিরো ব্যাকড্রপ সিনেমাটিক ব্যানার -->
        <div class="hero-banner-wrap">
            <img id="detailHeroBackdrop" src="" class="hero-banner-img">
            <div class="hero-banner-overlay"></div>
        </div>

        <!-- ওভারলে পোস্টার এবং টাইটেল ডক -->
        <div class="poster-meta-dock">
            <div class="dock-poster-card">
                <img id="detailPosterThumb" src="" alt="Poster">
            </div>
            <div class="dock-title-info">
                <h1 id="detailTitle" class="detail-movie-title">Movie Title</h1>
                <div style="font-size: 12px; color: #38bdf8; font-weight: bold;" id="detailTypeBadge">Movie / Series</div>
            </div>
        </div>

        <div style="padding: 15px;">
            <!-- মেটাডাটা চিপস ও রেটিং -->
            <div class="badge-chips">
                <span class="chip chip-rating"><i class="fa-solid fa-star"></i> <span id="detailRatingVal">N/A</span>/10</span>
                <span class="chip chip-year" id="detailYearChip"><i class="fa-solid fa-calendar"></i> 2024</span>
                <span class="chip chip-lang" id="detailLangChip"><i class="fa-solid fa-language"></i> Dual Audio</span>
                <span class="chip chip-genre" id="detailGenreChip"><i class="fa-solid fa-film"></i> Action</span>
            </div>

            <!-- ডেসক্রিপশন / সিনোপসিস -->
            <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 20px;">
                <h3 style="font-size: 14px; font-weight: 800; color: #cbd5e1; margin-bottom: 6px;"><i class="fa-solid fa-align-left text-blue-400"></i> Storyline / Overview</h3>
                <p id="detailOverview" style="font-size: 13px; color: #94a3b8; line-height: 1.6;">Loading official synopsis...</p>
            </div>

            <!-- 🚀 ULTRA HIGH-SPEED DOWNLOAD & STREAM HUB (WEB-APP UNLOCK INTEGRATION) -->
            <div class="gateway-hub-card">
                <h2 style="font-size: 18px; font-weight: 900; color: #fff; margin-bottom: 8px; font-family:'Orbitron', sans-serif;">
                    <i class="fa-solid fa-magnet" style="color: #ff0055;"></i> Ultra High-Speed Links
                </h2>
                <p style="font-size: 12px; color: #cbd5e1; line-height: 1.5; margin-bottom: 15px;">
                    Download or stream directly in your preferred resolution. Multiple servers and Telegram bot direct links prepared below.
                </p>

                <!-- কোয়ালিটি লিংক লিস্ট কন্টেইনার -->
                <div id="detailQualityList" style="display: flex; flex-direction: column; gap: 8px;"></div>
            </div>

            <!-- 🎬 VLC AUDIO FIX NOTICE BOX -->
            <div style="background: #08080c; border: 1.5px solid rgba(0, 242, 255, 0.2); border-radius: 14px; padding: 16px 14px; margin: 20px 0; text-align: center;">
                <h4 style="color: #ffeb3b; font-size: 14px; font-weight: bold; margin-bottom: 8px;">
                    🎬 ভিডিও প্লে করলে যদি সাউন্ড না আসে 🔊
                </h4>
                <p style="color: #cbd5e1; font-size: 12px; line-height: 1.4; margin-bottom: 12px;">
                    👉 <b>VLC Player</b> অথবা <b>MX Player</b> দিয়ে প্লে করে অডিও ট্র্যাক পরিবর্তন করুন, সাউন্ড চলে আসবে!
                </p>
                <div style="display: flex; justify-content: center; gap: 10px;">
                    <a href="https://play.google.com/store/apps/details?id=org.videolan.vlc" target="_blank" class="home-btn" style="border-color: #00f2ff; color:#00f2ff;"><i class="fa-brands fa-google-play"></i> Get VLC Player</a>
                </div>
            </div>

            <!-- 🎥 TMDB OFFICIAL TRAILER SECTION -->
            <div id="detailTrailerSection" style="margin: 25px 0; display: none;">
                <h3 style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 10px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-circle-play text-red-500"></i> Official Movie Trailer
                </h3>
                <div style="position: relative; width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden; border: 1.5px solid rgba(255,255,255,0.1);">
                    <iframe id="detailTrailerIframe" src="" style="width: 100%; height: 100%; border: none;" allowfullscreen></iframe>
                </div>
            </div>

            <!-- 👥 TOP CAST MEMBERS -->
            <div id="detailCastSection" style="margin: 25px 0; display: none;">
                <h3 style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-user-group text-blue-400"></i> Characters & Main Cast
                </h3>
                <div class="cast-tile-grid" id="detailCastGrid"></div>
            </div>

            <!-- 💬 USER REVIEWS & RATINGS -->
            <div style="border-top: 1px solid #1e293b; padding-top: 20px; margin-top: 25px;">
                <h3 style="font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #cbd5e1;"><i class="fa-solid fa-comments text-yellow-400"></i> Audience Reviews</h3>
                
                <div style="background: rgba(15, 23, 42, 0.5); padding: 12px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 15px;">
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 6px; font-weight:bold;">Your Rating:</p>
                    <div style="display: flex; gap: 6px; font-size: 20px; color: #475569; cursor: pointer; margin-bottom: 10px;" id="starRatingSelect">
                        <i class="fa-solid fa-star" onclick="setSelectRating(1)"></i>
                        <i class="fa-solid fa-star" onclick="setSelectRating(2)"></i>
                        <i class="fa-solid fa-star" onclick="setSelectRating(3)"></i>
                        <i class="fa-solid fa-star" onclick="setSelectRating(4)"></i>
                        <i class="fa-solid fa-star" onclick="setSelectRating(5)"></i>
                    </div>
                    <textarea id="reviewText" style="width: 100%; height: 50px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: white; padding: 8px; font-size: 13px; outline: none; resize: none; margin-bottom: 8px;" placeholder="Write your review..."></textarea>
                    <button class="btn-submit" style="font-size: 13px; padding: 8px 16px; width: auto;" onclick="submitReview()">Submit Review</button>
                </div>

                <div id="modalReviewsList" style="display: flex; flex-direction: column; gap: 8px;"></div>
            </div>
        </div>
    </div>

    <!-- 🛑 আনলক / অ্যাড ওয়েটিং মডাল (আমাদের আসল আনলক সিস্টেম) -->
    <div id="directLinkModal" class="modal">
        <div class="modal-content" style="background: transparent; border: none; padding: 0;">
            <div class="close-icon" onclick="document.getElementById('directLinkModal').style.display='none'" style="top: -15px; right: 5px; z-index: 1000;"><i class="fa-solid fa-xmark"></i></div>
            <div class="dl-rgb-wrap">
                <div class="dl-inner-box">
                    <h2 style="color: #4ade80; font-size: 22px; font-weight: 900;"><i class="fa-solid fa-unlock-keyhole"></i> Unlock Video</h2>
                    <p id="dlDescText" style="color: #cbd5e1; font-size: 14px; font-weight: 600; text-align:center;">
                        To unlock this file, wait <b>{{AD_TIME}} seconds</b> on the link below.
                    </p>
                    <button id="dlClickBtn" class="btn-submit" style="background: linear-gradient(45deg, #ef4444, #f97316); margin-top: 10px;" onclick="executeDirectLink()">🔗 Click Here (Open Link)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- রেফার ও অন্যান্য মডাল সমূহ -->
    <div id="referModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('referModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <i class="fa-solid fa-share-nodes" style="font-size:50px; color:#38bdf8;"></i>
            <h2 style="margin:12px 0; color:white; font-size: 20px;">Refer & Earn</h2>
            <p style="color:#cbd5e1; font-size:14px; margin-bottom:15px;">Get <b>10 Points</b> for each successful referral!</p>
            <div style="background:#0f172a; padding:12px; border:1px dashed #3b82f6; margin-bottom:15px; word-break:break-all; font-size:13px;" id="refLinkText">...</div>
            <button class="btn-submit" onclick="copyReferLink()">Copy Link</button>
        </div>
    </div>
    
    <div id="watchlistModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('watchlistModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:#38bdf8; font-size: 20px; margin-bottom:15px;"><i class="fa-solid fa-bookmark"></i> My Watchlist</h2>
            <div id="watchlistModalList" class="grid" style="padding:0; max-height: 60vh; overflow-y:auto; gap: 15px;">
                <p style="color: #94a3b8;">Loading watchlist...</p>
            </div>
        </div>
    </div>

    <div id="requestsTrackerModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('requestsTrackerModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:#10b981; font-size: 20px; margin-bottom:10px;"><i class="fa-solid fa-code-pull-request"></i> Movie Request Status</h2>
            <div style="display:flex; gap:8px; margin-bottom: 15px;">
                <input type="text" id="reqTrackerInput" class="search-input" style="border-radius:10px; text-align:left; padding:8px 12px; font-size:14px;" placeholder="Enter Movie/Series name...">
                <button class="btn-submit" style="width: auto; padding:0 15px; font-size:13px;" onclick="submitReqTracker()">Request</button>
            </div>
            <div id="requestsTrackerList" style="text-align: left; display: flex; flex-direction: column; gap: 10px; max-height: 45vh; overflow-y: auto;"></div>
        </div>
    </div>

    <!-- বটম ফিক্সড নেভিগেশন বার -->
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
        <div class="nav-item" id="navProfile" onclick="toggleMenu(event)">
            <i class="fa-solid fa-user"></i>
            <span>Profile</span>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp; tg.expand();
        const DIRECT_LINKS = {{DIRECT_LINKS}};
        const SOCIAL_LINKS = {{SOCIAL_LINKS}};
        const INIT_DATA = tg.initData || "";
        const BOT_UNAME = "{{BOT_USER}}";
        const AD_WAIT_TIME = {{AD_TIME}}; 
        const TMDB_API_KEY = "7dc544d9253bccc3cfecc1c677f69819";
        
        let uid = tg.initDataUnsafe?.user?.id || 0;
        let isUserVip = false;
        let userCoins = 0;
        let loadedMovies = {}; 
        let currentPage = 1; 
        let searchQuery = "";
        let activeCategory = "";
        let autoScrollInterval;
        let activeAds = [];
        
        let currentSelectRating = 0;
        let isCurrentMovieBookmarked = false;
        let currentFileId = null;

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
                
                let firstName = tg.initDataUnsafe?.user?.first_name || 'Guest';
                document.getElementById('menuUname').innerText = firstName;
                document.getElementById('coinDisplay').innerHTML = `<i class="fa-solid fa-gem"></i> ${userCoins}`;
                
                if(isUserVip) {
                    document.getElementById('vipBadge').style.display = 'inline-block';
                    document.getElementById('menuStatus').innerText = '👑 VIP User';
                    document.getElementById('menuStatus').style.color = '#fbbf24';
                }
                document.getElementById('refLinkText').innerText = `https://t.me/${BOT_UNAME}?start=ref_${uid}`;
            } catch(e) {}
        }

        function toggleMenu(e) { 
            e.stopPropagation(); 
            setNavActive(3);
            const m = document.getElementById('dropdownMenu'); 
            m.style.display = m.style.display === 'block' ? 'none' : 'block'; 
        }
        function closeMenu() { document.getElementById('dropdownMenu').style.display = 'none'; }
        
        function goHome() { 
            setNavActive(0);
            closeDetails();
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
            closeDetails();
            closeMenu();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => document.getElementById('searchInput').focus(), 300);
        }

        function openReferModal() { 
            document.getElementById('referModal').style.display = 'flex'; 
            closeMenu(); 
        }
        function copyReferLink() { navigator.clipboard.writeText(document.getElementById('refLinkText').innerText); tg.showAlert("✅ Link Copied!"); }

        function openWatchlistModal() {
            document.getElementById('watchlistModal').style.display = 'flex';
            closeMenu();
            renderWatchlist();
        }

        async function renderWatchlist() {
            try {
                const res = await fetch(`/api/watchlist/list/${uid}`);
                const data = await res.json();
                let html = '';
                if (!data.watchlist || data.watchlist.length === 0) {
                    html = '<p style="color: #cbd5e1; text-align:center; padding: 20px;">Watchlist is empty!</p>';
                } else {
                    data.watchlist.forEach(m => {
                        loadedMovies[m.title] = { _id: m.title, photo_id: m.photo_id, files: m.files, clicks: m.clicks || 0 };
                        html += `
                        <div class="card" onclick="openDetails(this)" data-title="${encodeURIComponent(m.title)}">
                            <div class="post-content">
                                <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                                <div class="ep-badge"><i class="fa-solid fa-bookmark text-yellow-400"></i> Saved</div>
                            </div>
                            <div class="card-footer">
                                <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg"></div>
                                <div class="title-text">${m.title}</div>
                            </div>
                        </div>`;
                    });
                }
                document.getElementById('watchlistModalList').innerHTML = html;
            } catch(e) {}
        }

        async function toggleWatchlist() {
            const title = document.getElementById('detailTitle').innerText;
            let endpoint = isCurrentMovieBookmarked ? '/api/watchlist/remove' : '/api/watchlist/add';
            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, title: title, initData: INIT_DATA })
                });
                const d = await res.json();
                if (d.ok) {
                    isCurrentMovieBookmarked = !isCurrentMovieBookmarked;
                    updateBookmarkButtonUI();
                    tg.showAlert(isCurrentMovieBookmarked ? "💾 Added to Watchlist!" : "❌ Removed from Watchlist!");
                }
            } catch(e) {}
        }

        function updateBookmarkButtonUI() {
            const btn = document.getElementById('detailBookmarkBtn');
            if (isCurrentMovieBookmarked) {
                btn.innerHTML = '<i class="fa-solid fa-bookmark text-yellow-400"></i> Saved';
            } else {
                btn.innerHTML = '<i class="fa-regular fa-bookmark"></i> Save';
            }
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
            
            searchQuery = ""; 
            document.getElementById('searchInput').value = "";
            document.getElementById('trendingWrapper').style.display = cat === "" ? 'block' : 'none';
            loadMovies(1);
        }

        async function loadTrending() {
            try {
                const r = await fetch(`/api/trending?uid=${uid}`);
                const data = await r.json();
                const grid = document.getElementById('trendingGrid');
                if(data.length === 0) return document.getElementById('trendingWrapper').style.display = 'none';
                grid.innerHTML = data.map(m => {
                    loadedMovies[m._id] = m;
                    return `<div class="trending-card" onclick="openDetails(this)" data-title="${encodeURIComponent(m._id)}">
                        <div class="post-content">
                            <div class="top-badge">🔥 TOP</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                            <div class="ep-badge"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="view-badge"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                }).join('');
            } catch(e) {}
        }

        async function loadMovies(page = 1) {
            currentPage = page;
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = "<p style='color:white; text-align:center;'>Loading Movies...</p>";
            try {
                const r = await fetch(`/api/list?page=${currentPage}&q=${encodeURIComponent(searchQuery)}&uid=${uid}&cat=${encodeURIComponent(activeCategory)}`);
                const data = await r.json();
                if(data.movies.length === 0) return grid.innerHTML = `<p style='text-align:center; color:#fbbf24;'>No movies found!</p>`;
                
                let htmlContent = "";
                data.movies.forEach(m => {
                    loadedMovies[m._id] = m;
                    let langBadge = m.badge || "HD";
                    htmlContent += `<div class="card" onclick="openDetails(this)" data-title="${encodeURIComponent(m._id)}">
                        <div class="post-content">
                            <div class="lang-card-badge">${langBadge}</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy" onerror="this.src='https://via.placeholder.com/640x360?text=No+Image'">
                            <div class="ep-badge"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="view-badge"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                });
                grid.innerHTML = htmlContent;
            } catch(e) {}
        }

        /* =========================================================
           🍿 OPEN CINEMATIC MOVIE DETAIL VIEW (TMDB + UNLOCK SYSTEM)
           ========================================================= */
        async function openDetails(element) {
            let title = decodeURIComponent(element.getAttribute('data-title'));
            const movie = loadedMovies[title];
            if (!movie) return;

            document.getElementById('detailTitle').innerText = title;
            document.getElementById('detailHeroBackdrop').src = `/api/image/${movie.photo_id}`;
            document.getElementById('detailPosterThumb').src = `/api/image/${movie.photo_id}`;
            document.getElementById('detailTypeBadge').innerText = movie.files.length > 1 ? "📺 Web Series" : "🎬 Full Movie";
            
            // রেন্ডার ডাউনলোড বাটনসমূহ (আমাদের আনলক আর্কিটেকচার অক্ষুণ্ণ রাখা হয়েছে)
            document.getElementById('detailQualityList').innerHTML = movie.files.map(f => {
                let isFree = f.is_unlocked || isUserVip;
                let icon = isFree ? '<i class="fa-solid fa-paper-plane text-green-400"></i>' : '<i class="fa-solid fa-lock text-red-400"></i>';
                return `<div class="rgb-border-action" onclick="handleQualityClick('${f.id}', ${f.is_unlocked})">
                    <div class="rgb-inner-action">
                        <span><i class="fa-solid fa-download"></i> ${f.quality}</span>
                        ${icon}
                    </div>
                </div>`;
            }).join('');

            // স্ক্রিন শো করানো
            document.getElementById('mainHomeScreen').style.display = 'none';
            document.getElementById('detailScreen').style.display = 'block';
            document.getElementById('detailScreen').scrollTo({ top: 0, behavior: 'instant' });

            // TMDB রিয়েল-টাইম লাইভ ট্রেইলার, কাস্ট এবং সাইনোপসিস লোড করা
            loadTmdbMovieLiveInfo(title);
            
            // রিভিউ এবং বুকমার্ক চেক
            loadReviews(title);
            checkWatchlistState(title);

            // ভিউ কাউন্ট আপডেট
            fetch('/api/view_movie', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({title: title}) }).catch(e=>{});
        }

        function closeDetails() {
            document.getElementById('detailTrailerIframe').src = "";
            document.getElementById('detailScreen').style.display = 'none';
            document.getElementById('mainHomeScreen').style.display = 'block';
        }

        // 🔍 TMDB লাইভ ট্রেইলার, পোস্টার ও কাস্ট ফেচ ফাংশন
        async function loadTmdbMovieLiveInfo(queryTitle) {
            try {
                let cleanTitle = queryTitle.replace(/\[.*?\]|\(.*?\)/g, "").trim();
                let res = await fetch(`https://api.themoviedb.org/3/search/multi?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(cleanTitle)}`);
                let data = await res.json();
                
                if (data.results && data.results.length > 0) {
                    let tmdb = data.results[0];
                    let tmdbId = tmdb.id;
                    let mediaType = tmdb.media_type || "movie";

                    // ১. ওভারভিউ ও রেটিং
                    if (tmdb.overview) document.getElementById('detailOverview').innerText = tmdb.overview;
                    if (tmdb.vote_average) document.getElementById('detailRatingVal').innerText = tmdb.vote_average.toFixed(1);
                    if (tmdb.release_date || tmdb.first_air_date) {
                        document.getElementById('detailYearChip').innerHTML = `<i class="fa-solid fa-calendar"></i> ${(tmdb.release_date || tmdb.first_air_date).split('-')[0]}`;
                    }

                    // ২. বড় ব্যাকড্রপ পিকচার
                    if (tmdb.backdrop_path) {
                        document.getElementById('detailHeroBackdrop').src = `https://image.tmdb.org/t/p/w780${tmdb.backdrop_path}`;
                    }

                    // ৩. অফিশিয়াল ট্রেইলার ও কাস্ট মেম্বারস
                    let dRes = await fetch(`https://api.themoviedb.org/3/${mediaType}/${tmdbId}?api_key=${TMDB_API_KEY}&append_to_response=videos,credits`);
                    let details = await dRes.json();

                    // ট্রেইলার
                    let trailers = details.videos?.results?.filter(v => v.site === "YouTube" && (v.type === "Trailer" || v.type === "Teaser"));
                    if (trailers && trailers.length > 0) {
                        document.getElementById('detailTrailerIframe').src = `https://www.youtube.com/embed/${trailers[0].key}`;
                        document.getElementById('detailTrailerSection').style.display = 'block';
                    } else {
                        document.getElementById('detailTrailerSection').style.display = 'none';
                    }

                    // কাস্ট
                    let cast = details.credits?.cast?.slice(0, 6);
                    if (cast && cast.length > 0) {
                        document.getElementById('detailCastGrid').innerHTML = cast.map(c => `
                            <div class="cast-tile">
                                <img src="${c.profile_path ? 'https://image.tmdb.org/t/p/w185' + c.profile_path : 'https://via.placeholder.com/100'}" alt="${c.name}">
                                <div style="overflow:hidden;">
                                    <div class="cast-tile-name">${c.name}</div>
                                    <div class="cast-tile-char">as ${c.character || 'Actor'}</div>
                                </div>
                            </div>
                        `).join('');
                        document.getElementById('detailCastSection').style.display = 'block';
                    } else {
                        document.getElementById('detailCastSection').style.display = 'none';
                    }
                }
            } catch(e) {}
        }

        function checkWatchlistState(title) {
            fetch(`/api/watchlist/list/${uid}`).then(r => r.json()).then(wl => {
                isCurrentMovieBookmarked = wl.watchlist.some(w => w.title === title);
                updateBookmarkButtonUI();
            }).catch(e => { isCurrentMovieBookmarked = false; updateBookmarkButtonUI(); });
        }

        function handleQualityClick(fileId, isUnlocked) {
            if(isUnlocked || isUserVip) { 
                sendFileAndClose(fileId); 
            } else { 
                currentFileId = fileId; 
                document.getElementById('directLinkModal').style.display = 'flex';
                resetDlButton();
            }
        }

        function resetDlButton() {
            const btn = document.getElementById('dlClickBtn');
            btn.onclick = executeDirectLink;
            btn.innerText = "🔗 Click Here (Open Link) 🚀";
            btn.style.background = "linear-gradient(45deg, #ef4444, #f97316)";
            btn.disabled = false;
        }

        let linkOpenedAt = 0;
        let isWaitingForReturn = false;
        let dlTimerInterval = null;

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

        document.addEventListener("visibilitychange", function() {
            if (document.visibilityState === 'visible' && isWaitingForReturn) {
                isWaitingForReturn = false; 
                clearInterval(dlTimerInterval);
                let elapsedSeconds = (Date.now() - linkOpenedAt) / 1000;
                if (elapsedSeconds < AD_WAIT_TIME - 1) { 
                    tg.showAlert(`⚠️ You must wait full ${AD_WAIT_TIME} seconds on the link.`);
                    resetDlButton();
                } else { 
                    document.getElementById('directLinkModal').style.display = 'none'; 
                    if (currentFileId) sendFileAndClose(currentFileId); 
                }
            }
        });

        async function sendFileAndClose(id) {
            showProcessingUI(); 
            try {
                const res = await fetch('/api/send', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({userId: uid, movieId: id, initData: INIT_DATA}) });
                const data = await res.json();
                if(data.ok) { 
                    setTimeout(() => tg.close(), 600);
                } else {
                    hideProcessingUI();
                    tg.showAlert("⚠️ Session expired! Please close and reopen the mini app.");
                }
            } catch (e) {
                hideProcessingUI();
                tg.showAlert("⚠️ Network error! Please try again.");
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
                    <div style="color:#cbd5e1; margin-top:12px; font-size:14px; font-weight:bold;">Video is being sent to your bot inbox!</div>
                `;
                document.body.appendChild(procModal);
            }
            procModal.style.display = 'flex';
        }
        function hideProcessingUI() {
            let procModal = document.getElementById('processingModalCustom');
            if(procModal) procModal.style.display = 'none';
        }

        function setSelectRating(r) {
            currentSelectRating = r;
            document.querySelectorAll('#starRatingSelect i').forEach((star, index) => {
                star.className = index < r ? "fa-solid fa-star text-yellow-400" : "fa-solid fa-star text-gray-600";
            });
        }

        async function submitReview() {
            const title = document.getElementById('detailTitle').innerText;
            const rText = document.getElementById('reviewText').value.trim();
            const uname = tg.initDataUnsafe?.user?.first_name || 'Guest';

            if (currentSelectRating === 0) { tg.showAlert("Please select a star rating!"); return; }
            if (!rText) { tg.showAlert("Please write a review message!"); return; }

            try {
                const res = await fetch('/api/reviews/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid, uname: uname, title: title, rating: currentSelectRating, review: rText, initData: INIT_DATA })
                });
                const data = await res.json();
                if (data.ok) {
                    tg.showAlert("🎉 Review submitted successfully!");
                    document.getElementById('reviewText').value = '';
                    setSelectRating(0);
                    loadReviews(title);
                }
            } catch(e) {}
        }

        async function loadReviews(title) {
            try {
                const res = await fetch(`/api/reviews/get/${encodeURIComponent(title)}`);
                const data = await res.json();
                let html = '';
                data.reviews.forEach(r => {
                    let starsHtml = '';
                    for(let i=1; i<=5; i++) starsHtml += i <= r.rating ? '<i class="fa-solid fa-star text-yellow-400 text-xs"></i>' : '<i class="fa-solid fa-star text-gray-700 text-xs"></i>';
                    html += `
                    <div style="background: rgba(15, 23, 42, 0.4); padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                        <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
                            <span style="font-weight:bold; font-size:12px; color:#cbd5e1;">${r.uname}</span>
                            <div>${starsHtml}</div>
                        </div>
                        <p style="font-size:12px; color:#94a3b8; line-height:1.4;">${r.review}</p>
                    </div>`;
                });
                document.getElementById('modalReviewsList').innerHTML = html || '<p style="color: #64748b; font-size: 12px;">No reviews yet. Be the first to review!</p>';
            } catch(e) {}
        }

        async function initApp() {
            try {
                await Promise.all([
                    fetchUserInfo(),
                    loadCategories(),
                    loadTrending(),
                    loadMovies(1)
                ]);
            } catch(e) {}
        }
        initApp();
    </script>
</body>
</html>
"""