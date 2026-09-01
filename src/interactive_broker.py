from ib_async import IB, AccountValue


class InteractiveBroker:
    def __init__(self) -> None:
        self.ib: IB = IB()
        self.servidor: str = '127.0.0.1'
        self.puerto: int = 4001
        self.id: int = 1

    async def conectar(self) -> bool:
        try:
            await self.ib.connectAsync(self.servidor, self.puerto, clientId=self.id)
            return True
        except Exception:
            return False

    def esta_conectado(self) -> bool:
        return self.ib.isConnected()

    async def obtener_valores_cuenta(self) -> list[AccountValue]:
        if not self.esta_conectado():
            return []
        return self.ib.accountValues()
