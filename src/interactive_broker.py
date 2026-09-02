from ib_async import IB, AccountValue, PortfolioItem


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

    async def obtener_cartera(self) -> list[PortfolioItem]:
        """
        Obtiene los datos de la cartera, incluyendo posiciones, precio de mercado, costo promedio y PNL.

        Returns:
            list[PortfolioItem]: lista de posiciones, precio de mercado y coste promedio
        """
        if not self.esta_conectado():
            return []

        cartera_crudo = self.ib.portfolio()
        cartera_formateada = []

        # valor total de la cartera
        valor_total_cartera = sum(item.marketValue for item in cartera_crudo)

        for item in cartera_crudo:
            simbolo: str = item.contract.symbol
            exchange: str = item.contract.primaryExchange or item.contract.exchange
            contrato: str = f'{simbolo} ({exchange})'
            base_coste: float = item.position * item.averageCost

            if base_coste != 0:
                pct_pyg_no_realizadas: float = (item.unrealizedPNL / base_coste) * 100
            else:
                pct_pyg_no_realizadas: float = 0.0

            if valor_total_cartera != 0:
                pct_liquidacion: float = (item.marketValue / valor_total_cartera) * 100
            else:
                pct_liquidacion: float = 0.0

            # Crear diccionario plano para que el st.dataframe lo parsee
            cartera_formateada.append({
                "Intrumento": contrato,
                "Posición": round(item.position, 4),
                "Último": round(item.marketPrice, 2),
                "Precio Medio": round(item.averageCost, 2),
                "Base de Coste": round(base_coste, 2),
                "Valor Mercado": round(item.marketValue, 2),
                "% Liquidación Neta": round(pct_liquidacion, 2),
                "PyG No Realizadas": round(item.unrealizedPNL, 2),
                "% PyG No Realizadas": round(pct_pyg_no_realizadas, 2),
                "PyG Realizadas": round(item.realizedPNL, 2)
            })

        return cartera_formateada
