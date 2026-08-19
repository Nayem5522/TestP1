# html_template.py

HTML_CODE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Prime Flix OTT</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-red: #ff0055;
            --neon-cyan: #00f2ff;
            --neon-green: #00ffa3;
            --neon-yellow: #ffcc00;
            --neon-purple: #7c3aed;
            --bg-dark: #040711;
            --card-bg: #0b1120;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
        body { background: var(--bg-dark); font-family: 'Poppins', sans-serif; color: #fff; overflow-x: hidden; width: 100%; -webkit-overflow-scrolling: touch; padding-bottom: 85px; } 

        /* 🌈 RGB FLOWING ANIMATIONS */
        @keyframes rgbBorderFlow {
            0% { border-color: #ff0055; box-shadow: 0 0 15px rgba(255, 0, 85, 0.4); }
            33% { border-color: #00f2ff; box-shadow: 0 0 15px rgba(0, 242, 255, 0.4); }
            66% { border-color: #00ffa3; box-shadow: 0 0 15px rgba(0, 255, 163, 0.4); }
            100% { border-color: #ff0055; box-shadow: 0 0 15px rgba(255, 0, 85, 0.4); }
        }
        @keyframes spinRing {
            0% { transform: rotate(0deg); filter: hue-rotate(0deg); }
            100% { transform: rotate(360deg); filter: hue-rotate(360deg); }
        }
        @keyframes headerGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* 👑 ULTRA-PREMIUM HEADER */
        header { 
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
            padding: 14px 15px; position: sticky; top: 0; 
            background: rgba(4, 7, 17, 0.92); backdrop-filter: blur(15px); 
            z-index: 1000; width: 100%; gap: 10px;
            border-bottom: 2px solid transparent;
            background-image: linear-gradient(rgba(4, 7, 17, 0.95), rgba(4, 7, 17, 0.95)), 
                              linear-gradient(90deg, #ff0055, #00f2ff, #ffcc00, #00ffa3, #ff0055);
            background-origin: border-box; background-clip: padding-box, border-box;
            background-size: 300% 300%;
            animation: headerGlow 6s linear infinite;
        }
        .header-top-row { display: flex; align-items: center; justify-content: space-between; width: 100%; max-width: 900px; }
        .logo-text { font-family: 'Orbitron', sans-serif; font-size: 22px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; background: linear-gradient(90deg, #00f2ff, #fff, #ff0055); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .home-btn { background: rgba(0, 242, 255, 0.1); color: var(--neon-cyan); border: 1.5px solid var(--neon-cyan); padding: 5px 14px; border-radius: 20px; font-weight: 800; font-size: 11px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }
        .home-btn:active { transform: scale(0.95); }

        /* 📱 BOTTOM NAV */
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(4, 7, 17, 0.96); backdrop-filter: blur(20px); border-top: 1px solid #1e293b; display: flex; justify-content: space-around; align-items: center; padding: 10px 0; z-index: 2000; padding-bottom: calc(10px + env(safe-area-inset-bottom)); }
        .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #94a3b8; font-size: 11px; font-weight: bold; cursor: pointer; transition: 0.2s; width: 25%; gap: 3px; }
        .nav-item i { font-size: 19px; }
        .nav-item.active { color: var(--neon-cyan); text-shadow: 0 0 10px rgba(0, 242, 255, 0.6); }

        /* 🔍 SEARCH */
        .search-box { padding: 15px; }
        .search-input { width: 100%; padding: 15px; border-radius: 25px; border: 1.5px solid #1e293b; outline: none; text-align: center; background: #0c1324; color: #fff; font-size: 16px; font-weight: bold; transition: 0.3s; }
        .search-input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 15px rgba(0, 242, 255, 0.3); }

        /* 🎨 PILL CATEGORIES */
        .category-container { display: flex; overflow-x: auto; flex-wrap: nowrap; gap: 10px; padding: 10px 15px 20px; scroll-behavior: smooth; width: 100%; }
        .category-container::-webkit-scrollbar { display: none; }
        
        .cat-btn { background: #e2e8f0; color: #0f172a; border: none; padding: 9px 20px; border-radius: 30px; font-size: 13px; font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; white-space: nowrap; transition: 0.25s; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .cat-btn:active { transform: scale(0.95); }
        
        /* ✦ FOR YOU BUTTON SPECIAL LOGIC */
        .cat-btn.for-you-btn {
            background: #ffffff !important;
            color: #7c3aed !important;
            box-shadow: 0 0 15px 2px rgba(124, 58, 237, 0.5) !important;
            animation: forYouPulse 2s infinite ease-in-out;
        }
        .cat-btn.for-you-btn.active {
            background: linear-gradient(135deg, #7c3aed, #db2777) !important;
            color: #ffffff !important;
            box-shadow: 0 0 25px 6px rgba(219, 39, 119, 0.8) !important;
        }
        @keyframes forYouPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 10px rgba(124, 58, 237, 0.4); }
            50% { transform: scale(1.03); box-shadow: 0 0 20px rgba(124, 58, 237, 0.8); }
        }

        .cat-btn.active:not(.for-you-btn) {
            background: linear-gradient(135deg, #ff0055, #ff7300) !important;
            color: #fff !important;
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.6);
        }

        /* 🎬 MOVIE CARD & DISSOLVE/TYPING LANGUAGE BADGE */
        .grid { padding: 0 15px 20px; display: flex; flex-direction: column; gap: 18px; }
        .card { background: transparent; cursor: pointer; }
        .post-content { position: relative; padding: 2.5px; border-radius: 14px; background: linear-gradient(45deg, #ff0055, #00f2ff, #00ffa3, #ffcc00, #ff0055); background-size: 250%; animation: headerGlow 6s linear infinite; }
        .post-content img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; border-radius: 12px; }

        /* 🏷️ DISSOLVING TYPING BADGE (TOP-LEFT) */
        .badge-top-left {
            position: absolute; top: 10px; left: 10px;
            background: linear-gradient(135deg, rgba(255,0,85,0.9), rgba(180,0,50,0.95));
            color: #fff; font-size: 10.5px; font-weight: 900;
            padding: 4px 10px; border-radius: 6px; z-index: 10;
            text-transform: uppercase; letter-spacing: 0.5px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.2);
            min-width: 60px; text-align: center;
        }

        /* 🏷️ TOP-RIGHT BADGE (FILES COUNT) */
        .badge-top-right {
            position: absolute; top: 10px; right: 10px;
            background: rgba(16, 185, 129, 0.9);
            color: #fff; font-size: 10.5px; font-weight: 800;
            padding: 4px 8px; border-radius: 6px; z-index: 10;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }

        /* 🏷️ BOTTOM-RIGHT BADGE (QUALITY) */
        .badge-bottom-right {
            position: absolute; bottom: 10px; right: 10px;
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: #fff; font-size: 10px; font-weight: 900;
            padding: 3px 8px; border-radius: 6px; z-index: 10;
            text-transform: uppercase;
        }

        /* 🏷️ BOTTOM-LEFT BADGE (VIEWS) */
        .badge-bottom-left {
            position: absolute; bottom: 10px; left: 10px;
            background: rgba(0,0,0,0.75); color: #cbd5e1;
            font-size: 10px; font-weight: 700; padding: 3px 8px;
            border-radius: 6px; z-index: 10;
        }

        .card-footer { padding: 10px 4px 0; display: flex; align-items: center; gap: 12px; }
        .channel-logo { width: 38px; height: 38px; border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden; }
        .channel-logo::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: conic-gradient(#ff0055, #00f2ff, #ffcc00, #00ffa3, #ff0055); animation: spinRing 4s linear infinite; }
        .channel-logo img { width: calc(100% - 4px); height: calc(100% - 4px); object-fit: cover; border-radius: 50%; position: relative; z-index: 2; }
        .title-text { color: #fff; font-size: 15px; font-weight: 700; line-height: 1.3; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

        /* 🔥 TRENDING HORIZONTAL */
        .trending-container { display: flex; overflow-x: auto; gap: 15px; padding: 0 15px 15px; scroll-behavior: smooth; }
        .trending-container::-webkit-scrollbar { display: none; }
        .trending-card { min-width: 275px; max-width: 275px; flex-shrink: 0; cursor: pointer; }

        /* =========================================================
           🍿 CINEMATIC FULL SCREEN MOVIE DETAIL VIEW (TMDB SYNC)
           ========================================================= */
        #detailScreen {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #040711; z-index: 4000; overflow-y: auto; padding-bottom: 90px;
            animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes slideIn { 0% { transform: translateX(100%); } 100% { transform: translateX(0); } }

        .detail-top-nav {
            position: sticky; top: 0; background: rgba(4, 7, 17, 0.9);
            backdrop-filter: blur(15px); padding: 12px 15px;
            display: flex; align-items: center; justify-content: space-between;
            z-index: 50; border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .back-nav-btn {
            background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff; padding: 7px 16px; border-radius: 30px; font-size: 12.5px; font-weight: 700;
            cursor: pointer; display: flex; align-items: center; gap: 6px;
        }

        .hero-banner-wrap { position: relative; width: 100%; aspect-ratio: 16/9; background: #000; overflow: hidden; }
        .hero-banner-img { width: 100%; height: 100%; object-fit: cover; }
        .hero-banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, transparent 30%, rgba(4, 7, 17, 0.98) 100%); }

        .poster-meta-dock { display: flex; gap: 14px; padding: 0 15px; margin-top: -65px; position: relative; z-index: 10; }
        .dock-poster-card { width: 105px; aspect-ratio: 2/3; border-radius: 12px; overflow: hidden; border: 2px solid rgba(255,255,255,0.25); box-shadow: 0 10px 25px rgba(0,0,0,0.9); flex-shrink: 0; background: #0b1120; }
        .dock-poster-card img { width: 100%; height: 100%; object-fit: cover; }
        
        .dock-title-info { display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 4px; }
        .detail-movie-title { font-size: 20px; font-weight: 900; line-height: 1.25; color: #fff; margin-bottom: 4px; }

        .badge-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 15px 0; }
        .chip { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; display: inline-flex; align-items: center; gap: 5px; }
        .chip-rating { background: rgba(245, 197, 24, 0.15); color: #fbbf24; border: 1px solid rgba(245, 197, 24, 0.4); }
        .chip-type { background: rgba(0, 242, 255, 0.15); color: var(--neon-cyan); border: 1px solid var(--neon-cyan); }
        .chip-lang { background: rgba(0, 255, 163, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }

        /* 🌈 RGB DOWNLOAD GATEWAY BOX */
        .gateway-hub-card {
            margin: 20px 0; background: #0b1120; border-radius: 18px; padding: 20px 15px;
            border: 2px solid transparent;
            background-image: linear-gradient(#0b1120, #0b1120), 
                              linear-gradient(135deg, #ff0055, #00f2ff, #00ffa3);
            background-origin: border-box; background-clip: padding-box, border-box;
            box-shadow: 0 10px 30px rgba(0, 242, 255, 0.15); text-align: center;
        }
        .rgb-border-action {
            position: relative; background: linear-gradient(45deg, #ff0055, #00f2ff, #00ffa3, #ffcc00, #ff0055);
            background-size: 200%; padding: 2.5px; border-radius: 12px; margin-bottom: 10px; cursor: pointer; width: 100%;
        }
        .rgb-inner-action { display: flex; justify-content: space-between; align-items: center; background: #040711; padding: 14px 16px; border-radius: 10px; color: white; font-weight: 800; font-size: 15px; }

        .cast-tile-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
        .cast-tile { background: rgba(19, 25, 43, 0.7); padding: 8px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 10px; }
        .cast-tile img { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; border: 2px solid var(--neon-cyan); }
        .cast-tile-name { font-size: 12px; font-weight: bold; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .cast-tile-char { font-size: 10px; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* 🍿 SUGGESTION CARDS */
        .suggest-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 10px; }
        .suggest-card { background: #0b1120; border-radius: 10px; overflow: hidden; border: 1px solid #1e293b; cursor: pointer; }
        .suggest-card img { width: 100%; aspect-ratio: 16/9; object-fit: cover; }
        .suggest-title { padding: 8px; font-size: 12px; font-weight: bold; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* MODAL */
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: none; align-items: center; justify-content: center; z-index: 5000; backdrop-filter: blur(5px); }
        .modal-content { background: #0b1120; width: 90%; max-width: 380px; padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #1e293b; position: relative; }
        .close-icon { position: absolute; top: 12px; right: 15px; width: 30px; height: 30px; border-radius: 50%; background: #1e293b; color: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; }
        .btn-submit { background: linear-gradient(45deg, #ff0055, #ff7300); color: white; border: none; padding: 14px 20px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 15px; cursor: pointer; }

        .spinner-new { width: 60px; height: 60px; border: 4px solid rgba(255,255,255,0.1); border-left-color: var(--neon-cyan); border-radius: 50%; animation: spinRing 1s linear infinite; margin: 0 auto 15px; }
        .big-processing-text { font-size: 22px; font-weight: 900; color: var(--neon-cyan); }
    </style>
</head>
<body onclick="closeMenu(event)">

    <!-- হেডার -->
    <header>
        <div class="header-top-row">
            <div class="logo-text">𝑷𝑹𝑰𝑴𝑬 𝑪𝑰𝑵𝑬𝑭𝑳𝑰𝑿</div>
            <button onclick="goHome()" class="home-btn"><i class="fa-solid fa-house"></i> Home</button>
        </div>
    </header>

    <!-- প্রোফাইল ড্রপডাউন -->
    <div id="dropdownMenu" class="dropdown-menu" style="display:none; position:fixed; bottom:85px; right:15px; background:#0b1120; border:1px solid #1e293b; border-radius:12px; padding:15px; z-index:2000; width:220px;">
        <div style="font-weight:bold; font-size:14px; color:#fff;" id="menuUname">Guest</div>
        <div style="font-size:12px; color:#38bdf8; margin: 5px 0 10px;" id="menuStatus">Free User</div>
        <a onclick="openReferModal()" style="display:block; color:#fff; font-size:13px; margin-bottom:8px; cursor:pointer;"><i class="fa-solid fa-share-nodes text-blue-400"></i> Refer & Earn</a>
        <a onclick="openWatchlistModal()" style="display:block; color:#fff; font-size:13px; cursor:pointer;"><i class="fa-solid fa-bookmark text-yellow-400"></i> My Watchlist</a>
    </div>

    <!-- মেইন হোম স্ক্রিন -->
    <div id="mainHomeScreen">
        <div class="search-box">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search Movies or Series...">
        </div>

        <div id="categoryBox" class="category-container"></div>

        <div id="trendingWrapper">
            <div style="padding: 5px 15px 12px; font-size: 18px; font-weight: 900; display: flex; align-items: center; gap: 6px; color:#ff4e2a;">
                <i class="fa-solid fa-fire"></i> Trending Worldwide
            </div>
            <div class="trending-container" id="trendingGrid"></div>
        </div>

        <div style="padding: 10px 15px 12px; font-size: 18px; font-weight: 900; display: flex; align-items: center; gap: 6px; color:#38bdf8;" id="recentTitle">
            <i class="fa-solid fa-clock-rotate-left"></i> Recently Added
        </div>
        <div class="grid" id="movieGrid"></div>
    </div>

    <!-- =========================================================
         🍿 CINEMATIC FULL SCREEN MOVIE DETAIL VIEW
         ========================================================= -->
    <div id="detailScreen">
        <div class="detail-top-nav">
            <button onclick="closeDetails()" class="back-nav-btn"><i class="fa-solid fa-arrow-left"></i> Back</button>
            <button id="detailBookmarkBtn" onclick="toggleWatchlist()" class="back-nav-btn" style="border-color: #f59e0b; color: #fbbf24;"><i class="fa-regular fa-bookmark"></i> Save</button>
        </div>

        <!-- হিরো ব্যানার (আমাদের ব্যাকএন্ডের দেয়া ১৬:৯ থাম্বনেইল) -->
        <div class="hero-banner-wrap">
            <img id="detailHeroBackdrop" src="" class="hero-banner-img">
            <div class="hero-banner-overlay"></div>
        </div>

        <!-- ডক পোস্টার (TMDB থেকে ফেচ করা আসল লম্বা পোস্টার) -->
        <div class="poster-meta-dock">
            <div class="dock-poster-card">
                <img id="detailTmdbPortrait" src="" alt="Poster">
            </div>
            <div class="dock-title-info">
                <h1 id="detailTitle" class="detail-movie-title">Movie Title</h1>
                <div style="font-size: 12px; color: var(--neon-cyan); font-weight: 800;" id="detailTypeBadge">🎬 Movie</div>
            </div>
        </div>

        <div style="padding: 15px;">
            <!-- চিপস ব্যাজ -->
            <div class="badge-chips">
                <span class="chip chip-rating"><i class="fa-solid fa-star"></i> <span id="detailRatingVal">N/A</span>/10</span>
                <span class="chip chip-type" id="detailTypeChip">🎬 Full Movie</span>
                <span class="chip chip-lang" id="detailLangChip">Dual Audio</span>
            </div>

            <!-- স্টোরিলাইন / সিনোপসিস -->
            <div style="background: rgba(15, 23, 42, 0.7); padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 20px;">
                <h3 style="font-size: 14px; font-weight: 800; color: #cbd5e1; margin-bottom: 6px;"><i class="fa-solid fa-align-left text-blue-400"></i> Storyline / Overview</h3>
                <p id="detailOverview" style="font-size: 13px; color: #94a3b8; line-height: 1.6;">Loading storyline from TMDB...</p>
            </div>

            <!-- ডাউনলোড ও স্ট্রিম গেটওয়ে (আমাদের আসল আনলক সিস্টেম) -->
            <div class="gateway-hub-card">
                <h2 style="font-size: 17px; font-weight: 900; color: #fff; margin-bottom: 6px; font-family:'Orbitron', sans-serif;">
                    <i class="fa-solid fa-magnet" style="color: #ff0055;"></i> Ultra High-Speed Links
                </h2>
                <p style="font-size: 12px; color: #cbd5e1; line-height: 1.4; margin-bottom: 15px;">
                    Select your preferred quality below to unlock high-speed stream or direct bot delivery.
                </p>
                <div id="detailQualityList" style="display: flex; flex-direction: column; gap: 8px;"></div>
            </div>

            <!-- VLC নোটিশ বক্স -->
            <div style="background: #080d1a; border: 1.5px solid rgba(0, 242, 255, 0.2); border-radius: 14px; padding: 14px; margin: 20px 0; text-align: center;">
                <h4 style="color: #ffeb3b; font-size: 13.5px; font-weight: bold; margin-bottom: 6px;">
                    🎬 ভিডিওতে সাউন্ড না আসলে 🔊
                </h4>
                <p style="color: #cbd5e1; font-size: 12px; line-height: 1.4; margin-bottom: 10px;">
                    👉 <b>VLC Player</b> দিয়ে প্লে করে অডিও ট্র্যাক পরিবর্তন করুন, সাউন্ড চলে আসবে!
                </p>
                <a href="https://play.google.com/store/apps/details?id=org.videolan.vlc" target="_blank" class="home-btn" style="display:inline-flex; border-color: #00f2ff; color:#00f2ff;"><i class="fa-brands fa-google-play"></i> Get VLC Player</a>
            </div>

            <!-- ট্রেইলার সেকশন -->
            <div id="detailTrailerSection" style="margin: 25px 0; display: none;">
                <h3 style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 10px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-circle-play text-red-500"></i> Official Trailer
                </h3>
                <div style="position: relative; width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 12px; overflow: hidden; border: 1.5px solid rgba(255,255,255,0.1);">
                    <iframe id="detailTrailerIframe" src="" style="width: 100%; height: 100%; border: none;" allowfullscreen></iframe>
                </div>
            </div>

            <!-- কাস্ট গ্রিড -->
            <div id="detailCastSection" style="margin: 25px 0; display: none;">
                <h3 style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-user-group text-blue-400"></i> Top Star Cast
                </h3>
                <div class="cast-tile-grid" id="detailCastGrid"></div>
            </div>

            <!-- সাজেস্টেড মুভি সেকশন (You Might Also Like) -->
            <div style="margin-top: 30px;">
                <h3 style="font-size: 15px; font-weight: 800; color: #fff; margin-bottom: 8px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-film text-purple-400"></i> You Might Also Like
                </h3>
                <div class="suggest-grid" id="detailSuggestGrid"></div>
            </div>
        </div>
    </div>

    <!-- আনলক অ্যাড মডাল -->
    <div id="directLinkModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('directLinkModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color: #00ffa3; font-size: 20px; font-weight: 900; margin-bottom: 10px;"><i class="fa-solid fa-unlock-keyhole"></i> Unlock Video</h2>
            <p style="color: #cbd5e1; font-size: 13.5px; margin-bottom: 15px;">
                To unlock this file, please wait <b>{{AD_TIME}} seconds</b> on the opened link.
            </p>
            <button id="dlClickBtn" class="btn-submit" onclick="executeDirectLink()">🔗 Open Link & Unlock</button>
        </div>
    </div>

    <!-- রেফার মডাল -->
    <div id="referModal" class="modal">
        <div class="modal-content">
            <div class="close-icon" onclick="document.getElementById('referModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <i class="fa-solid fa-share-nodes" style="font-size:45px; color:var(--neon-cyan);"></i>
            <h2 style="margin:10px 0; color:white; font-size: 18px;">Refer & Earn</h2>
            <p style="color:#cbd5e1; font-size:13px; margin-bottom:12px;">Get <b>10 Points</b> for each referral!</p>
            <div style="background:#040711; padding:10px; border:1px dashed var(--neon-cyan); margin-bottom:15px; word-break:break-all; font-size:12px;" id="refLinkText">...</div>
            <button class="btn-submit" onclick="copyReferLink()">Copy Invitation Link</button>
        </div>
    </div>

    <!-- ওয়াচলিস্ট মডাল -->
    <div id="watchlistModal" class="modal">
        <div class="modal-content" style="max-width:420px;">
            <div class="close-icon" onclick="document.getElementById('watchlistModal').style.display='none'"><i class="fa-solid fa-xmark"></i></div>
            <h2 style="color:var(--neon-cyan); font-size: 18px; margin-bottom:15px;"><i class="fa-solid fa-bookmark"></i> My Watchlist</h2>
            <div id="watchlistModalList" class="grid" style="padding:0; max-height: 55vh; overflow-y:auto;"></div>
        </div>
    </div>

    <!-- বটম নেভ -->
    <div class="bottom-nav">
        <div class="nav-item active" onclick="goHome()"><i class="fa-solid fa-house"></i><span>Home</span></div>
        <div class="nav-item" onclick="focusSearch()"><i class="fa-solid fa-magnifying-glass"></i><span>Search</span></div>
        <div class="nav-item" onclick="window.location.href='/upcoming'"><i class="fa-solid fa-calendar-days"></i><span>Upcoming</span></div>
        <div class="nav-item" onclick="toggleMenu(event)"><i class="fa-solid fa-user"></i><span>Profile</span></div>
    </div>

    <script>
        let tg = window.Telegram.WebApp; tg.expand();
        const DIRECT_LINKS = {{DIRECT_LINKS}};
        const INIT_DATA = tg.initData || "";
        const BOT_UNAME = "{{BOT_USER}}";
        const AD_WAIT_TIME = {{AD_TIME}}; 
        const TMDB_API_KEY = "7dc544d9253bccc3cfecc1c677f69819";
        
        let uid = tg.initDataUnsafe?.user?.id || 0;
        let isUserVip = false;
        let loadedMovies = {}; 
        let allMoviesList = [];
        let searchQuery = "";
        let activeCategory = "";
        let autoScrollInterval;
        let currentFileId = null;
        let isCurrentMovieBookmarked = false;

        /* 🌈 DISSOLVING TYPING BADGE LOOP */
        function startTypingBadgeLoop() {
            setInterval(() => {
                document.querySelectorAll('.badge-top-left').forEach(badge => {
                    const fullText = badge.getAttribute('data-full-text') || badge.innerText;
                    badge.setAttribute('data-full-text', fullText);
                    
                    // ডিসলভিং / মুছে ফেলা
                    let len = fullText.length;
                    let eraseTimer = setInterval(() => {
                        len--;
                        badge.innerText = fullText.substring(0, len);
                        if(len <= 0) {
                            clearInterval(eraseTimer);
                            // আবার টাইপ হয়ে আসা
                            let typeIdx = 0;
                            let typeTimer = setInterval(() => {
                                typeIdx++;
                                badge.innerText = fullText.substring(0, typeIdx);
                                if(typeIdx >= fullText.length) clearInterval(typeTimer);
                            }, 80);
                        }
                    }, 50);
                });
            }, 6000);
        }

        async function fetchUserInfo() {
            try {
                const res = await fetch('/api/user/' + uid);
                const data = await res.json();
                isUserVip = data.vip;
                let firstName = tg.initDataUnsafe?.user?.first_name || 'Guest';
                document.getElementById('menuUname').innerText = firstName;
                if(isUserVip) {
                    document.getElementById('menuStatus').innerText = '👑 VIP Member';
                    document.getElementById('menuStatus').style.color = '#fbbf24';
                }
                document.getElementById('refLinkText').innerText = `https://t.me/${BOT_UNAME}?start=ref_${uid}`;
            } catch(e) {}
        }

        function toggleMenu(e) { e.stopPropagation(); const m = document.getElementById('dropdownMenu'); m.style.display = m.style.display === 'block' ? 'none' : 'block'; }
        function closeMenu() { document.getElementById('dropdownMenu').style.display = 'none'; }
        
        function goHome() { 
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
            closeDetails();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            setTimeout(() => document.getElementById('searchInput').focus(), 300);
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
                    html = '<p style="color: #cbd5e1; text-align:center; padding: 20px;">Watchlist is empty!</p>';
                } else {
                    data.watchlist.forEach(m => {
                        loadedMovies[m.title] = { _id: m.title, photo_id: m.photo_id, files: m.files, clicks: m.clicks || 0 };
                        html += `
                        <div class="card" onclick="openDetails(this)" data-title="${encodeURIComponent(m.title)}">
                            <div class="post-content">
                                <img src="/api/image/${m.photo_id}">
                                <div class="badge-top-right">Saved</div>
                            </div>
                            <div class="card-footer">
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
                    document.getElementById('detailBookmarkBtn').innerHTML = isCurrentMovieBookmarked ? '<i class="fa-solid fa-bookmark text-yellow-400"></i> Saved' : '<i class="fa-regular fa-bookmark"></i> Save';
                    tg.showAlert(isCurrentMovieBookmarked ? "💾 Added to Watchlist!" : "❌ Removed from Watchlist!");
                }
            } catch(e) {}
        }

        function formatViews(n) { if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'; if (n >= 1000) return (n / 1000).toFixed(1) + 'K'; return n; }

        /* 🏷️ ডাইনামিক ল্যাঙ্গুয়েজ স্ক্যানার */
        function detectLanguage(title) {
            let t = title.toLowerCase();
            if (t.includes("bangla dubbed") || t.includes("বাংলা ডাবিং")) return "Bangla Dub";
            if (t.includes("hindi dubbed") || t.includes("হিন্দি ডাবিং")) return "Hindi Dub";
            if (t.includes("dual") || t.includes("ডুয়েল") || t.includes("multi")) return "Dual Audio";
            if (t.includes("bangla") || t.includes("বাংলা")) return "Bangla";
            if (t.includes("hindi") || t.includes("হিন্দি")) return "Hindi";
            if (t.includes("english") || t.includes("eng")) return "English";
            if (t.includes("korean") || t.includes("কোরিয়ান")) return "Korean";
            if (t.includes("tamil") || t.includes("তামিল")) return "Tamil";
            if (t.includes("telugu") || t.includes("তেলেগু")) return "Telugu";
            return "HD Movie";
        }

        /* 🎬 পারফেক্ট মুভি বনাম ওয়েব সিরিজ ডিটেকশন */
        function isWebSeries(movie) {
            let t = (movie._id || "").toLowerCase();
            let isSeriesTitle = t.includes("season") || t.includes("s0") || t.includes("ep") || t.includes("episode") || t.includes("part");
            let isSeriesFiles = movie.files && movie.files.some(f => {
                let q = (f.quality || "").toLowerCase();
                return q.includes("ep") || q.includes("s0") || q.includes("season") || q.includes("part");
            });
            return isSeriesTitle || isSeriesFiles || (movie.files && movie.files.length > 2);
        }

        async function loadCategories() {
            try {
                const res = await fetch('/api/categories');
                const cats = await res.json();
                if(cats.length === 0) return;
                
                let html = '';
                cats.forEach((c, idx) => {
                    let catQuery = c.name === "Latest" ? "" : c.name.replace(/'/g, "\\'");
                    let isForYou = (c.name === "For You");
                    let btnClass = "cat-btn" + (idx === 0 ? " active" : "") + (isForYou ? " for-you-btn" : "");
                    let iconColor = c.name === "Trending" ? "color:#ff4e2a;" : c.name === "Latest" ? "color:#0284c7;" : "color:#00ffa3;";
                    let iconHtml = isForYou ? `<span style="color:#7c3aed; font-size:16px;">✦</span>` : `<i class="${c.icon || 'fa-solid fa-film'}" style="${iconColor}"></i>`;
                    html += `<button class="${btnClass}" onclick="setCategory('${catQuery}', this, '${c.name}')"><span>${iconHtml} ${c.name}</span></button>`;
                });
                document.getElementById('categoryBox').innerHTML = html;
            } catch(e) {}
        }

        function setCategory(cat, btn, catName) {
            activeCategory = cat;
            document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            searchQuery = ""; 
            document.getElementById('searchInput').value = "";
            document.getElementById('trendingWrapper').style.display = cat === "" ? 'block' : 'none';
            loadMovies(1);
        }

        /* 🔄 অটো-স্ক্রোল ট্রেন্ডিং */
        function startAutoScrollTrending() {
            if(autoScrollInterval) clearInterval(autoScrollInterval);
            autoScrollInterval = setInterval(() => {
                let grid = document.getElementById('trendingGrid');
                if(grid) {
                    if (grid.scrollLeft >= (grid.scrollWidth - grid.clientWidth - 10)) grid.scrollTo({ left: 0, behavior: 'smooth' });
                    else grid.scrollBy({ left: 285, behavior: 'smooth' });
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
                    let lang = detectLanguage(m._id);
                    let quality = m.files && m.files.length > 0 ? m.files[0].quality : "HD";
                    return `<div class="trending-card" onclick="openDetails(this)" data-title="${encodeURIComponent(m._id)}">
                        <div class="post-content">
                            <div class="badge-top-left">${lang}</div>
                            <div class="badge-top-right"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="badge-bottom-right">${quality}</div>
                            <div class="badge-bottom-left"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy">
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                }).join('');
                startAutoScrollTrending();
            } catch(e) {}
        }

        async function loadMovies(page = 1) {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = "<p style='color:white; text-align:center; padding:20px;'>Loading Blockbusters...</p>";
            try {
                const r = await fetch(`/api/list?page=${page}&q=${encodeURIComponent(searchQuery)}&uid=${uid}&cat=${encodeURIComponent(activeCategory)}`);
                const data = await r.json();
                if(data.movies.length === 0) return grid.innerHTML = `<p style='text-align:center; color:#fbbf24; padding:30px;'>No movies found!</p>`;
                
                allMoviesList = data.movies;
                let htmlContent = "";
                data.movies.forEach(m => {
                    loadedMovies[m._id] = m;
                    let lang = m.badge || detectLanguage(m._id);
                    let quality = m.files && m.files.length > 0 ? m.files[0].quality : "HD";
                    htmlContent += `<div class="card" onclick="openDetails(this)" data-title="${encodeURIComponent(m._id)}">
                        <div class="post-content">
                            <div class="badge-top-left">${lang}</div>
                            <div class="badge-top-right"><i class="fa-solid fa-list"></i> ${m.files.length}</div>
                            <div class="badge-bottom-right">${quality}</div>
                            <div class="badge-bottom-left"><i class="fa-solid fa-eye"></i> ${formatViews(m.clicks)}</div>
                            <img src="/api/image/${m.photo_id}" loading="lazy">
                        </div>
                        <div class="card-footer">
                            <div class="channel-logo"><img src="https://i.ibb.co/XHhKLn7/photo-2026-06-23-19-29-46-7654675389934993448.jpg"></div>
                            <div class="title-text">${m._id}</div>
                        </div>
                    </div>`;
                });
                grid.innerHTML = htmlContent;
                startTypingBadgeLoop();
            } catch(e) {}
        }

        /* =========================================================
           🍿 OPEN CINEMATIC MOVIE DETAIL VIEW (TMDB SYNC)
           ========================================================= */
        async function openDetails(element) {
            let title = decodeURIComponent(element.getAttribute('data-title'));
            const movie = loadedMovies[title];
            if (!movie) return;

            // ১. ব্যাকএন্ডের দেয়া ১৬:৯ থাম্বনেইল হিরো ব্যানারে সেট হবে
            document.getElementById('detailTitle').innerText = title;
            document.getElementById('detailHeroBackdrop').src = `/api/image/${movie.photo_id}`;
            document.getElementById('detailTmdbPortrait').src = `/api/image/${movie.photo_id}`;

            // ২. নির্ভুল মুভি বনাম সিরিজ যাচাই
            let isSeries = isWebSeries(movie);
            let typeLabel = isSeries ? "📺 Web-Series" : "🎬 Full Movie";
            document.getElementById('detailTypeBadge').innerText = typeLabel;
            document.getElementById('detailTypeChip').innerText = typeLabel;
            document.getElementById('detailLangChip').innerText = detectLanguage(title);

            // ৩. ডাউনলোড গেটওয়ে লিংক লিস্ট (আমাদের আসল আনলক আর্কিটেকচার)
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

            // ভিউ স্ক্রিন চেঞ্জ
            document.getElementById('mainHomeScreen').style.display = 'none';
            document.getElementById('detailScreen').style.display = 'block';
            document.getElementById('detailScreen').scrollTo({ top: 0, behavior: 'instant' });

            // ৪. রিয়েল-টাইম TMDB ট্রেইলার, পোর্ট্রেট পোস্টার ও কাস্ট লোড
            loadTmdbMovieLiveInfo(title);

            // ৫. সাজেস্টেড মুভি লোড
            renderSuggestions(title);

            // ভিউ কাউন্ট
            fetch('/api/view_movie', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({title: title}) }).catch(e=>{});
        }

        function closeDetails() {
            document.getElementById('detailTrailerIframe').src = "";
            document.getElementById('detailScreen').style.display = 'none';
            document.getElementById('mainHomeScreen').style.display = 'block';
        }

        /* 🔍 TMDB লাইভ ট্রেইলার, খাড়া পোর্ট্রেট পোস্টার ও কাস্ট ফেচ */
        async function loadTmdbMovieLiveInfo(queryTitle) {
            try {
                let cleanTitle = queryTitle.replace(/\[.*?\]|\(.*?\)|1080p|720p|480p|hd|rip|web/gi, "").trim();
                let res = await fetch(`https://api.themoviedb.org/3/search/multi?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(cleanTitle)}`);
                let data = await res.json();
                
                if (data.results && data.results.length > 0) {
                    let tmdb = data.results[0];
                    let tmdbId = tmdb.id;
                    let mediaType = tmdb.media_type || (tmdb.first_air_date ? "tv" : "movie");

                    // আসল খাড়া ২:৩ পোস্টার সেট করা
                    if (tmdb.poster_path) {
                        document.getElementById('detailTmdbPortrait').src = `https://image.tmdb.org/t/p/w500${tmdb.poster_path}`;
                    }
                    if (tmdb.overview) document.getElementById('detailOverview').innerText = tmdb.overview;
                    if (tmdb.vote_average) document.getElementById('detailRatingVal').innerText = tmdb.vote_average.toFixed(1);

                    // ট্রেইলার ও কাস্ট
                    let dRes = await fetch(`https://api.themoviedb.org/3/${mediaType}/${tmdbId}?api_key=${TMDB_API_KEY}&append_to_response=videos,credits`);
                    let details = await dRes.json();

                    let trailers = details.videos?.results?.filter(v => v.site === "YouTube" && (v.type === "Trailer" || v.type === "Teaser"));
                    if (trailers && trailers.length > 0) {
                        document.getElementById('detailTrailerIframe').src = `https://www.youtube.com/embed/${trailers[0].key}`;
                        document.getElementById('detailTrailerSection').style.display = 'block';
                    } else {
                        document.getElementById('detailTrailerSection').style.display = 'none';
                    }

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

        /* 🍿 রেন্ডার সাজেস্টেড মুভি */
        function renderSuggestions(currentTitle) {
            let suggestions = allMoviesList.filter(m => m._id !== currentTitle).slice(0, 6);
            if (suggestions.length > 0) {
                document.getElementById('detailSuggestGrid').innerHTML = suggestions.map(m => `
                    <div class="suggest-card" onclick="openDetails(this)" data-title="${encodeURIComponent(m._id)}">
                        <img src="/api/image/${m.photo_id}">
                        <div class="suggest-title">${m._id}</div>
                    </div>
                `).join('');
            }
        }

        /* 🚀 ডাউনলোড লিংক হ্যান্ডলার (আমাদের আসল আনলক আর্কিটেকচার) */
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
            btn.innerText = "🔗 Open Link & Unlock";
            btn.disabled = false;
        }

        let linkOpenedAt = 0;
        let isWaitingForReturn = false;

        function executeDirectLink() {
            if (!DIRECT_LINKS || DIRECT_LINKS.length === 0) { 
                document.getElementById('directLinkModal').style.display = 'none'; 
                if (currentFileId) sendFileAndClose(currentFileId); 
                return; 
            }
            tg.openLink(DIRECT_LINKS[Math.floor(Math.random() * DIRECT_LINKS.length)]);
            linkOpenedAt = Date.now(); 
            isWaitingForReturn = true;
            document.getElementById('dlClickBtn').disabled = true;
            document.getElementById('dlClickBtn').innerText = `⏳ Please wait ${AD_WAIT_TIME}s...`;
        }

        document.addEventListener("visibilitychange", function() {
            if (document.visibilityState === 'visible' && isWaitingForReturn) {
                isWaitingForReturn = false; 
                let elapsed = (Date.now() - linkOpenedAt) / 1000;
                if (elapsed < AD_WAIT_TIME - 1) { 
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
                if(data.ok) { setTimeout(() => tg.close(), 600); }
                else { hideProcessingUI(); tg.showAlert("⚠️ Session expired! Reopen app."); }
            } catch (e) { hideProcessingUI(); tg.showAlert("⚠️ Network error!"); }
        }

        function showProcessingUI() {
            let procModal = document.getElementById('processingModalCustom');
            if(!procModal) {
                procModal = document.createElement('div');
                procModal.id = 'processingModalCustom';
                procModal.style.cssText = 'position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:9999; display:flex; align-items:center; justify-content:center; flex-direction:column; backdrop-filter: blur(5px);';
                procModal.innerHTML = `<div class="spinner-new"></div><div class="big-processing-text">Sending File...</div><div style="color:#cbd5e1; margin-top:10px;">Check your bot inbox!</div>`;
                document.body.appendChild(procModal);
            }
            procModal.style.display = 'flex';
        }
        function hideProcessingUI() { let p = document.getElementById('processingModalCustom'); if(p) p.style.display = 'none'; }

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