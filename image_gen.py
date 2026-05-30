
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


_MAX_PROMPT_LEN = 480
_MAX_RETRIES = 3


def _truncate_prompt(text, max_len=_MAX_PROMPT_LEN):
    """Prompt'u belirtilen uzunluğa kısaltır, kelime sınırından keser."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
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

    genre_style = GENRE_VISUAL_STYLES.get(genre, "")
    full_prompt = f"{prompt}, {genre_style}, album cover art, high quality, detailed"


    full_prompt = _truncate_prompt(full_prompt)


    encoded_prompt = quote(full_prompt)


    seed = random.randint(1, 999999)


    url = (
        f"{POLLINATIONS_BASE_URL}{encoded_prompt}"
        f"?width={COVER_IMAGE_WIDTH}"
        f"&height={COVER_IMAGE_HEIGHT}"
        f"&nologo=true"
        f"&seed={seed}"
    )


    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()


            image = Image.open(io.BytesIO(response.content)).convert("RGB")
            return image

        except requests.exceptions.Timeout:
            last_error = "Image generation timed out. Please try again."
        except requests.exceptions.RequestException as e:
            last_error = f"Image generation failed: {e}"
        except Exception as e:
            last_error = f"Error processing generated image: {e}"


        if attempt < _MAX_RETRIES:
            time.sleep(2 * attempt)

    raise Exception(last_error)
