# ============================================================
# gemini_api.py — Gemini LLM Entegrasyonu
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================
# GEREKSİNİM 4: Gemini, albüm meta verilerini JSON olarak üretir
# ============================================================

import json
from google import genai
from config import GEMINI_API_KEY

# Gemini istemcisini API anahtarıyla yapılandır
client = genai.Client(api_key=GEMINI_API_KEY)


def _strip_markdown_fences(text):
    """
    Gemini'nin bazen JSON'u sardığı markdown kod bloğu işaretlerini kaldırır.
    Örn: ```json ... ``` → düz JSON metni
    """
    text = text.strip()
    if text.startswith("```"):
        # Açılış işaret satırını kaldır
        text = text.split("```", 1)[1]
        # Dil tanımlayıcısını kaldır (örn: 'json')
        if text.startswith("json"):
            text = text[4:]
        # Kapanış işaretini kaldır
        if "```" in text:
            text = text.rsplit("```", 1)[0]
        text = text.strip()
    return text


def query_gemini(journal_text, genre, era, track_count):
    """
    Günlük girdisini ve parametreleri Gemini LLM'e gönderir.
    Albüm meta verilerini içeren bir sözlük döndürür:
        {
            "album_name": str,
            "artist_name": str,
            "year": str,
            "label": str,
            "mood_description": str,
            "cover_prompt": str,
            "lastfm_tags": [str, ...]
        }
    JSON ayrıştırma başarısız olursa ValueError fırlatır.
    API hataları için Exception fırlatır.
    """
    prompt = f"""You are a creative music AI. Based on the following journal entry / mood description, 
generate a FICTIONAL album concept. Return ONLY valid JSON with this exact schema:

{{
    "album_name": "A creative fictional album name",
    "artist_name": "A creative fictional artist name",
    "year": "A year that fits the {era} era",
    "label": "A fictional record label name",
    "mood_description": "A short 1-2 sentence description of the album's mood and vibe",
    "cover_prompt": "A detailed visual description for generating album cover art (do NOT include text or letters in the image description)",
    "lastfm_tags": ["array", "of", "4-6", "lowercase", "Last.fm", "compatible", "tag", "strings"]
}}

The genre is: {genre}
The era is: {era}
The desired number of tracks is: {track_count}


Important rules for lastfm_tags:
- If the user mentions a specific western pop star like "selena gomez" or "ariana grande", do NOT use their exact name as a tag since Last.fm tags prefer genres. Instead, combine the requested genre with specific sub-genres like "dance-pop", "contemporary r&b", "teen pop", or "synth-pop" that directly represent that artist's musical style to ensure their type of music populates the list.
- Include a mix of genre tags (e.g., "{genre}") and relevant mood tags.
- CRITICAL: If the selected genre is 'Türk Pop' or the prompt implies Turkish music, EVERY SINGLE TAG you generate MUST be chosen ONLY from this fixed list of valid Last.fm Turkish tags: ["türkçe pop", "türkçe", "turkish", "türkçe slow", "türkçe rock", "türkçe rap", "türkçe akustik", "türkçe 90lar"]. 
- NEVER invent or translate your own Turkish mood tags like "türkçe rahatlatıcı", "türkçe hüzünlü", or "türkçe rüyamsı" because they do not exist on Last.fm and will return 0 songs. If the mood is sad, use "türkçe slow". If the mood is happy/chill, use "türkçe pop" or "türkçe akustik".
- Use only lowercase, 4 to 6 tags total.

Journal entry:
\"{journal_text}\"

Return ONLY the JSON object, nothing else."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw_text = response.text.strip()

        # Varsa markdown kod bloğu işaretlerini kaldır
        clean_text = _strip_markdown_fences(raw_text)

        # JSON'u ayrıştır
        album_data = json.loads(clean_text)

        # Gerekli alanları doğrula
        required_fields = [
            "album_name", "artist_name", "year", "label",
            "mood_description", "cover_prompt", "lastfm_tags"
        ]
        for field in required_fields:
            if field not in album_data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(album_data["lastfm_tags"], list):
            raise ValueError("lastfm_tags must be a list")

        return album_data

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}\nRaw response: {raw_text}")
    except Exception as e:
        raise Exception(f"Gemini API error: {e}")
