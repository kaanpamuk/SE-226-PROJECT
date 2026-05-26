# SE226 — PDA-226 Project Report

## İzmir University of Economics
### 2025-2026 Spring — SE226 Software Engineering Project

---

## Group Members

| # | Full Name | Student ID | Contribution |
|---|-----------|------------|--------------|
| 1 | [İsim Soyisim] | [Öğrenci No] | [Katkı açıklaması] |
| 2 | [İsim Soyisim] | [Öğrenci No] | [Katkı açıklaması] |
| 3 | [İsim Soyisim] | [Öğrenci No] | [Katkı açıklaması] |

---

## 1. Project Overview

PDA-226, kullanıcının serbest metin girişini (günlük yazısı veya ruh hali açıklaması) alarak yapay zeka destekli hayali bir albüm oluşturan Python masaüstü uygulamasıdır. Uygulama:

- **Gemini LLM** ile albüm metadata'sı üretir (albüm adı, sanatçı, yıl, etiketler vb.)
- **Last.fm API** ile gerçek şarkılardan oluşan bir tracklist oluşturur
- **Pollinations.ai** ile yapay zeka destekli albüm kapağı görseli üretir
- Sonuçları **Spotify-tarzı** bir arayüzde sunar

---

## 2. Requirements Analysis

### REQUIREMENT 1 — Last.fm API (tag.gettoptracks) ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** `requests` kütüphanesi kullanılarak Last.fm Web API'nin `tag.gettoptracks` endpoint'i sorgulanmıştır. Gemini'den dönen tag'ler için birden fazla sorgu yapılarak sonuçlar birleştirilmiştir.

**İlgili Dosya:** `lastfm_api.py`

**Kod Snippet'i:**
```python
# lastfm_api.py — fetch_tracks_by_tag fonksiyonu
def fetch_tracks_by_tag(tag, limit=10):
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "limit": limit,
        "api_key": LASTFM_API_KEY,
        "format": "json",
    }
    headers = {"User-Agent": "AlbumCoverStudio/1.0"}
    response = requests.get(LASTFM_BASE_URL, params=params,
                           headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data.get("tracks", {}).get("track", [])
```

**Ekran Görüntüsü:** [Buraya Last.fm API sonuçlarının gösterildiği ekran görüntüsünü ekleyin]

---

### REQUIREMENT 2 — Tkinter GUI ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Tkinter ve ttk widget'ları kullanılarak GUI oluşturulmuştur. `ttk.Style` ile 'clam' teması üzerine Spotify-tarzı koyu tema uygulanmıştır. `ttk.Combobox`, `ttk.Spinbox` ve `ttk.Button` widget'ları kullanılmıştır.

**İlgili Dosya:** `gui.py`

**Kod Snippet'i:**
```python
# gui.py — Style setup
self.style = ttk.Style()
self.style.theme_use("clam")
self.style.configure("Generate.TButton",
                     background="#1DB954", foreground="#FFFFFF",
                     font=("Segoe UI", 11, "bold"))
```

