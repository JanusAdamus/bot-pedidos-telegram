# Bot de pedidos para Telegram

Bot para que una cafetería (o cualquier negocio chico) reciba pedidos por chat.  El cliente ve el menú, arma su carrito, confirma, y el pedido queda registrado con fecha, nombre, detalle y total.

## Comandos

| Comando | Qué hace |
|---|---|
| `/menu` | Muestra productos y precios |
| `/pedir latte 2` | Agrega al carrito |
| `/carrito` | Muestra el pedido y el total |
| `/confirmar` | Envía el pedido y lo guarda |
| `/cancelar` | Vacía el carrito |

## Uso

1. En Telegram, habla con [@BotFather](https://t.me/BotFather), crea un bot y copia el token.
2. Corre:

```bash
pip install -r requirements.txt
TELEGRAM_TOKEN=tu_token python bot.py
```

Los pedidos se guardan en `pedidos.csv`.

## Diseño

La lógica de pedidos (`pedidos.py`) está separada de Telegram, así que se prueba sin internet y se puede reutilizar en WhatsApp (API de WhatsApp Business) o en una página web.

```bash
pip install -r requirements-dev.txt
pytest
```

## Siguientes pasos típicos con un cliente

- Guardar en Google Sheets en vez de CSV para que el negocio vea los pedidos en vivo.
- Avisar al dueño por mensaje cada vez que entra un pedido.
- Menú editable desde una hoja de cálculo.
