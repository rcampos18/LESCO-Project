from pathlib import Path
from tqdm import tqdm
from utils import (
    PLAYLIST_DIR,
    VIDEO_URLS_FILE,
    YOUTUBE_VIDEO_REGEX,
    logger
)

def extract_urls():
    """
    Extrae URLs válidas de videos.
    """

    logger.info("Iniciando extracción de URLs...")

    all_urls = set()

    txt_files = list(PLAYLIST_DIR.glob("*.txt"))

    logger.info(f"TXT encontrados: {len(txt_files)}")

    for txt_file in tqdm(txt_files, desc="Procesando playlists"):

        try:
            content = txt_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            matches = YOUTUBE_VIDEO_REGEX.findall(content)

            for url in matches:

                if "&list=" in url:
                    continue

                all_urls.add(url.strip())

        except Exception as e:
            logger.error(f"Error leyendo {txt_file.name}: {e}")

    VIDEO_URLS_FILE.write_text(
        "\n".join(sorted(all_urls)),
        encoding="utf-8"
    )

    logger.info(f"URLs extraídas: {len(all_urls)}")
    logger.info(f"Archivo generado: {VIDEO_URLS_FILE}")


if __name__ == "__main__":
    extract_urls()