**Ekran Görüntüsü:** [Buraya GUI'nin genel görünümünün ekran görüntüsünü ekleyin]

---

### REQUIREMENT 3 — Input Widgets with Defaults ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Kullanıcı girişi için çok satırlı metin alanı (Text), müzik türü (Combobox), dönem (Combobox) ve şarkı sayısı (Spinbox) widget'ları eklenmiştir. Her parametre için varsayılan değerler tanımlanmıştır.

**İlgili Dosya:** `gui.py`, `config.py`

**Kod Snippet'i:**
```python
# config.py — Default values
DEFAULT_GENRE = "Pop"
DEFAULT_ERA = "2020s"
DEFAULT_TRACK_COUNT = 8

# gui.py — Widgets
self.genre_var = tk.StringVar(value=DEFAULT_GENRE)
genre_combo = ttk.Combobox(inner, textvariable=self.genre_var,
                           values=GENRES, state="readonly")
```

**Ekran Görüntüsü:** [Buraya input widget'larının ekran görüntüsünü ekleyin]

---

### REQUIREMENT 4 — Gemini JSON Output ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** "Generate Album" butonuna basıldığında günlük metni ve parametreler Gemini'ye gönderilir. Gemini, JSON formatında albüm metadata'sı döner. Markdown code fence'leri otomatik olarak temizlenir.

**İlgili Dosya:** `gemini_api.py`

**Kod Snippet'i:**
```python
# gemini_api.py — Markdown fence stripping
def _strip_markdown_fences(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 1)[1]
        if text.startswith("json"):
            text = text[4:]
        if "```" in text:
            text = text.rsplit("```", 1)[0]
        text = text.strip()
    return text
```

**Ekran Görüntüsü:** [Buraya Gemini çıktısının gösterildiği ekran görüntüsünü ekleyin]

---

### REQUIREMENT 5 — Tracklist Deduplication ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Gemini'den dönen Last.fm tag'leri kullanılarak birden fazla sorgu yapılır. Tekrarlanan şarkılar filtrelenir ve kullanıcının istediği sayıda şarkı içeren final tracklist oluşturulur.

**İlgili Dosya:** `lastfm_api.py`

**Kod Snippet'i:**
```python
# lastfm_api.py — build_tracklist fonksiyonu
def build_tracklist(tags, track_count):
    seen = set()
    tracklist = []
    for tag in tags:
        raw_tracks = fetch_tracks_by_tag(tag, limit=per_tag_limit)
        for track in raw_tracks:
            dedup_key = f"{title.lower()} - {artist_name.lower()}"
            if dedup_key not in seen:
                seen.add(dedup_key)
                tracklist.append({...})
    return tracklist[:track_count]
```

**Ekran Görüntüsü:** [Buraya tracklist'in gösterildiği ekran görüntüsünü ekleyin]

---

### REQUIREMENT 6 — Cover Image Generation ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Gemini'den dönen cover prompt'u, seçilen müzik türünün görsel stil açıklamasıyla birleştirilerek Pollinations.ai'ye gönderilir. Üretilen görsel GUI'de gösterilir.

**İlgili Dosya:** `image_gen.py`

**Kod Snippet'i:**
```python
# image_gen.py — generate_cover fonksiyonu
def generate_cover(prompt, genre="Pop"):
    genre_style = GENRE_VISUAL_STYLES.get(genre, "")
    full_prompt = f"{prompt}, {genre_style}, album cover art"
    encoded_prompt = quote(full_prompt)
    url = f"{POLLINATIONS_BASE_URL}{encoded_prompt}?width=600&height=600&nologo=true"
    response = requests.get(url, timeout=90)
    return Image.open(io.BytesIO(response.content)).convert("RGB")
```

**Ekran Görüntüsü:** [Buraya üretilen albüm kapağının ekran görüntüsünü ekleyin]

---

### REQUIREMENT 7 — Spotify-Style Layout ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Albüm kapağı, metadata ve tracklist Spotify-tarzı bir düzende sunulur. Her şarkı satırında şarkı adı, sanatçı adı ve tıklanabilir "Listen" butonu bulunur. Listen butonu şarkının Last.fm sayfasını tarayıcıda açar.

**İlgili Dosya:** `gui.py`

**Kod Snippet'i:**
```python
# gui.py — Listen button
listen_btn = tk.Button(row, text="▶ Listen",
                       bg="#1DB954", fg="#FFFFFF",
                       command=lambda u=url: webbrowser.open(u))
```

**Ekran Görüntüsü:** [Buraya Spotify-tarzı arayüzün ekran görüntüsünü ekleyin]

---

### REQUIREMENT 8 — JSON + PNG Export ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Kullanıcı "Export Album" butonuna bastığında bir klasör seçim penceresi açılır. Albüm metadata'sı ve tracklist bir JSON dosyasına, kapak görseli bir PNG dosyasına kaydedilir.

**İlgili Dosya:** `gui.py`

**Kod Snippet'i:**
```python
# gui.py — export_album fonksiyonu
json_path = os.path.join(export_dir, f"{safe_name}.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

png_path = os.path.join(export_dir, f"{safe_name}.png")
self.cover_image.save(png_path, "PNG")
```

**Ekran Görüntüsü:** [Buraya export sonuçlarının ekran görüntüsünü ekleyin]

---

### REQUIREMENT 9 — Background Threading ✅ / ❌

**Status:** ✅ Satisfied / ❌ Not Satisfied

**Açıklama:** Gemini API çağrısı, Last.fm sorguları ve görsel indirme işlemleri `threading.Thread` kullanılarak arka plan thread'inde çalıştırılır. Status bar, kullanıcıyı mevcut adım hakkında bilgilendirir.

**İlgili Dosya:** `gui.py`

**Kod Snippet'i:**
```python
# gui.py — Background threading
thread = threading.Thread(
    target=self._generation_worker,
    args=(journal, genre, era, track_count),
    daemon=True
)
thread.start()

# Status updates
self.root.after(0, self._update_status, "✨ Gemini is thinking...", STATUS_YELLOW)
self.root.after(0, self._update_status, "🎵 Fetching tracks from Last.fm...", STATUS_YELLOW)
self.root.after(0, self._update_status, "🎨 Generating album cover...", STATUS_YELLOW)
```

**Ekran Görüntüsü:** [Buraya status bar'ın gösterildiği ekran görüntüsünü ekleyin]

---

## 3. Application Architecture

### File Structure
```
SE226 PROJECT/
├── main.py              # Application entry point
├── config.py            # API keys, constants, parameters
├── gemini_api.py        # Gemini LLM integration (REQ 4)
├── lastfm_api.py        # Last.fm API integration (REQ 1, 5)
├── image_gen.py         # Pollinations.ai image generation (REQ 6)
├── gui.py               # Tkinter GUI (REQ 2, 3, 7, 8, 9)
└── requirements.txt     # Python dependencies
```

### Data Flow
```
User Input → Gemini LLM → Album Metadata (JSON)
                        → Last.fm Tags → Real Tracks
                        → Cover Prompt → Pollinations.ai → Cover Image
                                       → Spotify-Style Dashboard
```

---

## 4. Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Programming language |
| Tkinter / ttk | GUI framework |
| requests | HTTP requests to APIs |
| google-generativeai | Gemini LLM SDK |
| Pillow (PIL) | Image processing |
| threading | Background operations |
| json | Data serialization |
| webbrowser | Opening Last.fm song pages |

---

## 5. Individual Contributions

### [Üye 1 — İsim Soyisim]
- **Çalıştığı dosyalar:** [Dosya listesi]
- **İmplemente ettiği fonksiyonlar:** [Fonksiyon listesi]
- **Çözdüğü problemler:** [Problem açıklaması]
- **Katkı detayı:** [Detaylı açıklama]

### [Üye 2 — İsim Soyisim]
- **Çalıştığı dosyalar:** [Dosya listesi]
- **İmplemente ettiği fonksiyonlar:** [Fonksiyon listesi]
- **Çözdüğü problemler:** [Problem açıklaması]
- **Katkı detayı:** [Detaylı açıklama]

### [Üye 3 — İsim Soyisim]
- **Çalıştığı dosyalar:** [Dosya listesi]
- **İmplemente ettiği fonksiyonlar:** [Fonksiyon listesi]
- **Çözdüğü problemler:** [Problem açıklaması]
- **Katkı detayı:** [Detaylı açıklama]

---

## 6. Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Gemini JSON'u markdown fence ile sarıyor | `_strip_markdown_fences()` fonksiyonu ile temizleme |
| Last.fm tag sorgularında tekrar eden şarkılar | `seen` set'i ile deduplication |
| GUI uzun işlemlerde donuyor | `threading.Thread` ile arka plan çalıştırma |
| [Ek sorun] | [Çözüm] |

---

## 7. Screenshots

### Initial State
[Uygulamanın başlangıç durumunun ekran görüntüsünü buraya ekleyin]

### Generated Album
[Albüm üretildikten sonraki ekran görüntüsünü buraya ekleyin]

### Export Result
[Export sonrası dosyaların ekran görüntüsünü buraya ekleyin]

---

## 8. References

1. [Gemini API Documentation](https://ai.google.dev/docs)
2. [Last.fm API Documentation](https://www.last.fm/api)
3. [Pollinations.ai](https://pollinations.ai/)
4. [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
5. [Ek referanslar buraya eklenecek]

---

## 9. Conclusion

[Projenin genel değerlendirmesi, öğrenilen dersler ve olası iyileştirmeler hakkında kısa bir sonuç paragrafı yazın.]
