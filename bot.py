"""Bot de Telegram que toma pedidos de una cafetería y los guarda en pedidos.csv.

Uso: TELEGRAM_TOKEN=xxxx python bot.py
"""
import logging
import os
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from pedidos import Carrito, guardar_pedido, interpretar_pedido, texto_menu

ARCHIVO_PEDIDOS = Path("pedidos.csv")
AYUDA = ("Hola, soy el bot de pedidos.\n"
         "/menu ver productos\n/pedir latte 2 agregar al carrito\n"
         "/carrito ver tu pedido\n/confirmar enviar pedido\n/cancelar vaciar carrito")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def carrito_de(context: ContextTypes.DEFAULT_TYPE) -> Carrito:
    return context.user_data.setdefault("carrito", Carrito())


async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(AYUDA)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(texto_menu())


async def pedir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        clave, cantidad = interpretar_pedido(context.args)
        carrito_de(context).agregar(clave, cantidad)
    except ValueError as error:
        await update.message.reply_text(str(error))
        return
    await update.message.reply_text(f"Agregado.\n\n{carrito_de(context).resumen()}")


async def ver_carrito(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(carrito_de(context).resumen())


async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    carrito = carrito_de(context)
    if not carrito.articulos:
        await update.message.reply_text("Tu carrito está vacío.  Usa /pedir para agregar algo.")
        return
    guardar_pedido(ARCHIVO_PEDIDOS, update.effective_user.full_name, carrito)
    await update.message.reply_text(f"Pedido recibido, gracias.\n\n{carrito.resumen()}")
    context.user_data["carrito"] = Carrito()


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["carrito"] = Carrito()
    await update.message.reply_text("Carrito vacío.")


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("Falta TELEGRAM_TOKEN.  Pídelo a @BotFather en Telegram.")
    app = Application.builder().token(token).build()
    for comando, funcion in [("start", inicio), ("menu", menu), ("pedir", pedir),
                             ("carrito", ver_carrito), ("confirmar", confirmar), ("cancelar", cancelar)]:
        app.add_handler(CommandHandler(comando, funcion))
    app.run_polling()


if __name__ == "__main__":
    main()
