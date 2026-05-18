from pathlib import Path
import logging
import re
import random
import time
import unicodedata
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent

PLAYLIST_DIR = BASE_DIR / "playlist"
OUTPUT_DIR = BASE_DIR / "output"

VIDEO_URLS_FILE = OUTPUT_DIR / "video_urls.txt"
VALID_VIDEOS_FILE = OUTPUT_DIR / "videos_validos.txt"
INVALID_VIDEOS_FILE = OUTPUT_DIR / "videos_no_analizados.txt"
ERROR_REPORT_FILE = OUTPUT_DIR / "reporte_errores.txt"
OUT_FILE = OUTPUT_DIR / "out.txt"
OUT_CLEAN_FILE = OUTPUT_DIR / "out_clean.txt"
LOG_FILE = OUTPUT_DIR / "logs.txt"

OUTPUT_DIR.mkdir(exist_ok=True)

YOUTUBE_VIDEO_REGEX = re.compile(
    r"(https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{11})"
)

VIDEO_ID_REGEX = re.compile(r"v=([A-Za-z0-9_-]{11})")


def setup_logger(name: str) -> logging.Logger:
    """
    Configura logging global.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger("LESCO-EMPATHY-AI")


def extract_video_id(url: str) -> Optional[str]:
    """
    Extrae el ID del video desde una URL.
    """

    match = VIDEO_ID_REGEX.search(url)

    if match:
        return match.group(1)

    return None


def random_delay(min_seconds: int = 2, max_seconds: int = 5):
    """
    Delay aleatorio para evitar bloqueos.
    """

    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def normalize_text(text: str) -> str:
    """
    Normaliza texto Unicode.
    """

    text = unicodedata.normalize("NFKC", text)
    return text.strip()


def classify_error(error_message: str) -> str:
    """
    Clasifica errores de YouTube.
    """

    error_message = error_message.lower()

    if "private" in error_message:
        return "PRIVADO"

    if "unavailable" in error_message:
        return "NO DISPONIBLE"

    if "restricted" in error_message:
        return "RESTRINGIDO"

    if "blocked" in error_message:
        return "RESTRINGIDO"

    return "OTRO"