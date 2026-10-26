import csv

import pytest

from pedidos import Carrito, guardar_pedido, interpretar_pedido


def test_carrito_suma_cantidades_y_total():
    carrito = Carrito()
    carrito.agregar("latte", 2)
    carrito.agregar("pan", 1)
    carrito.agregar("latte", 1)

    assert carrito.articulos == {"latte": 3, "pan": 1}
    assert carrito.total() == 3 * 60 + 25


@pytest.mark.parametrize("clave,cantidad", [("pizza", 1), ("latte", 0), ("latte", 99)])
def test_rechaza_producto_o_cantidad_invalida(clave, cantidad):
    with pytest.raises(ValueError):
        Carrito().agregar(clave, cantidad)


@pytest.mark.parametrize("args,esperado", [(["Latte", "2"], ("latte", 2)), (["pan"], ("pan", 1))])
def test_interpreta_comando(args, esperado):
    assert interpretar_pedido(args) == esperado


@pytest.mark.parametrize("args", [[], ["latte", "dos"]])
def test_comando_mal_escrito_da_mensaje(args):
    with pytest.raises(ValueError, match="/pedir"):
        interpretar_pedido(args)


def test_guarda_pedidos_en_csv(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    carrito = Carrito()
    carrito.agregar("cafe", 2)

    guardar_pedido(ruta, "Ana", carrito)
    guardar_pedido(ruta, "Luis", carrito)

    filas = list(csv.DictReader(ruta.open(encoding="utf-8")))
    assert [f["cliente"] for f in filas] == ["Ana", "Luis"]
    assert filas[0]["detalle"] == "2 Café americano"
    assert filas[0]["total"] == "90"
