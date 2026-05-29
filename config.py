# ============================================================
# config.py — API Anahtarları, Sabitler ve Uygulama Parametreleri
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================

# ──────────────────────────────────────────────────────────────
# API ANAHTARLARI — Çalıştırmadan önce kendi anahtarlarınızla değiştirin
# ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = ""
LASTFM_API_KEY = ""

# ──────────────────────────────────────────────────────────────
# Last.fm API
# ──────────────────────────────────────────────────────────────
LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# ──────────────────────────────────────────────────────────────
# Albüm Oluşturma Parametreleri (AOP)
# ──────────────────────────────────────────────────────────────
GENRES = [
    "Pop",
    "Rock",
    "Hip-Hop / Rap",
    "Electronic",
    "Indie",
    "R&B / Soul",
    "Jazz",
    "Metal",
    "Türk Pop",
    "Klasik",
]

ERAS = [
    "1970s",
    "1980s",
    "1990s",
    "2000s",
    "2010s",
    "2020s",
]

DEFAULT_GENRE = "Pop"
DEFAULT_ERA = "2020s"
DEFAULT_TRACK_COUNT = 8
MIN_TRACK_COUNT = 6
MAX_TRACK_COUNT = 14

# ──────────────────────────────────────────────────────────────
# Türe özel görsel stil açıklamaları (kapak görseli istemi için)
# Albüm kapak görseli Pollinations.ai ile oluşturulurken
# Gemini'nin kapak istemine bu açıklamalar eklenir
# ──────────────────────────────────────────────────────────────
GENRE_VISUAL_STYLES = {
    "Pop":          "vibrant neon colors, glossy, modern pop album cover aesthetic, bright lighting",
    "Rock":         "gritty textures, electric guitars, dark dramatic lighting, rock album cover style",
    "Hip-Hop / Rap":"urban street art, bold typography, gold chains, hip-hop album aesthetic",
    "Electronic":   "futuristic, glowing neon grids, synthwave, digital art, electronic music aesthetic",
    "Indie":        "lo-fi film grain, pastel tones, vintage camera, indie album cover aesthetic",
    "R&B / Soul":   "warm golden tones, smooth gradients, soulful atmosphere, R&B album style",
    "Jazz":         "smoky jazz club, dim lighting, saxophone silhouette, classic jazz album art",
    "Metal":        "dark gothic imagery, fire and skulls, heavy metal album cover, intense contrast",
    "Türk Pop":     "Istanbul skyline, Bosphorus, Turkish patterns, modern Turkish pop aesthetic",
    "Klasik":       "elegant orchestra hall, classical instruments, refined and timeless album art",
}

# ──────────────────────────────────────────────────────────────
# Görsel oluşturma ayarları
# ──────────────────────────────────────────────────────────────
POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
COVER_IMAGE_WIDTH = 600
COVER_IMAGE_HEIGHT = 600
