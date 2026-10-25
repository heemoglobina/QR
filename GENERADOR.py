
# Generador de códigos QR

from pathlib import Path

import qrcode
from PIL import ImageColor


def validar_color(color: str, nombre: str) -> str:
    # Valida un color para devolver su nombre o código HEX
    try:
        ImageColor.getrgb(color)
        return color
    except (ValueError, TypeError) as error:
        raise ValueError(
            f"El color de {nombre} no es válido"
        ) from error


def pedir_texto() -> str:
    # Solicita el contenido para el QR
    texto = input("Ingresá un texto o una URL: ").strip()

    if not texto:
        raise ValueError("El texto no puede estar vacío")

    return texto


def pedir_nombre_archivo() -> str:
    # Solicita el nombre que tendrá la imagen del QR
    nombre = input(
        "Ingresá un nombre para el archivo: "
    ).strip()

    if not nombre:
        raise ValueError(
            "El nombre del archivo no puede estar vacío"
        )

    caracteres_invalidos = '<>:"/\\|?*'

    if any(caracter in nombre for caracter in caracteres_invalidos):
        raise ValueError(
            "El nombre contiene caracteres no válidos"
        )

    if nombre in {".", ".."}:
        raise ValueError("El nombre del archivo no es válido")

    if not nombre.lower().endswith(".png"):
        nombre += ".png"

    return nombre


def pedir_colores() -> tuple[str, str]:
    # Pide y valida los colores del QR y del fondo
    color_qr = input(
        "Color del QR (ENTER para negro): "
    ).strip() or "black"

    color_fondo = input(
        "Color del fondo (ENTER para blanco): "
    ).strip() or "white"

    return (
        validar_color(color_qr, "QR"),
        validar_color(color_fondo, "fondo")
    )


def generar_qr(
    texto: str,
    nombre_archivo: str,
    color_qr: str = "black",
    color_fondo: str = "white"
) -> Path:
    # Genera el QR, guarda la imagen y devuelve su ruta
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_salida = carpeta_proyecto / nombre_archivo

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(texto)
    qr.make(fit=True)

    imagen = qr.make_image(
        fill_color=color_qr,
        back_color=color_fondo
    )

    imagen.save(ruta_salida)

    return ruta_salida.resolve()


def main() -> None:
    # Coordina la entrada de datos y la generación del QR
    try:
        texto = pedir_texto()
        nombre_archivo = pedir_nombre_archivo()
        color_qr, color_fondo = pedir_colores()

        ruta = generar_qr(
            texto,
            nombre_archivo,
            color_qr,
            color_fondo,
        )

        print("\n¡Código generado!")
        print(f"Ubicación: {ruta}")

    except qrcode.exceptions.DataOverflowError:
        print("Error: el contenido es demasiado grande")

    except (ValueError, OSError) as error:
        print(f"\nError: {error}")

    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada por el usuario")


if __name__ == "__main__":
    main()

