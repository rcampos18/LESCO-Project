import re
import pandas as pd
import emoji

from tqdm import tqdm
from langdetect import detect

from utils import (
    OUT_FILE,
    OUT_CLEAN_FILE,
    normalize_text,
    logger
)


def clean_text(text: str) -> str:
    """
    Limpieza de comentarios.
    """

    if pd.isna(text):
        return ""

    text = normalize_text(text)

    text = emoji.replace_emoji(text, replace="")

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[\r\n\t]+", " ", text)

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\w\sáéíóúÁÉÍÓÚñÑ.,!?¿()]", "", text)

    return text.strip()


def detect_language(text: str) -> str:
    """
    Detecta idioma.
    """

    try:
        return detect(text)

    except Exception:
        return "unknown"


def main():

    logger.info("Iniciando limpieza de comentarios...")

    df = pd.read_csv(
        OUT_FILE,
        sep="\t",
        encoding="utf-8"
    )

    tqdm.pandas()

    df["Comentario"] = df["Comentario"].progress_apply(clean_text)

    df = df[df["Comentario"].str.strip() != ""]

    df["Idioma"] = df["Comentario"].progress_apply(detect_language)

    df.to_csv(
        OUT_CLEAN_FILE,
        sep="\t",
        index=False,
        encoding="utf-8"
    )

    logger.info(
        f"Comentarios limpios: {len(df)}"
    )

    logger.info(
        f"Archivo generado: {OUT_CLEAN_FILE}"
    )


if __name__ == "__main__":
    main()