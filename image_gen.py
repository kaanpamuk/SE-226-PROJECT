# ============================================================
# image_gen.py — Yapay Zeka Görsel Oluşturma (Pollinations.ai)
# PDA-226: Kurgusal Albüm Oluşturucu
# ============================================================
# GEREKSİNİM 6: Kapak istemi + tür stili → albüm kapak görseli
# ============================================================

import requests
from PIL import Image
import io
import time
import random
from urllib.parse import quote
from config import (
    POLLINATIONS_BASE_URL,
    COVER_IMAGE_WIDTH,
    COVER_IMAGE_HEIGHT,
    GENRE_VISUAL_STYLES,
)

# Prompt'un URL'de sorun yaratmaması için maksimum karakter sınırı
_MAX_PROMPT_LEN = 480
_MAX_RETRIES = 2


def _truncate_prompt(text, max_len=_MAX_PROMPT_LEN):
    """Prompt'u belirtilen uzunluğa kısaltır, kelime sınırından keser."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    # Son boşluktan kes ki kelime ortasından bölünmesin
    last_space = truncated.rfind(" ")
    if last_space > max_len // 2:
        truncated = truncated[:last_space]
    return truncated.rstrip(",. ")


def generate_cover(prompt, genre="Pop"):
    """
    Pollinations.ai kullanarak albüm kapak görseli oluşturur.
    Daha tutarlı bir sonuç için Gemini'nin ürettiği kapak istemini
    türün görsel stil açıklamasıyla birleştirir.

    Parametreler:
        prompt (str): Gemini'den gelen kapak görseli istemi
        genre (str): Seçilen müzik türü (görsel stil eklemek için kullanılır)

    Döndürür:
        PIL.Image: Oluşturulan kapak görseli (RGB formatında)

    Hatalar:
        Exception: Görsel oluşturma veya indirme başarısız olursa fırlatılır
    """
    # Gemini istemini türe özel görsel stille birleştir
    genre_style = GENRE_VISUAL_STYLES.get(genre, "")
    full_prompt = f"{prompt}, {genre_style}, album cover art, high quality, detailed"

    # Prompt'u kısalt — çok uzun URL'ler Pollinations'da 500 hatasına yol açar
    full_prompt = _truncate_prompt(full_prompt)

    # İstemi URL formatında kodla
    encoded_prompt = quote(full_prompt)

    # Rastgele seed ekle — her seferinde farklı görsel üretmek için
    seed = random.randint(1, 999999)

    # Pollinations URL'sini oluştur
    url = (
        f"{POLLINATIONS_BASE_URL}{encoded_prompt}"
        f"?width={COVER_IMAGE_WIDTH}"
        f"&height={COVER_IMAGE_HEIGHT}"
        f"&nologo=true"
        f"&seed={seed}"
    )

    # Retry mekanizması — geçici sunucu hatalarına karşı
    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=45)
            response.raise_for_status()

            # Yanıt baytlarını PIL Image nesnesine dönüştür
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
            return image

        except requests.exceptions.Timeout:
            last_error = "Image generation timed out. Please try again."
        except requests.exceptions.RequestException as e:
            last_error = f"Image generation failed: {e}"
        except Exception as e:
            last_error = f"Error processing generated image: {e}"

        # Son denemede değilse bekle ve tekrar dene
        if attempt < _MAX_RETRIES:
            time.sleep(2 * attempt)

    raise Exception(last_error)


