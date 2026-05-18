# LESCO Empathy AI

Sistema automatizado para extracción y análisis de comentarios de YouTube orientado a UX Research, Human-Centered Design (HCD) y generación automática de mapas de empatía mediante IA.

---

# Objetivo

Analizar comentarios de videos relacionados con aprendizaje de LESCO para detectar:

- emociones,
- frustraciones,
- necesidades,
- barreras,
- motivaciones,
- accesibilidad,
- inclusión social.

---

# Tecnologías

- Python 3.10+
- yt-dlp
- youtube-comment-downloader
- pandas
- tqdm
- nltk
- langdetect
- emoji

---

# Estructura del Proyecto

```text
lesco-empathy-ai/
```

---

# Instalación

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Pipeline de Ejecución

## 1. Extraer URLs

```bash
python scripts/extract_video_urls.py
```

Genera:

```text
output/video_urls.txt
```

---

## 2. Validar videos

```bash
python scripts/validate_videos.py
```

Genera:

```text
output/videos_validos.txt
output/videos_no_analizados.txt
output/reporte_errores.txt
```

---

## 3. Descargar comentarios

```bash
python scripts/download_comments.py
```

Genera:

```text
output/out.txt
```

---

## 4. Limpiar comentarios

```bash
python scripts/clean_comments.py
```

Genera:

```text
output/out_clean.txt
```

---

## 5. Generar prompt IA

```bash
python scripts/generate_empathy_prompt.py
```

Genera:

```text
output/empathy_prompt.txt
```

---

# Formato out.txt

```text
Video_Origen	ID_Video	Usuario	Comentario	Likes	Hace cuanto tiempo
```

---

# Logging

Todos los procesos generan:

```text
output/logs.txt
```

Incluye:

- timestamps,
- errores,
- videos procesados,
- cantidad de comentarios.

---

# Troubleshooting

## Error: yt-dlp no encontrado

Actualizar:

```bash
pip install -U yt-dlp
```

---

## Error: bloqueos de YouTube

Reducir velocidad de requests aumentando delays.

---

## Error: comentarios vacíos

Algunos videos tienen comentarios deshabilitados.

---

# Consideraciones Éticas

Este proyecto tiene fines académicos y de investigación UX/HCD.

Los comentarios utilizados:

- son públicos,
- deben anonimizarse para investigación formal,
- no deben utilizarse para vigilancia o profiling indebido.

---

# Objetivo Final

Los datos serán utilizados para:

- mapas de empatía,
- user personas,
- customer journey maps,
- storyboards,
- análisis UX,
- investigación HCD,
- empatía digital.