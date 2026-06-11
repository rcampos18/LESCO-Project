from pathlib import Path
import pandas as pd

OUT_FILE = Path("output/out.txt")

def main():

    df = pd.read_csv(
        OUT_FILE,
        sep="\t",
        encoding="utf-8"
    )

    # Eliminar usuarios vacíos
    df["Usuario"] = df["Usuario"].fillna("").astype(str).str.strip()

    df = df[df["Usuario"] != ""]

    total_comments = len(df)

    unique_users = df["Usuario"].nunique()

    print("=" * 50)
    print("ESTADÍSTICAS DE USUARIOS")
    print("=" * 50)
    print(f"Total comentarios: {total_comments:,}")
    print(f"Usuarios únicos: {unique_users:,}")
    print("=" * 50)

    # Top usuarios más activos
    print("\nTOP 20 USUARIOS MÁS ACTIVOS\n")

    top_users = (
        df["Usuario"]
        .value_counts()
        .head(20)
    )

    print(top_users)

    # Guardar usuarios únicos
    output_users = Path("output/usuarios_unicos.txt")

    usuarios = sorted(df["Usuario"].unique())

    output_users.write_text(
        "\n".join(usuarios),
        encoding="utf-8"
    )

    print(
        f"\nListado guardado en: {output_users}"
    )

if __name__ == "__main__":
    main()