"""Lógica de pedidos, separada de Telegram para poder probarla sola."""
import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

MENU = {"cafe": ("Café americano", 45), "latte": ("Latte", 60), "pan": ("Pan dulce", 25), "sandwich": ("Sándwich", 85)}
CANTIDAD_MAXIMA = 20


@dataclass
class Carrito:
    articulos: dict[str, int] = field(default_factory=dict)

    def agregar(self, clave: str, cantidad: int) -> None:
        if clave not in MENU:
            raise ValueError(f"No tenemos '{clave}'.  Escribe /menu para ver las opciones.")
        if not 1 <= cantidad <= CANTIDAD_MAXIMA:
            raise ValueError(f"La cantidad debe ser de 1 a {CANTIDAD_MAXIMA}.")
        self.articulos[clave] = self.articulos.get(clave, 0) + cantidad

    def total(self) -> int:
        return sum(MENU[clave][1] * n for clave, n in self.articulos.items())

    def resumen(self) -> str:
        if not self.articulos:
            return "Tu carrito está vacío."
        lineas = [f"{n} x {MENU[c][0]} = ${MENU[c][1] * n}" for c, n in self.articulos.items()]
        return "\n".join(lineas + [f"Total: ${self.total()}"])


def texto_menu() -> str:
    return "\n".join(f"{clave}: {nombre} ${precio}" for clave, (nombre, precio) in MENU.items())


def interpretar_pedido(args: list[str]) -> tuple[str, int]:
    """'/pedir latte 2' -> ('latte', 2).  Si no hay cantidad, es 1."""
    if not args:
        raise ValueError("Escribe el producto, por ejemplo: /pedir latte 2")
    try:
        cantidad = int(args[1]) if len(args) > 1 else 1
    except ValueError:
        raise ValueError("La cantidad debe ser un número, por ejemplo: /pedir latte 2") from None
    return args[0].lower(), cantidad


def guardar_pedido(ruta: Path, cliente: str, carrito: Carrito) -> None:
    # shortcut: CSV local; para un cliente real se cambia por Google Sheets o su base de datos
    es_nuevo = not ruta.exists()
    with ruta.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if es_nuevo:
            escritor.writerow(["fecha", "cliente", "detalle", "total"])
        detalle = "; ".join(f"{n} {MENU[c][0]}" for c, n in carrito.articulos.items())
        escritor.writerow([datetime.now().isoformat(timespec="seconds"), cliente, detalle, carrito.total()])
