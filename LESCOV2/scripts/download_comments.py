import csv

from tqdm import tqdm
from youtube_comment_downloader import YoutubeCommentDownloader

from utils import (
    VALID_VIDEOS_FILE,
    OUT_FILE,
    extract_video_id,
    random_delay,
    logger,
)

downloader = YoutubeCommentDownloader()

import re

def clean_comment_text(text: str) -> str:
    """
    Limpia comentarios para guardarlos en una sola línea.
    """

    if not text:
        return ""

    # Saltos de línea
    text = re.sub(r'[\r\n]+', ' ', text)

    # Tabs
    text = re.sub(r'\t+', ' ', text)

    # Espacios múltiples
    text = re.sub(r'\s+', ' ', text)

    # Caracteres invisibles frecuentes
    text = text.replace('\u200b', '')
    text = text.replace('\ufeff', '')

    return text.strip()

def save_header_if_needed():
    """
    Escribe encabezado TSV.
    """

    if not OUT_FILE.exists():

        with open(
            OUT_FILE,
            "w",
            encoding="utf-8",
            newline=""
        ) as f:

            writer = csv.writer(
                f,
                delimiter="\t"
            )

            writer.writerow([
                "Video_Origen",
                "ID_Video",
                "Usuario",
                "Comentario",
                "Likes",
                "Hace cuanto tiempo"
            ])

def download_comments():

    logger.info("Iniciando descarga de comentarios...")

    save_header_if_needed()

    urls = VALID_VIDEOS_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    total_comments = 0

    with open(
        OUT_FILE,
        "a",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.writer(
            f,
            delimiter="\t"
        )

        for url in tqdm(urls, desc="Descargando comentarios"):

            try:

                video_id = extract_video_id(url)

                comments = downloader.get_comments_from_url(url)

                video_comments = 0

                for comment in comments:

                    comment_text = clean_comment_text(
                        comment.get("text", "")
                    )

                    if not comment_text:
                        continue

                    writer.writerow([
                        url,
                        video_id,
                        clean_comment_text(
                            comment.get("author", "")
                        ),
                        comment_text,
                        comment.get("votes", 0),
                        comment.get("time", "")
                    ])

                    video_comments += 1
                    total_comments += 1

                logger.info(
                    f"{video_id} -> {video_comments} comentarios"
                )

                random_delay()

            except Exception as e:

                logger.error(
                    f"Error descargando comentarios {url}: {e}"
                )

    logger.info(
        f"Comentarios descargados: {total_comments}"
    )


if __name__ == "__main__":
    download_comments()