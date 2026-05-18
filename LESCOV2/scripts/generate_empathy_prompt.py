import pandas as pd
from collections import Counter

from utils import (
    OUT_CLEAN_FILE,
    OUTPUT_DIR,
    logger
)

PROMPT_OUTPUT = OUTPUT_DIR / "empathy_prompt.txt"


KEYWORDS = {
    "frustracion": [
        "difícil",
        "rápido",
        "confuso",
        "frustrante",
        "entiendo",
        "problema"
    ],

    "motivacion": [
        "me encanta",
        "quiero aprender",
        "excelente",
        "gracias",
        "motivación"
    ],

    "inclusion": [
        "sordo",
        "familia",
        "inclusión",
        "comunidad",
        "comunicación"
    ]
}


def analyze_patterns(comments):

    patterns = {}

    joined = " ".join(comments).lower()

    for category, words in KEYWORDS.items():

        count = 0

        for word in words:
            count += joined.count(word)

        patterns[category] = count

    return patterns


def get_top_words(comments, top_n=20):

    text = " ".join(comments).lower()

    words = text.split()

    counter = Counter(words)

    return counter.most_common(top_n)


def build_prompt(patterns, top_words):

    return f"""
Crea un mapa de empatía profesional estilo UX Research y Human-Centered Design basado EXCLUSIVAMENTE en comentarios reales de YouTube sobre aprendizaje de LESCO en Costa Rica.

PATRONES DETECTADOS:

{patterns}

PALABRAS MÁS FRECUENTES:

{top_words}

REQUISITOS:

- detectar frustraciones,
- emociones,
- motivaciones,
- necesidades,
- barreras de aprendizaje,
- inclusión,
- accesibilidad,
- aprendizaje autodidacta.

Generar:

- ¿Qué piensa y siente?
- ¿Qué oye?
- ¿Qué ve?
- ¿Qué dice y hace?
- Esfuerzos / frustraciones
- Resultados / necesidades

NO INVENTAR INFORMACIÓN.
Usar únicamente patrones reales.
"""


def main():

    logger.info("Generando prompt IA...")

    df = pd.read_csv(
        OUT_CLEAN_FILE,
        sep="\t",
        encoding="utf-8"
    )

    comments = df["Comentario"].astype(str).tolist()

    patterns = analyze_patterns(comments)

    top_words = get_top_words(comments)

    prompt = build_prompt(
        patterns,
        top_words
    )

    PROMPT_OUTPUT.write_text(
        prompt,
        encoding="utf-8"
    )

    logger.info(
        f"Prompt generado: {PROMPT_OUTPUT}"
    )


if __name__ == "__main__":
    main()