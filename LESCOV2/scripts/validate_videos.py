import yt_dlp
from tqdm import tqdm

from utils import (
    VIDEO_URLS_FILE,
    VALID_VIDEOS_FILE,
    INVALID_VIDEOS_FILE,
    ERROR_REPORT_FILE,
    extract_video_id,
    classify_error,
    logger,
)

YDL_OPTIONS = {
    "quiet": True,
    "skip_download": True,
    "extract_flat": False
}


def validate_video(url: str):
    """
    Valida video usando yt-dlp.
    """

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:

        try:
            info = ydl.extract_info(url, download=False)

            if not info:
                raise Exception("Información vacía")

            return True, None

        except Exception as e:
            return False, str(e)


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

    valid_videos = []
    invalid_videos = []

    for url in tqdm(urls, desc="Validando videos"):

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