"""
Pobla la base de datos con un usuario demo y varios videos de ejemplo,
usando enlaces públicos de video (Blender Foundation / Google Sample
Videos) para que la app funcione de inmediato para cualquiera que
clone el repositorio, sin necesidad de subir archivos pesados a Git.

Uso:
    python seed.py

Nota: en producción esto se ejecuta automáticamente al arrancar la app
(ver app.py), así que normalmente no necesitas correr este script tú
mismo salvo en tu máquina local.
"""
from app import create_app
from seed_data import seed_if_empty


def seed():
    app = create_app()
    with app.app_context():
        created = seed_if_empty()
        if created:
            print("Listo: videos de ejemplo creados.")
            print("Usuario demo -> usuario: demo | contraseña: demo1234")
        else:
            print("La base de datos ya tenía videos. No se hizo nada.")


if __name__ == "__main__":
    seed()
