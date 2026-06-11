import yt_dlp
from tqdm import tqdm
import random
import time
from utils import (
    VIDEO_URLS_FILE,
    VALID_VIDEOS_FILE,
    INVALID_VIDEOS_FILE,
    ERROR_REPORT_FILE,
    extract_video_id,
    classify_error,
    logger,
)
from youtube_comment_downloader import YoutubeCommentDownloader
from pathlib import Path

COOKIE_FILE = (
    Path(__file__).resolve().parent.parent /
    "cookies.txt"
)

YDL_OPTIONS = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": True,
    "cookiefile": str(COOKIE_FILE),
    "ignoreerrors": True,
    "noplaylist": True
}
def validate_comments(url: str):

    try:

        downloader = YoutubeCommentDownloader()

        comments = downloader.get_comments_from_url(url)

        first = next(iter(comments), None)

        if first:
            return True, None

        return False, "COMENTARIOS_DESACTIVADOS"

    except Exception as e:

        error = str(e)

        if "Failed to set sorting" in error:
            return False, "COMENTARIOS_DESACTIVADOS"

        return False, error
    
def validate_video(url: str):

    try:

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            if info:
                return True, None

    except Exception as e:

        ytdlp_error = str(e)

        logger.warning(
            f"yt-dlp falló para {url}: {ytdlp_error}"
        )

        # Intentar validar usando comentarios
        try:

            if validate_comments(url):

                logger.info(
                    f"Validado mediante comentarios: {url}"
                )

                return True, "VALIDO_COMENTARIOS"

        except Exception:
            pass

        return False, ytdlp_error

    return False, "ERROR_DESCONOCIDO"


def generate_report(valid_count, invalid_count, invalid_details):
    """
    Genera reporte de errores.
    """

    total = valid_count + invalid_count

    lines = [
        "========== REPORTE DE ERRORES ==========",
        "",
        f"TOTAL ANALIZADOS: {total}",
        f"VIDEOS VALIDOS: {valid_count}",
        f"VIDEOS INVALIDOS: {invalid_count}",
        "",
        "========== DETALLE ==========",
        ""
    ]

    for item in invalid_details:
        lines.append(item)

    ERROR_REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


def main():

    logger.info("Iniciando validación de videos...")

    urls = VIDEO_URLS_FILE.read_text(
        encoding="utf-8"
    ).splitlines()
    if not COOKIE_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de cookies: {COOKIE_FILE}"
        )
    valid_videos = []
    invalid_videos = []

    for url in tqdm(urls, desc="Validando videos"):
        # time.sleep(
        #     random.uniform(2, 6)
        # )
        video_id = extract_video_id(url)

        success, error = validate_video(url)

        if success:

            valid_videos.append(url)
            logger.info(f"VALIDO: {url}")

        else:

            category = classify_error(error)

            line = f"{video_id} | {url} | {error} | {category}"

            invalid_videos.append(line)

            logger.error(line)

    VALID_VIDEOS_FILE.write_text(
        "\n".join(valid_videos),
        encoding="utf-8"
    )

    INVALID_VIDEOS_FILE.write_text(
        "\n".join(invalid_videos),
        encoding="utf-8"
    )

    generate_report(
        len(valid_videos),
        len(invalid_videos),
        invalid_videos
    )

    logger.info("Validación completada.")


if __name__ == "__main__":
    main()