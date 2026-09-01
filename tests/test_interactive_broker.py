import asyncio
from typing import NoReturn

from src.interactive_broker import InteractiveBroker


def test_conectar_devuelve_false_si_no_hay_conexion(monkeypatch):
    """Si el broker no responde, la conexión debe fallar de forma controlada."""
    broker = InteractiveBroker()

    async def conectar_que_falla(*args, **kwargs) -> NoReturn:
        raise ConnectionError("No hay servicio de IB")

    monkeypatch.setattr(broker.ib, "connectAsync", conectar_que_falla)

    assert asyncio.run(broker.conectar()) is False
