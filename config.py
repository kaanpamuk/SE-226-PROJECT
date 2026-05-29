# ============================================================
# config.py — API Anahtarları, Sabitler ve Uygulama Parametreleri
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================

# ──────────────────────────────────────────────────────────────
# API ANAHTARLARI — Çalıştırmadan önce kendi anahtarlarınızla değiştirin
# ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AQ.Ab8RN6Jo_L1hnHblvUNYPCGkL7Y9lmYD4Isjif0VheosN34Zpw"
LASTFM_API_KEY = "56b29f8172077e6005444fb5d19b84af"

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
# Genre → guaranteed Last.fm tag(s) prepended to Gemini's tags
# Era → kısa Last.fm tag
ERA_SHORTHAND = {
    "1970s": "70s",
    "1980s": "80s",
    "1990s": "90s",
    "2000s": "2000s",
    "2010s": "2010s",
    "2020s": "2020s",
}

# Genre → kısa Last.fm tag
GENRE_SHORTHAND = {
    "Pop":           "pop",
    "Rock":          "rock",
    "Hip-Hop / Rap": "hip-hop",
    "Electronic":    "electronic",
    "Indie":         "indie",
    "R&B / Soul":    "r&b",
    "Jazz":          "jazz",
    "Metal":         "metal",
    "Türk Pop":      "turkish pop",
    "Klasik":        "classical",
}

GENRE_LASTFM_SEED_TAGS = {
    "Pop":          ["pop"],
    "Rock":         ["rock"],
    "Hip-Hop / Rap":["hip-hop", "rap"],
    "Electronic":   ["electronic"],
    "Indie":        ["indie"],
    "R&B / Soul":   ["r&b", "soul"],
    "Jazz":         ["jazz"],
    "Metal":        ["metal"],
    "Türk Pop":     ["turkish pop", "turk pop", "turkish"],
    "Klasik":       ["classical", "classical music"],
}

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
COVER_IMAGE_WIDTH = 600
COVER_IMAGE_HEIGHT = 600


