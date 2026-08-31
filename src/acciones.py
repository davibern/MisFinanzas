from ib_async import IB, AccountValue
import asyncio


class InteractiveBroker:
    def __init__(self) -> None:
        self.ib: IB = IB()
        self.servidor: str = '127.0.0.1'
        self.puerto: int = 4001
        self.id: int = 1

    async def conectar(self) -> None:
        await self.ib.connectAsync(self.servidor, self.puerto, clientId=self.id)

    async def obtener_valores_cuenta(self) -> list[AccountValue]:
        return self.ib.accountValues()


async def main() -> None:
    # Conectar al host local (puerto 4001) y un cliente único
    conexion = InteractiveBroker()
    await conexion.conectar()

    # Prueba
    print("Conexión establecida con éxito")
    try:
        valores = await conexion.obtener_valores_cuenta()
        print(valores)
    finally:
        conexion.ib.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
