from ib_async import IB
import asyncio


class InteractiveBroker:
    def __init__(self) -> None:
        self.ib = IB()
        self.servidor = '127.0.0.1'
        self.puerto = 4001
        self.id = 1

    async def conectar(self):
        await self.ib.connectAsync(self.servidor, self.puerto, clientId=self.id)

    async def obtener_valores_cuenta(self):
        return self.ib.accountValues()


async def main():
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
