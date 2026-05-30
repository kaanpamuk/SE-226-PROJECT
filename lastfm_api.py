
import requests
from config import LASTFM_BASE_URL, LASTFM_API_KEY


def fetch_tracks_by_tag(tag, limit=10):
    """
    Last.fm API'sinden belirli bir etiket için en popüler parçaları çeker.
    tag.gettoptracks uç noktasını kullanır.

    Parametreler:
        tag (str): Last.fm uyumlu bir etiket (örn: "indie", "sad", "rock")
        limit (int): Her etiket başına çekilecek maksimum parça sayısı

    Döndürür:
        list: Her biri şunları içeren parça sözlüklerinin listesi:
            - name (str): Şarkı adı
            - artist (dict): {"name": "Sanatçı Adı"}
            - url (str): Şarkının Last.fm sayfası URL'si
    """
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "limit": limit,
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }
    headers = {"User-Agent": "AlbumCoverStudio/1.0"}

    try:
        response = requests.get(
            LASTFM_BASE_URL,
            params=params,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return data.get("tracks", {}).get("track", [])
    except requests.exceptions.RequestException as e:
        print(f"[Last.fm] Error fetching tracks for tag '{tag}': {e}")
        return []
    except (ValueError, KeyError) as e:
        print(f"[Last.fm] Error parsing response for tag '{tag}': {e}")
        return []


def build_tracklist(tags, track_count):
    """
    Birden fazla Last.fm etiketini sorgulayarak tekrarsız bir parça listesi oluşturur.
    Tüm etiketlerdeki sonuçları birleştirir, tekrarları kaldırır ve
    tam olarak istenen sayıda parça döndürür.

    Parametreler:
        tags (list): Gemini'den gelen Last.fm etiketleri listesi
        track_count (int): Son listede istenen parça sayısı

    Döndürür:
        list: Şu anahtarları içeren parça sözlüklerinin listesi:
            - title (str): Şarkı adı
            - artist (str): Sanatçı adı
            - url (str): Last.fm sayfası URL'si
    """
    seen = set()
    tracklist = []


    per_tag_limit = max(10, (track_count * 2) // len(tags) + 2) if tags else 10

    for tag in tags:

        tag = tag.replace("&", "").replace("/", "").strip()

        # API Compatibility: Last.fm uses "rnb" instead of "rb" to index tracks.
        # This prevents empty API responses for R&B genre queries.
        if tag == "rb":
            tag = "rnb"

        if not tag:
            continue

        raw_tracks = fetch_tracks_by_tag(tag, limit=per_tag_limit)

        for track in raw_tracks:
            title = track.get("name", "Unknown Title")
            artist_name = track.get("artist", {}).get("name", "Unknown Artist")
            url = track.get("url", "")


            dedup_key = f"{title.lower()} - {artist_name.lower()}"

            if dedup_key not in seen:
                seen.add(dedup_key)
                tracklist.append({
                    "title": title,
                    "artist": artist_name,
                    "url": url,
                })


    import random
    random.shuffle(tracklist)


    return tracklist[:track_count]
