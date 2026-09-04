import asyncio
from typing import NoReturn
from types import SimpleNamespace

from src.interactive_broker import InteractiveBroker


def test_conectar_devuelve_false_si_no_hay_conexion(monkeypatch):
    """Si el broker no responde, la conexión debe fallar de forma controlada."""
    broker = InteractiveBroker()

    async def conectar_que_falla(*args, **kwargs) -> NoReturn:
        raise ConnectionError("No hay servicio de IB")

    monkeypatch.setattr(broker.ib, "connectAsync", conectar_que_falla)

    assert asyncio.run(broker.conectar()) is False


def test_obtener_cartera_devuelve_lista_vacia_si_no_hay_conexion(monkeypatch):
    """Si no hay conexión, no se consulta ni se transforma la cartera."""
    broker = InteractiveBroker()

    monkeypatch.setattr(broker.ib, "isConnected", lambda: False)

    assert asyncio.run(broker.obtener_cartera()) == []


def test_obtener_cartera_formatea_posiciones_y_calcula_porcentajes(monkeypatch):
    """La cartera incluye los valores calculados para cada posición."""
    broker = InteractiveBroker()
    cartera = [
        SimpleNamespace(
            contract=SimpleNamespace(symbol="AAPL", primaryExchange="NASDAQ", exchange="SMART"),
            position=10.123456,
            averageCost=100.0,
            marketPrice=110.126,
            marketValue=1100.0,
            unrealizedPNL=100.0,
            realizedPNL=25.126,
        ),
        SimpleNamespace(
            contract=SimpleNamespace(symbol="MSFT", primaryExchange="", exchange="SMART"),
            position=5.0,
            averageCost=100.0,
            marketPrice=100.0,
            marketValue=500.0,
            unrealizedPNL=-25.0,
            realizedPNL=0.0,
        ),
    ]

    monkeypatch.setattr(broker.ib, "isConnected", lambda: True)
    monkeypatch.setattr(broker.ib, "portfolio", lambda: cartera)

    async def obtener_detalles_con_nombre(contrato):
        nombres = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
        }
        return [SimpleNamespace(longName=nombres[contrato.symbol])]

    monkeypatch.setattr(
        broker.ib,
        "reqContractDetailsAsync",
        obtener_detalles_con_nombre,
    )

    resultado = asyncio.run(broker.obtener_cartera())

    assert resultado == [
        {
            "Instrumento": "AAPL - (Apple Inc.) - NASDAQ",
            "Posición": 10.1235,
            "Último": 110.13,
            "Precio Medio": 100.0,
            "Base de Coste": 1012.35,
            "Valor Mercado": 1100.0,
            "% Liquidación Neta": 68.75,
            "PyG No Realizadas": 100.0,
            "% PyG No Realizadas": 9.88,
            "PyG Realizadas": 25.13,
        },
        {
            "Instrumento": "MSFT - (Microsoft Corporation) - SMART",
            "Posición": 5.0,
            "Último": 100.0,
            "Precio Medio": 100.0,
            "Base de Coste": 500.0,
            "Valor Mercado": 500.0,
            "% Liquidación Neta": 31.25,
            "PyG No Realizadas": -25.0,
            "% PyG No Realizadas": -5.0,
            "PyG Realizadas": 0.0,
        },
    ]
